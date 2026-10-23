from rest_framework.routers import DefaultRouter

from .views import FarmOutcomeViewSet, FarmViewSet

router = DefaultRouter()
router.register("farms", FarmViewSet, basename="farm")
router.register("farm-outcomes", FarmOutcomeViewSet, basename="farm-outcome")

urlpatterns = router.urls
