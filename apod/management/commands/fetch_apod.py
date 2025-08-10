from django.core.management.base import BaseCommand
from apod.services import APODService


class Command(BaseCommand):
    help = 'Fetch Astronomy Picture of the Day data from NASA API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days to fetch (default: 7)'
        )

    def handle(self, *args, **options):
        days = options['days']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting to fetch APOD data for the last {days} days...')
        )
        
        service = APODService()
        apods = service.fetch_recent_apods(days)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fetched {len(apods)} APOD entries')
        )
        
        for apod in apods:
            self.stdout.write(f'  - {apod.date}: {apod.title}') 