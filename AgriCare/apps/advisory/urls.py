from rest_framework.routers import DefaultRouter

from .views import AdvisoryDeliveryViewSet, AdvisoryViewSet

router = DefaultRouter()
router.register("advisories", AdvisoryViewSet, basename="advisory")
router.register("advisory-deliveries", AdvisoryDeliveryViewSet, basename="advisory-delivery")

urlpatterns = router.urls
