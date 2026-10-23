"""Thin client around the Google Earth Engine Python API.

CHIRPS (rainfall) and NDVI both live as public Earth Engine ImageCollections,
so one authenticated client covers both rather than maintaining separate
integrations per data source. Computation (reduceRegion) runs server-side on
Google's infrastructure, which avoids needing GDAL installed locally.
"""

from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

_initialized = False

CHIRPS_COLLECTION = "UCSB-CHG/CHIRPS/DAILY"
CHIRPS_SCALE_METERS = 5566  # native ~0.05 degree resolution

# MOD13Q1 is a 16-day composite, not a daily product - composites get
# published on a fixed cadence Google doesn't document precisely enough to
# calculate locally, so querying the most recent one within a lookback
# window is more robust than assuming a specific day-of-year alignment.
NDVI_COLLECTION = "MODIS/061/MOD13Q1"
NDVI_BAND = "NDVI"
NDVI_SCALE_METERS = 250
NDVI_SCALE_FACTOR = 0.0001  # MOD13Q1 stores NDVI as raw int16 * 10000
NDVI_LOOKBACK_DAYS = 32  # ~2 composite cycles, safety margin


def init_earth_engine():
    global _initialized
    if _initialized:
        return

    import ee

    email = settings.EE_SERVICE_ACCOUNT_EMAIL
    key_file = settings.EE_SERVICE_ACCOUNT_KEY_FILE
    if not email or not key_file:
        raise ImproperlyConfigured(
            "EE_SERVICE_ACCOUNT_EMAIL and EE_SERVICE_ACCOUNT_KEY_FILE must be set in .env "
            "before Earth Engine calls can run."
        )

    credentials = ee.ServiceAccountCredentials(email, key_file)
    ee.Initialize(credentials, project=settings.EE_PROJECT_ID or None)
    _initialized = True


def get_chirps_image(target_date):
    """The CHIRPS daily image for one date, or None if it hasn't been published yet.

    ee.ImageCollection.first() never returns Python None even when the
    collection is empty - it's a lazy server-side reference that only fails
    once you try to compute on it. So the emptiness has to be checked
    explicitly via size(), before the image is handed to reduceRegion.
    """
    import ee

    init_earth_engine()

    start = target_date.isoformat()
    end = (target_date + timedelta(days=1)).isoformat()
    collection = ee.ImageCollection(CHIRPS_COLLECTION).filterDate(start, end)

    if collection.size().getInfo() == 0:
        return None
    return collection.first()


def reduce_mean_over_geometry(image, boundary_geojson):
    """Mean pixel value of a CHIRPS image over a zone's boundary."""
    import ee

    geometry = ee.Geometry(boundary_geojson)
    stats = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=CHIRPS_SCALE_METERS,
        maxPixels=1e9,
    ).getInfo()

    return stats.get("precipitation") if stats else None


def get_latest_ndvi_image(target_date):
    """The most recent NDVI composite at or before target_date, within
    NDVI_LOOKBACK_DAYS, paired with the calendar date it actually covers.

    Returns (observed_date, image), or (None, None) if nothing is published
    in that window.
    """
    import ee

    init_earth_engine()

    start = (target_date - timedelta(days=NDVI_LOOKBACK_DAYS)).isoformat()
    end = (target_date + timedelta(days=1)).isoformat()
    collection = (
        ee.ImageCollection(NDVI_COLLECTION)
        .filterDate(start, end)
        .select(NDVI_BAND)
        .sort("system:time_start", False)
    )

    if collection.size().getInfo() == 0:
        return None, None

    image = collection.first()
    millis = image.get("system:time_start").getInfo()

    from datetime import datetime, timezone as dt_timezone

    observed_date = datetime.fromtimestamp(millis / 1000, tz=dt_timezone.utc).date()
    return observed_date, image


def reduce_ndvi_over_geometry(image, boundary_geojson):
    """Mean NDVI over a zone's boundary, scaled from MOD13Q1's raw int16 storage."""
    import ee

    geometry = ee.Geometry(boundary_geojson)
    stats = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=NDVI_SCALE_METERS,
        maxPixels=1e9,
    ).getInfo()

    raw_value = stats.get(NDVI_BAND) if stats else None
    return raw_value * NDVI_SCALE_FACTOR if raw_value is not None else None
