import logging
from datetime import date, timedelta

from celery import shared_task
from django.utils import timezone

from .models import AgroecologicalZone, WeatherObservation
from .services import (
    get_chirps_image,
    get_latest_ndvi_image,
    init_earth_engine,
    reduce_mean_over_geometry,
    reduce_ndvi_over_geometry,
)

logger = logging.getLogger(__name__)

SOURCE_CHIRPS = "chirps"
SOURCE_NDVI = "ndvi"

# Starting point for the search; CHIRPS's actual publication lag isn't
# documented precisely enough to hardcode, so find_latest_chirps_image()
# walks backward from here until it finds a published image.
DEFAULT_LAG_DAYS = 5
MAX_LOOKBACK_DAYS = 30
NDVI_DEFAULT_LAG_DAYS = 5


def find_latest_chirps_image(start_date):
    """Walk backward from start_date until a published CHIRPS image is found."""
    for offset in range(MAX_LOOKBACK_DAYS):
        candidate = start_date - timedelta(days=offset)
        image = get_chirps_image(candidate)
        if image is not None:
            return candidate, image
    return None, None


@shared_task
def ingest_chirps_rainfall(target_date: str | None = None):
    """Pull daily CHIRPS rainfall for every zone that has a boundary, and
    upsert it into WeatherObservation. Zones without boundary_geojson are
    skipped (nothing to query against) rather than erroring out.
    """
    start = date.fromisoformat(target_date) if target_date else timezone.localdate() - timedelta(days=DEFAULT_LAG_DAYS)

    # Fail fast and loud on setup/auth problems rather than retrying the same
    # broken credentials across every zone and reporting an opaque "skipped".
    init_earth_engine()

    target, image = find_latest_chirps_image(start)
    if image is None:
        logger.error("No CHIRPS image found within %s days before %s", MAX_LOOKBACK_DAYS, start.isoformat())
        return {"date": None, "processed": 0, "skipped": 0, "error": "no_chirps_image_found"}

    zones = AgroecologicalZone.objects.exclude(boundary_geojson__isnull=True)
    processed, skipped = 0, 0

    for zone in zones:
        try:
            rainfall_mm = reduce_mean_over_geometry(image, zone.boundary_geojson)
        except Exception:
            logger.exception("CHIRPS ingestion failed for zone %s (%s)", zone.code, zone.name)
            skipped += 1
            continue

        if rainfall_mm is None:
            skipped += 1
            continue

        WeatherObservation.objects.upsert_fields(
            zone=zone,
            observed_date=target,
            source=SOURCE_CHIRPS,
            rainfall_mm=rainfall_mm,
        )
        processed += 1

    return {"date": target.isoformat(), "processed": processed, "skipped": skipped}


@shared_task
def ingest_ndvi(target_date: str | None = None):
    """Pull the most recent NDVI composite for every zone that has a
    boundary, and upsert it into WeatherObservation alongside any rainfall
    already recorded for that date.
    """
    start = date.fromisoformat(target_date) if target_date else timezone.localdate() - timedelta(days=NDVI_DEFAULT_LAG_DAYS)

    init_earth_engine()

    observed_date, image = get_latest_ndvi_image(start)
    if image is None:
        logger.error("No NDVI composite found within lookback window before %s", start.isoformat())
        return {"date": None, "processed": 0, "skipped": 0, "error": "no_ndvi_image_found"}

    zones = AgroecologicalZone.objects.exclude(boundary_geojson__isnull=True)
    processed, skipped = 0, 0

    for zone in zones:
        try:
            ndvi_value = reduce_ndvi_over_geometry(image, zone.boundary_geojson)
        except Exception:
            logger.exception("NDVI ingestion failed for zone %s (%s)", zone.code, zone.name)
            skipped += 1
            continue

        if ndvi_value is None:
            skipped += 1
            continue

        WeatherObservation.objects.upsert_fields(
            zone=zone,
            observed_date=observed_date,
            source=SOURCE_NDVI,
            ndvi=ndvi_value,
        )
        processed += 1

    return {"date": observed_date.isoformat(), "processed": processed, "skipped": skipped}
