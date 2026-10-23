from django.db import models

from apps.farms.models import Farm


class Advisory(models.Model):
    class Source(models.TextChoices):
        RULE_BASED = "rule_based", "Rule-based"
        ML_MODEL = "ml_model", "ML Model"
        GEN_AI = "gen_ai", "Gen-AI"

    class RiskLevel(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="advisories")
    advisory_type = models.CharField(max_length=64)  # e.g. planting_date, drought_risk, pest_alert
    title = models.CharField(max_length=255)
    message = models.TextField()
    risk_level = models.CharField(max_length=16, choices=RiskLevel.choices, default=RiskLevel.LOW)
    source = models.CharField(max_length=16, choices=Source.choices, default=Source.RULE_BASED)
    generated_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.advisory_type} - {self.farm}"


class AdvisoryDelivery(models.Model):
    class Channel(models.TextChoices):
        APP = "app", "Mobile App"
        SMS = "sms", "SMS"
        WHATSAPP = "whatsapp", "WhatsApp"
        USSD = "ussd", "USSD"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    advisory = models.ForeignKey(Advisory, on_delete=models.CASCADE, related_name="deliveries")
    channel = models.CharField(max_length=16, choices=Channel.choices)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.advisory_id} via {self.channel} ({self.status})"
