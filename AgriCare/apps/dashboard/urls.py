from django.urls import path

from .views import (
    AdvisoryListView,
    DashboardLoginView,
    DashboardLogoutView,
    FarmListView,
    FarmOutcomeListView,
    HomeView,
    ZoneListView,
)

app_name = "dashboard"

urlpatterns = [
    path("login/", DashboardLoginView.as_view(), name="login"),
    path("logout/", DashboardLogoutView.as_view(), name="logout"),
    path("", HomeView.as_view(), name="home"),
    path("zones/", ZoneListView.as_view(), name="zones"),
    path("farms/", FarmListView.as_view(), name="farms"),
    path("advisories/", AdvisoryListView.as_view(), name="advisories"),
    path("outcomes/", FarmOutcomeListView.as_view(), name="outcomes"),
]
