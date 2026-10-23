from rest_framework import permissions, viewsets

from .models import Advisory, AdvisoryDelivery
from .serializers import AdvisoryDeliverySerializer, AdvisorySerializer


class AdvisoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Farmer-facing advisory feed - this is the core value-delivery
    endpoint the mobile app reads. Advisories are produced server-side by
    the rule-based/ML/Gen-AI pipeline, so this is read-only regardless of
    whether the caller owns the farm.
    """

    serializer_class = AdvisorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["farm", "advisory_type", "risk_level", "source"]

    def get_queryset(self):
        user = self.request.user
        qs = Advisory.objects.select_related("farm")
        if not user.is_staff:
            qs = qs.filter(farm__owner=user)
        return qs.order_by("-generated_at")


class AdvisoryDeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    """Per-channel send status (SMS/WhatsApp/app/USSD) - ops/debugging
    visibility, not something farmers need to see about their own
    advisories, so this is staff-only.
    """

    serializer_class = AdvisoryDeliverySerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ["advisory", "channel", "status"]
    queryset = AdvisoryDelivery.objects.select_related("advisory").order_by("-id")
