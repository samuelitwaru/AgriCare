from django.contrib import admin

from .models import Advisory, AdvisoryDelivery


class AdvisoryDeliveryInline(admin.TabularInline):
    model = AdvisoryDelivery
    extra = 0


@admin.register(Advisory)
class AdvisoryAdmin(admin.ModelAdmin):
    list_display = ("advisory_type", "farm", "risk_level", "source", "generated_at")
    list_filter = ("advisory_type", "risk_level", "source")
    inlines = [AdvisoryDeliveryInline]
