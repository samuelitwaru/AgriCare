from rest_framework import permissions, viewsets

from .models import Farm, FarmOutcome
from .serializers import FarmOutcomeSerializer, FarmSerializer


class FarmViewSet(viewsets.ModelViewSet):
    serializer_class = FarmSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Farm.objects.all().order_by("-created_at")
        return Farm.objects.filter(owner=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FarmOutcomeViewSet(viewsets.ModelViewSet):
    serializer_class = FarmOutcomeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["farm", "season"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return FarmOutcome.objects.all().order_by("-reported_at")
        return FarmOutcome.objects.filter(farm__owner=user).order_by("-reported_at")
