from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import AgroecologicalZone
from .serializers import (
    AgroecologicalZoneDetailSerializer,
    AgroecologicalZoneListSerializer,
    WeatherObservationSerializer,
)

# Time series responses aren't paginated through DRF's standard list()
# machinery (this is a nested @action, not a top-level list endpoint), so
# cap the range directly to keep a single response bounded.
MAX_WEATHER_DAYS = 365


class AgroecologicalZoneViewSet(viewsets.ReadOnlyModelViewSet):
    """Reference zone data (currently Uganda districts - see apps/geodata/data).
    Read-only: zones are seeded via the load_zones management command, not
    created through the API.
    """

    queryset = AgroecologicalZone.objects.all().order_by("name")
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "code"
    filterset_fields = ["region"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AgroecologicalZoneDetailSerializer
        return AgroecologicalZoneListSerializer

    @action(detail=True, methods=["get"])
    def weather(self, request, code=None):
        """Rainfall/NDVI/temperature history for this zone.

        Optional ?from=YYYY-MM-DD&to=YYYY-MM-DD query params narrow the
        range; otherwise the most recent MAX_WEATHER_DAYS observations are
        returned.
        """
        zone = self.get_object()
        qs = zone.weather_observations.order_by("-observed_date")

        date_from = request.query_params.get("from")
        date_to = request.query_params.get("to")
        if date_from:
            qs = qs.filter(observed_date__gte=date_from)
        if date_to:
            qs = qs.filter(observed_date__lte=date_to)

        serializer = WeatherObservationSerializer(qs[:MAX_WEATHER_DAYS], many=True)
        return Response(serializer.data)
