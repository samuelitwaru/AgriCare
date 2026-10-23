from django.conf import settings
from django.db import models

from apps.geodata.models import AgroecologicalZone


class Farm(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="farms")
    zone = models.ForeignKey(AgroecologicalZone, on_delete=models.SET_NULL, null=True, blank=True, related_name="farms")
    name = models.CharField(max_length=255)
    crop_type = models.CharField(max_length=100)
    size_acres = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # Point location until GIS_ENABLED=True swaps this for PointField.
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    boundary_geojson = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.owner})"


class FarmOutcome(models.Model):
    """Farmer-reported ground truth used as training labels for Phase 3 ML models."""

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="outcomes")
    season = models.CharField(max_length=32)
    planted_date = models.DateField(null=True, blank=True)
    yield_kg_per_acre = models.FloatField(null=True, blank=True)
    pest_incident_reported = models.BooleanField(default=False)
    pest_notes = models.TextField(blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farm} - {self.season}"
