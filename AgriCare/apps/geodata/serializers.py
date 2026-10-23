from rest_framework import serializers

from .models import AgroecologicalZone, WeatherObservation


class AgroecologicalZoneListSerializer(serializers.ModelSerializer):
    """Lightweight - excludes boundary_geojson, which would bloat a list of
    135 zones into a multi-hundred-KB response for no reason on a list view.
    """

    class Meta:
        model = AgroecologicalZone
        fields = ["code", "name", "region", "description"]


class AgroecologicalZoneDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgroecologicalZone
        fields = ["code", "name", "region", "description", "boundary_geojson"]


class WeatherObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherObservation
        fields = ["observed_date", "rainfall_mm", "temperature_c", "ndvi", "updated_at"]
