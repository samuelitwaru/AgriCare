import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.geodata.models import AgroecologicalZone


class Command(BaseCommand):
    help = (
        "Load or update AgroecologicalZone records from a GeoJSON FeatureCollection. "
        "Each feature's properties must include 'code' and 'name'; 'region' and "
        "'description' are optional. The feature geometry is stored as boundary_geojson. "
        "Safe to re-run: zones are matched and updated by 'code'."
    )

    def add_arguments(self, parser):
        parser.add_argument("geojson_path", type=str, help="Path to a GeoJSON FeatureCollection file")

    def handle(self, *args, **options):
        path = Path(options["geojson_path"])
        if not path.exists():
            raise CommandError(f"File not found: {path}")

        data = json.loads(path.read_text())
        features = data.get("features", [])
        if not features:
            raise CommandError("No features found in GeoJSON file")

        created, updated, skipped = 0, 0, 0
        for feature in features:
            props = feature.get("properties", {})
            code = props.get("code")
            name = props.get("name")
            if not code or not name:
                self.stderr.write(self.style.WARNING(f"Skipping feature missing 'code' or 'name': {props}"))
                skipped += 1
                continue

            zone, was_created = AgroecologicalZone.objects.update_or_create(
                code=code,
                defaults={
                    "name": name,
                    "region": props.get("region", ""),
                    "description": props.get("description", ""),
                    "boundary_geojson": feature.get("geometry"),
                },
            )
            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(
            self.style.SUCCESS(f"Zones loaded: {created} created, {updated} updated, {skipped} skipped.")
        )
