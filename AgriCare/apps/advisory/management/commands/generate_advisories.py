from django.core.management.base import BaseCommand

from apps.advisory.tasks import generate_advisories


class Command(BaseCommand):
    help = "Run rule-based advisory generation synchronously (no Celery worker needed)."

    def handle(self, *args, **options):
        result = generate_advisories()
        self.stdout.write(self.style.SUCCESS(str(result)))
