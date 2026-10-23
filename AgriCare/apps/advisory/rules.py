"""Rule-based agri-climate advisory generation (Phase 1 - explicit
thresholds, not ML). This is the honest starting point: there isn't yet
enough farmer-reported outcome data (see apps.farms.models.FarmOutcome) to
train real prediction models, so advisories come from simple rules applied
to the rainfall/NDVI data ingested from CHIRPS/MODIS.

IMPORTANT: the threshold values below are illustrative starting points, not
validated agronomic figures for Uganda. They need review against real
crop-water-requirement guidance (e.g. NARO extension data) before being
relied on for actual farmer decisions. Kept centralized here so they're easy
to find and recalibrate once better guidance is available.
"""

from dataclasses import dataclass
from datetime import timedelta

from django.utils import timezone

RAINFALL_WINDOW_DAYS = 14
RAINFALL_MIN_OBSERVED_DAYS = 5  # don't call drought risk from a near-empty window
LOW_RAINFALL_THRESHOLD_MM = 20  # PLACEHOLDER - needs agronomic validation

NDVI_HIGH_RISK_THRESHOLD = 0.3
NDVI_MEDIUM_RISK_THRESHOLD = 0.5

RAINFALL_ADVISORY_VALIDITY_DAYS = 7
NDVI_ADVISORY_VALIDITY_DAYS = 14  # matches the MOD13Q1 composite cadence


@dataclass
class Finding:
    advisory_type: str
    title: str
    message: str
    risk_level: str
    validity_days: int


def evaluate_rainfall(zone, as_of):
    window_start = as_of - timedelta(days=RAINFALL_WINDOW_DAYS)
    observations = zone.weather_observations.filter(
        observed_date__gte=window_start, observed_date__lte=as_of, rainfall_mm__isnull=False
    )
    observed_days = observations.count()
    if observed_days < RAINFALL_MIN_OBSERVED_DAYS:
        return None  # too little data in the window to call this confidently

    total_rainfall = sum(o.rainfall_mm for o in observations)
    if total_rainfall >= LOW_RAINFALL_THRESHOLD_MM:
        return None

    return Finding(
        advisory_type="drought_risk",
        title="Low rainfall in your area",
        message=(
            f"Only {total_rainfall:.1f}mm of rain has fallen in your district over the last "
            f"{observed_days} observed days (target: {LOW_RAINFALL_THRESHOLD_MM}mm+ over "
            f"{RAINFALL_WINDOW_DAYS} days). Consider delaying planting or prioritizing "
            "drought-tolerant practices until rainfall improves."
        ),
        risk_level="high" if total_rainfall < LOW_RAINFALL_THRESHOLD_MM / 2 else "medium",
        validity_days=RAINFALL_ADVISORY_VALIDITY_DAYS,
    )


def evaluate_ndvi(zone, as_of):
    latest = (
        zone.weather_observations.filter(observed_date__lte=as_of, ndvi__isnull=False)
        .order_by("-observed_date")
        .first()
    )
    if latest is None:
        return None

    if latest.ndvi < NDVI_HIGH_RISK_THRESHOLD:
        risk_level = "high"
    elif latest.ndvi < NDVI_MEDIUM_RISK_THRESHOLD:
        risk_level = "medium"
    else:
        return None  # healthy vegetation, nothing to flag

    return Finding(
        advisory_type="vegetation_stress",
        title="Vegetation stress detected",
        message=(
            f"Satellite vegetation health (NDVI) in your district is {latest.ndvi:.2f} as of "
            f"{latest.observed_date}, below the healthy range. This can indicate water stress, "
            "poor soil conditions, or early-stage pest/disease pressure."
        ),
        risk_level=risk_level,
        validity_days=NDVI_ADVISORY_VALIDITY_DAYS,
    )


EVALUATORS = (evaluate_rainfall, evaluate_ndvi)


def evaluate_zone(zone, as_of=None):
    as_of = as_of or timezone.localdate()
    return [finding for finding in (evaluator(zone, as_of) for evaluator in EVALUATORS) if finding is not None]
