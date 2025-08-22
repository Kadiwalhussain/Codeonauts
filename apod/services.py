import requests
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from .models import APOD



logger = logging.getLogger(__name__)


class APODService:
    """
    Service class to handle NASA APOD API interactions
    """
    BASE_URL = "https://api.nasa.gov/planetary/apod"
    
    def __init__(self, api_key=None):
        self.api_key = api_key or getattr(settings, 'NASA_API_KEY', 'DEMO_KEY')
    
    def fetch_apod(self, date=None):
        """
        Fetch APOD data for a specific date or today
        """
        if date is None:
            date = timezone.now().date()
        
        # Check if we already have this APOD in our database
        try:
            existing_apod = APOD.objects.get(date=date)
            logger.info(f"APOD for {date} already exists in database")
            return existing_apod
        except APOD.DoesNotExist:
            pass
        
        # Fetch from NASA API
        params = {
            'api_key': self.api_key,
            'date': date.strftime('%Y-%m-%d')
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Create APOD object
            apod = APOD.objects.create(
                date=date,
                title=data.get('title', ''),
                explanation=data.get('explanation', ''),
                url=data.get('url', ''),
                media_type=data.get('media_type', 'image'),
                hdurl=data.get('hdurl', '')
            )
            
            logger.info(f"Successfully fetched and saved APOD for {date}")
            return apod
            
        except requests.RequestException as e:
            logger.error(f"Error fetching APOD for {date}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error processing APOD for {date}: {e}")
            return None
    
    def fetch_recent_apods(self, days=7):
        """
        Fetch APOD data for the last N days
        """
        apods = []
        for i in range(days):
            date = timezone.now().date() - timedelta(days=i)
            apod = self.fetch_apod(date)
            if apod:
                apods.append(apod)
        
        return apods
    
    def get_latest_apod(self):
        """
        Get the most recent APOD from database or fetch new one
        """
        try:
            latest = APOD.objects.latest('date')
            if latest.is_today:
                return latest
        except APOD.DoesNotExist:
            pass
        
        return self.fetch_apod() 