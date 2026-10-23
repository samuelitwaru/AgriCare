from django.db import models


class AgroecologicalZone(models.Model):
    """Reference zones used to scope advisories and prediction models.

    Boundaries stay as GeoJSON here until GIS_ENABLED=True switches the
    project onto PostGIS, at which point this field is replaced by a
    django.contrib.gis.db.models.MultiPolygonField via migration.
    """

    name = models.CharField(max_length=255, unique=True)
    code = models.SlugField(max_length=32, unique=True)
    region = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    boundary_geojson = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class WeatherObservationManager(models.Manager):
    def upsert_fields(self, zone, observed_date, source, **fields):
        """Merge one source's fields into the shared zone/day row without
        touching columns owned by other sources, and record that source's
        contribution in raw_payload (keyed by source, not overwritten).
        """
        obs, _ = self.get_or_create(zone=zone, observed_date=observed_date)
        for key, value in fields.items():
            setattr(obs, key, value)
        raw = obs.raw_payload or {}
        raw[source] = fields
        obs.raw_payload = raw
        obs.save()
        return obs


class WeatherObservation(models.Model):
    """One row per zone per day, assembled from multiple ingestion sources
    (CHIRPS rainfall, NDVI, station/API temperature). Each ingestion task
    updates only the columns it owns, so this works as a shared feature row
    rather than a per-source log. raw_payload keeps each source's untouched
    response, keyed by source name, for reprocessing without re-fetching.
    """

    zone = models.ForeignKey(AgroecologicalZone, on_delete=models.CASCADE, related_name="weather_observations")
    observed_date = models.DateField()
    rainfall_mm = models.FloatField(null=True, blank=True)
    temperature_c = models.FloatField(null=True, blank=True)
    ndvi = models.FloatField(null=True, blank=True)
    raw_payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WeatherObservationManager()

    class Meta:
        unique_together = ("zone", "observed_date")

    def __str__(self):
        return f"{self.zone.code} {self.observed_date}"
