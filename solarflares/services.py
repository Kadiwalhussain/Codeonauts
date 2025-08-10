import requests
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
import pytz
from .models import SolarFlare

logger = logging.getLogger(__name__)


class SolarFlareService:
    """
    Service class to handle NASA DONKI API interactions for solar flares
    """
    BASE_URL = "https://api.nasa.gov/DONKI/FLR"
    
    def __init__(self, api_key=None):
        self.api_key = api_key or getattr(settings, 'NASA_API_KEY', 'DEMO_KEY')
    
    def fetch_solar_flares(self, start_date=None, end_date=None):
        """
        Fetch solar flare data for a date range
        """
        if start_date is None:
            start_date = timezone.now().date() - timedelta(days=30)
        if end_date is None:
            end_date = timezone.now().date()
        
        params = {
            'api_key': self.api_key,
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d')
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            flares_created = 0
            for flare_data in data:
                try:
                    flare = self._create_flare_from_data(flare_data)
                    if flare:
                        flares_created += 1
                except Exception as e:
                    logger.error(f"Error processing flare data: {e}")
                    continue
            
            logger.info(f"Successfully fetched and saved {flares_created} solar flares")
            return flares_created
            
        except requests.RequestException as e:
            logger.error(f"Error fetching solar flares: {e}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error processing solar flares: {e}")
            return 0
    
    def _create_flare_from_data(self, flare_data):
        """
        Create a SolarFlare object from API data
        """
        flare_id = flare_data.get('flrID')
        
        # Check if flare already exists
        if SolarFlare.objects.filter(flare_id=flare_id).exists():
            return None
        
        # Parse dates
        begin_time = self._parse_datetime(flare_data.get('beginTime'))
        peak_time = self._parse_datetime(flare_data.get('peakTime'))
        end_time = self._parse_datetime(flare_data.get('endTime'))
        
        if not all([begin_time, peak_time, end_time]):
            logger.warning(f"Missing time data for flare {flare_id}")
            return None
        
        # Extract flare class from classType
        class_type = flare_data.get('classType', '')
        flare_class = class_type[0] if class_type else 'A'
        
        # Create the flare
        flare = SolarFlare.objects.create(
            flare_id=flare_id,
            flare_class=flare_class,
            begin_time=begin_time,
            peak_time=peak_time,
            end_time=end_time,
            source_location=flare_data.get('sourceLocation', ''),
            active_region_num=flare_data.get('activeRegionNum', ''),
            linked_events=flare_data.get('linkedEvents', []),
            instruments=flare_data.get('instruments', [])
        )
        
        return flare
    
    def _parse_datetime(self, date_string):
        """
        Parse datetime string from NASA API format
        """
        if not date_string:
            return None
        
        try:
            # NASA API returns dates in format: "2024-01-15T10:30:00Z"
            return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
        except ValueError:
            try:
                # Try without timezone info
                return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.UTC)
            except ValueError:
                try:
                    # Try with just Z timezone indicator
                    return datetime.strptime(date_string, '%Y-%m-%dT%H:%MZ').replace(tzinfo=pytz.UTC)
                except ValueError:
                    logger.error(f"Could not parse datetime: {date_string}")
                    return None
    
    def get_recent_flares(self, days=7):
        """
        Get recent solar flares from database
        """
        start_date = timezone.now().date() - timedelta(days=days)
        return SolarFlare.objects.filter(
            peak_time__date__gte=start_date
        ).order_by('-peak_time')
    
    def get_flares_by_class(self, flare_class):
        """
        Get flares filtered by class
        """
        return SolarFlare.objects.filter(flare_class=flare_class).order_by('-peak_time') 