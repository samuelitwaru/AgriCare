from django.core.management.base import BaseCommand

from apps.geodata.tasks import ingest_ndvi


class Command(BaseCommand):
    help = (
        "Run the NDVI ingestion synchronously (no Celery worker needed). "
        "Pulls the most recent MODIS MOD13Q1 composite available."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=str,
            default=None,
            help="Search backward from this date (YYYY-MM-DD). Defaults to 5 days before today.",
        )

    def handle(self, *args, **options):
        result = ingest_ndvi(target_date=options["date"])
        self.stdout.write(self.style.SUCCESS(str(result)))
