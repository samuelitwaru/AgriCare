from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.utils import timezone
from django.views.generic import ListView, TemplateView

from apps.advisory.models import Advisory
from apps.farms.models import Farm, FarmOutcome
from apps.geodata.models import AgroecologicalZone


class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"


class DashboardLogoutView(LogoutView):
    next_page = "dashboard:login"


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Dashboard access is provisioned (is_staff set via Django admin), not
    self-service - public registration always creates a plain farmer
    account, so this intentionally can't be reached by signing up.
    """

    login_url = "dashboard:login"

    def test_func(self):
        return self.request.user.is_staff


class HomeView(StaffRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        active_advisories = Advisory.objects.filter(valid_until__gte=now) | Advisory.objects.filter(valid_until__isnull=True)
        context.update(
            {
                "farm_count": Farm.objects.count(),
                "zone_count": AgroecologicalZone.objects.count(),
                "active_advisory_count": active_advisories.count(),
                "high_risk_count": active_advisories.filter(risk_level=Advisory.RiskLevel.HIGH).count(),
                "recent_outcomes_count": FarmOutcome.objects.filter(
                    reported_at__gte=now - timezone.timedelta(days=30)
                ).count(),
                "recent_advisories": Advisory.objects.select_related("farm").order_by("-generated_at")[:10],
            }
        )
        return context


class ZoneListView(StaffRequiredMixin, ListView):
    template_name = "dashboard/zones.html"
    context_object_name = "zones"
    paginate_by = 50

    def get_queryset(self):
        qs = AgroecologicalZone.objects.all().order_by("name")
        region = self.request.GET.get("region")
        if region:
            qs = qs.filter(region=region)
        return qs.prefetch_related("weather_observations")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["regions"] = (
            AgroecologicalZone.objects.exclude(region="").values_list("region", flat=True).distinct().order_by("region")
        )
        context["selected_region"] = self.request.GET.get("region", "")
        # weather_observations was prefetched in get_queryset, so picking the
        # latest here in Python reuses that cache instead of one query per zone
        for zone in context["zones"]:
            zone.latest_weather = max(
                zone.weather_observations.all(), key=lambda w: w.observed_date, default=None
            )
        return context


class FarmListView(StaffRequiredMixin, ListView):
    template_name = "dashboard/farms.html"
    context_object_name = "farms"
    paginate_by = 50

    def get_queryset(self):
        qs = Farm.objects.select_related("owner", "zone").order_by("-created_at")
        zone_code = self.request.GET.get("zone")
        if zone_code:
            qs = qs.filter(zone__code=zone_code)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["zones"] = AgroecologicalZone.objects.order_by("name")
        context["selected_zone"] = self.request.GET.get("zone", "")
        return context


class AdvisoryListView(StaffRequiredMixin, ListView):
    template_name = "dashboard/advisories.html"
    context_object_name = "advisories"
    paginate_by = 50

    def get_queryset(self):
        qs = Advisory.objects.select_related("farm", "farm__zone").order_by("-generated_at")
        risk_level = self.request.GET.get("risk_level")
        advisory_type = self.request.GET.get("advisory_type")
        if risk_level:
            qs = qs.filter(risk_level=risk_level)
        if advisory_type:
            qs = qs.filter(advisory_type=advisory_type)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["risk_levels"] = Advisory.RiskLevel.choices
        context["advisory_types"] = Advisory.objects.values_list("advisory_type", flat=True).distinct()
        context["selected_risk_level"] = self.request.GET.get("risk_level", "")
        context["selected_advisory_type"] = self.request.GET.get("advisory_type", "")
        return context


class FarmOutcomeListView(StaffRequiredMixin, ListView):
    template_name = "dashboard/outcomes.html"
    context_object_name = "outcomes"
    paginate_by = 50

    def get_queryset(self):
        return FarmOutcome.objects.select_related("farm").order_by("-reported_at")
