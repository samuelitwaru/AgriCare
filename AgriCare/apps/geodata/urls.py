from rest_framework.routers import DefaultRouter

from .views import AgroecologicalZoneViewSet

router = DefaultRouter()
router.register("zones", AgroecologicalZoneViewSet, basename="zone")

urlpatterns = router.urls
