from rest_framework import serializers

from apps.geodata.models import AgroecologicalZone

from .models import Farm, FarmOutcome


class FarmSerializer(serializers.ModelSerializer):
    # Zones are addressed by `code` everywhere else in the API (it's the
    # zone detail/weather endpoint's lookup_field, and the only identifier
    # AgroecologicalZoneListSerializer exposes) - using the same slug field
    # here instead of the numeric PK keeps one consistent identifier scheme
    # for zones across the whole API, rather than clients needing the PK in
    # one place and the code in another.
    zone = serializers.SlugRelatedField(slug_field="code", queryset=AgroecologicalZone.objects.all(), required=False, allow_null=True)
    zone_name = serializers.CharField(source="zone.name", read_only=True)

    class Meta:
        model = Farm
        fields = [
            "id",
            "name",
            "crop_type",
            "size_acres",
            "zone",
            "zone_name",
            "latitude",
            "longitude",
            "boundary_geojson",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        # owner is deliberately excluded here and set server-side from
        # request.user in the view - never accepted from the client, or a
        # caller could register a farm under someone else's account.


class FarmOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmOutcome
        fields = [
            "id",
            "farm",
            "season",
            "planted_date",
            "yield_kg_per_acre",
            "pest_incident_reported",
            "pest_notes",
            "reported_at",
        ]
        read_only_fields = ["id", "reported_at"]

    def validate_farm(self, farm):
        request = self.context["request"]
        if farm.owner_id != request.user.id and not request.user.is_staff:
            raise serializers.ValidationError("You can only report outcomes for your own farms.")
        return farm
