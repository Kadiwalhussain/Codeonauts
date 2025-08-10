from django.core.management.base import BaseCommand
from asteroids.services import AsteroidService


class Command(BaseCommand):
    help = 'Fetch near-Earth asteroid data from NASA NeoWs API'

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
            self.style.SUCCESS(f'Starting to fetch asteroid data for the next {days} days...')
        )
        
        service = AsteroidService()
        asteroids_created = service.fetch_asteroids()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fetched {asteroids_created} asteroids')
        ) 