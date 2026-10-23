from django.db import models

from apps.farms.models import Farm


class ModelVersion(models.Model):
    """Registry entry for a trained model artifact (mirrors what MLflow would track)."""

    target = models.CharField(max_length=64)  # e.g. drought_risk, yield, pest_outbreak
    version = models.CharField(max_length=32)
    artifact_path = models.CharField(max_length=512)
    training_metrics = models.JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    trained_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("target", "version")

    def __str__(self):
        return f"{self.target} v{self.version}"


class Prediction(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="predictions")
    model_version = models.ForeignKey(ModelVersion, on_delete=models.CASCADE, related_name="predictions")
    target = models.CharField(max_length=64)
    predicted_value = models.FloatField(null=True, blank=True)
    predicted_label = models.CharField(max_length=64, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    predicted_for_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["farm", "target", "predicted_for_date"])]

    def __str__(self):
        return f"{self.target} for {self.farm} on {self.predicted_for_date}"
