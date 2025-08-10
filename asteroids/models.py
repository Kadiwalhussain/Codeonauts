from django.db import models
from django.utils import timezone
import pytz


class Asteroid(models.Model):
    """
    Model to store NASA NeoWs API near-Earth asteroid data
    """
    neo_reference_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    nasa_jpl_url = models.URLField()
    absolute_magnitude_h = models.FloatField()
    estimated_diameter_min = models.FloatField(help_text="Estimated diameter in kilometers (min)")
    estimated_diameter_max = models.FloatField(help_text="Estimated diameter in kilometers (max)")
    is_potentially_hazardous = models.BooleanField(default=False)
    is_sentry_object = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Near-Earth Asteroid"
        verbose_name_plural = "Near-Earth Asteroids"

    def __str__(self):
        return f"{self.name} (ID: {self.neo_reference_id})"


class CloseApproach(models.Model):
    """
    Model to store close approach data for asteroids
    """
    asteroid = models.ForeignKey(Asteroid, on_delete=models.CASCADE, related_name='close_approaches')
    close_approach_date = models.DateTimeField()
    relative_velocity_km_per_sec = models.FloatField()
    relative_velocity_km_per_hour = models.FloatField()
    miss_distance_astronomical = models.FloatField()
    miss_distance_lunar = models.FloatField()
    miss_distance_kilometers = models.FloatField()
    orbiting_body = models.CharField(max_length=50, default='Earth')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['close_approach_date']
        verbose_name = "Close Approach"
        verbose_name_plural = "Close Approaches"
        unique_together = ['asteroid', 'close_approach_date']

    def __str__(self):
        return f"{self.asteroid.name} - {self.close_approach_date.strftime('%Y-%m-%d %H:%M')}"

    def get_local_time(self, timezone_name='UTC'):
        """Convert UTC time to local timezone"""
        utc = pytz.timezone('UTC')
        local_tz = pytz.timezone(timezone_name)
        return self.close_approach_date.replace(tzinfo=utc).astimezone(local_tz)

    @property
    def is_future(self):
        """Check if this approach is in the future"""
        return self.close_approach_date > timezone.now()

    @property
    def days_until_approach(self):
        """Calculate days until approach"""
        delta = self.close_approach_date - timezone.now()
        return delta.days
