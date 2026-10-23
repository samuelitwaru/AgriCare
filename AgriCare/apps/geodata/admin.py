from django.contrib import admin

from .models import AgroecologicalZone, WeatherObservation


@admin.register(AgroecologicalZone)
class AgroecologicalZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "region")
    search_fields = ("name", "code", "region")


@admin.register(WeatherObservation)
class WeatherObservationAdmin(admin.ModelAdmin):
    list_display = ("zone", "observed_date", "rainfall_mm", "temperature_c", "ndvi")
    list_filter = ("zone",)
    date_hierarchy = "observed_date"
