from django.core.management.base import BaseCommand
from solarflares.services import SolarFlareService


class Command(BaseCommand):
    help = 'Fetch solar flare data from NASA DONKI API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days to fetch (default: 30)'
        )

    def handle(self, *args, **options):
        days = options['days']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting to fetch solar flare data for the last {days} days...')
        )
        
        service = SolarFlareService()
        flares_created = service.fetch_solar_flares()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fetched {flares_created} solar flares')
        ) 