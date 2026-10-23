import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from apps.farms.models import Farm
from apps.geodata.models import AgroecologicalZone

from .models import Advisory
from .rules import evaluate_zone

logger = logging.getLogger(__name__)


def _should_create(farm, finding):
    """Skip creating a duplicate when the farm already has a current advisory
    of this type at the same risk level - only re-notify when the risk level
    has changed or the previous advisory has expired.
    """
    latest = Advisory.objects.filter(farm=farm, advisory_type=finding.advisory_type).order_by("-generated_at").first()
    if latest is None:
        return True
    if latest.valid_until and latest.valid_until < timezone.now():
        return True
    return latest.risk_level != finding.risk_level


@shared_task
def generate_advisories():
    """Evaluate rule-based findings per zone (see rules.py) and fan them out
    to every farm registered in that zone.
    """
    created, zones_with_findings = 0, 0

    for zone in AgroecologicalZone.objects.all():
        findings = evaluate_zone(zone)
        if not findings:
            continue
        zones_with_findings += 1

        for farm in Farm.objects.filter(zone=zone):
            for finding in findings:
                if not _should_create(farm, finding):
                    continue
                Advisory.objects.create(
                    farm=farm,
                    advisory_type=finding.advisory_type,
                    title=finding.title,
                    message=finding.message,
                    risk_level=finding.risk_level,
                    source=Advisory.Source.RULE_BASED,
                    valid_until=timezone.now() + timedelta(days=finding.validity_days),
                )
                created += 1

    return {"zones_with_findings": zones_with_findings, "advisories_created": created}
