from rest_framework import serializers

from .models import Advisory, AdvisoryDelivery


class AdvisorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisory
        fields = [
            "id",
            "farm",
            "advisory_type",
            "title",
            "message",
            "risk_level",
            "source",
            "generated_at",
            "valid_until",
        ]
        read_only_fields = fields  # generated server-side by the advisory pipeline, never submitted by clients


class AdvisoryDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvisoryDelivery
        fields = ["id", "advisory", "channel", "status", "sent_at", "error_message"]
        read_only_fields = fields
