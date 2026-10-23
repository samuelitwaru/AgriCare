from django.contrib import admin

from .models import ModelVersion, Prediction


@admin.register(ModelVersion)
class ModelVersionAdmin(admin.ModelAdmin):
    list_display = ("target", "version", "is_active", "trained_at")
    list_filter = ("target", "is_active")


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("target", "farm", "predicted_value", "predicted_label", "confidence", "predicted_for_date")
    list_filter = ("target",)
    date_hierarchy = "predicted_for_date"
