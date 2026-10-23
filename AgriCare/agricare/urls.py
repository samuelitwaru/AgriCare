from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(request):
    return JsonResponse({"status": "ok", "service": "agricare"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health-check"),
    path("api/v1/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.farms.urls")),
    path("api/v1/", include("apps.geodata.urls")),
    path("api/v1/", include("apps.advisory.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
]
