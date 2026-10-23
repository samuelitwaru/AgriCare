from django.contrib import admin

from .models import Farm, FarmOutcome


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "crop_type", "zone", "size_acres")
    list_filter = ("crop_type", "zone")
    search_fields = ("name", "owner__username")


@admin.register(FarmOutcome)
class FarmOutcomeAdmin(admin.ModelAdmin):
    list_display = ("farm", "season", "planted_date", "yield_kg_per_acre", "pest_incident_reported")
    list_filter = ("season", "pest_incident_reported")
