import requests
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
import pytz
from .models import Asteroid, CloseApproach

logger = logging.getLogger(__name__)


class AsteroidService:
    """
    Service class to handle NASA NeoWs API interactions
    """
    BASE_URL = "https://api.nasa.gov/neo/rest/v1"
    
    def __init__(self, api_key=None):
        self.api_key = api_key or getattr(settings, 'NASA_API_KEY', 'DEMO_KEY')
    
    def fetch_asteroids(self, start_date=None, end_date=None):
        """
        Fetch near-Earth asteroids for a date range
        """
        if start_date is None:
            start_date = timezone.now().date()
        if end_date is None:
            end_date = start_date + timedelta(days=7)
        
        params = {
            'api_key': self.api_key,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }
        
        try:
            response = requests.get(f"{self.BASE_URL}/feed", params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            asteroids_created = 0
            approaches_created = 0
            
            for date_str, asteroids_data in data.get('near_earth_objects', {}).items():
                for asteroid_data in asteroids_data:
                    try:
                        asteroid, approaches = self._create_asteroid_from_data(asteroid_data, date_str)
                        if asteroid:
                            asteroids_created += 1
                            approaches_created += len(approaches)
                    except Exception as e:
                        logger.error(f"Error processing asteroid data: {e}")
                        continue
            
            logger.info(f"Successfully fetched and saved {asteroids_created} asteroids with {approaches_created} approaches")
            return asteroids_created
            
        except requests.RequestException as e:
            logger.error(f"Error fetching asteroids: {e}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error processing asteroids: {e}")
            return 0
    
    def _create_asteroid_from_data(self, asteroid_data, date_str):
        """
        Create Asteroid and CloseApproach objects from API data
        """
        neo_id = asteroid_data.get('neo_reference_id')
        
        # Check if asteroid already exists
        asteroid, created = Asteroid.objects.get_or_create(
            neo_reference_id=neo_id,
            defaults={
                'name': asteroid_data.get('name', ''),
                'nasa_jpl_url': asteroid_data.get('nasa_jpl_url', ''),
                'absolute_magnitude_h': asteroid_data.get('absolute_magnitude_h', 0.0),
                'estimated_diameter_min': self._get_diameter_min(asteroid_data),
                'estimated_diameter_max': self._get_diameter_max(asteroid_data),
                'is_potentially_hazardous': asteroid_data.get('is_potentially_hazardous_asteroid', False),
                'is_sentry_object': asteroid_data.get('is_sentry_object', False),
            }
        )
        
        # Process close approaches
        approaches = []
        for approach_data in asteroid_data.get('close_approach_data', []):
            try:
                approach = self._create_approach_from_data(asteroid, approach_data)
                if approach:
                    approaches.append(approach)
            except Exception as e:
                logger.error(f"Error processing approach data: {e}")
                continue
        
        return asteroid, approaches
    
    def _create_approach_from_data(self, asteroid, approach_data):
        """
        Create CloseApproach object from API data
        """
        approach_date = self._parse_datetime(approach_data.get('close_approach_date_full'))
        if not approach_date:
            return None
        
        # Check if approach already exists
        if CloseApproach.objects.filter(
            asteroid=asteroid,
            close_approach_date=approach_date
        ).exists():
            return None
        
        # Extract velocity data
        relative_velocity = approach_data.get('relative_velocity', {})
        miss_distance = approach_data.get('miss_distance', {})
        
        approach = CloseApproach.objects.create(
            asteroid=asteroid,
            close_approach_date=approach_date,
            relative_velocity_km_per_sec=float(relative_velocity.get('kilometers_per_second', 0)),
            relative_velocity_km_per_hour=float(relative_velocity.get('kilometers_per_hour', 0)),
            miss_distance_astronomical=float(miss_distance.get('astronomical', 0)),
            miss_distance_lunar=float(miss_distance.get('lunar', 0)),
            miss_distance_kilometers=float(miss_distance.get('kilometers', 0)),
            orbiting_body=approach_data.get('orbiting_body', 'Earth')
        )
        
        return approach
    
    def _get_diameter_min(self, asteroid_data):
        """Extract minimum diameter from asteroid data"""
        diameter_data = asteroid_data.get('estimated_diameter', {}).get('kilometers', {})
        return diameter_data.get('estimated_diameter_min', 0.0)
    
    def _get_diameter_max(self, asteroid_data):
        """Extract maximum diameter from asteroid data"""
        diameter_data = asteroid_data.get('estimated_diameter', {}).get('kilometers', {})
        return diameter_data.get('estimated_diameter_max', 0.0)
    
    def _parse_datetime(self, date_string):
        """
        Parse datetime string from NASA API format
        """
        if not date_string:
            return None
        
        try:
            # NASA API returns dates in format: "2024-01-15 10:30:00"
            return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
        except ValueError:
            try:
                # Try format: "2025-Aug-10 09:08"
                return datetime.strptime(date_string, '%Y-%b-%d %H:%M').replace(tzinfo=pytz.UTC)
            except ValueError:
                logger.error(f"Could not parse datetime: {date_string}")
                return None
    
    def get_recent_approaches(self, days=30):
        """
        Get recent close approaches from database
        """
        start_date = timezone.now().date() - timedelta(days=days)
        return CloseApproach.objects.filter(
            close_approach_date__date__gte=start_date
        ).select_related('asteroid').order_by('close_approach_date')
    
    def get_hazardous_asteroids(self):
        """
        Get potentially hazardous asteroids
        """
        return Asteroid.objects.filter(
            is_potentially_hazardous=True
        ).order_by('-created_at')
    
    def get_upcoming_approaches(self, days=7):
        """
        Get upcoming close approaches
        """
        end_date = timezone.now().date() + timedelta(days=days)
        return CloseApproach.objects.filter(
            close_approach_date__date__gte=timezone.now().date(),
            close_approach_date__date__lte=end_date
        ).select_related('asteroid').order_by('close_approach_date') 