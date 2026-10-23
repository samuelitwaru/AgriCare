from django.core.management.base import BaseCommand

from apps.geodata.tasks import ingest_chirps_rainfall


class Command(BaseCommand):
    help = (
        "Run the CHIRPS rainfall ingestion synchronously (no Celery worker needed). "
        "Useful for local testing once zones have real boundaries and Earth Engine "
        "credentials are configured in .env."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=str,
            default=None,
            help="Target date as YYYY-MM-DD. Defaults to 5 days before today (CHIRPS latency buffer).",
        )

    def handle(self, *args, **options):
        result = ingest_chirps_rainfall(target_date=options["date"])
        self.stdout.write(self.style.SUCCESS(str(result)))
