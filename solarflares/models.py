from django.db import models
from django.utils import timezone
import pytz


class SolarFlare(models.Model):
    """
    Model to store NASA DONKI API solar flare data
    """
    FLARE_CLASS_CHOICES = [
        ('A', 'A-Class'),
        ('B', 'B-Class'),
        ('C', 'C-Class'),
        ('M', 'M-Class'),
        ('X', 'X-Class'),
    ]

    flare_id = models.CharField(max_length=100, unique=True)
    flare_class = models.CharField(max_length=1, choices=FLARE_CLASS_CHOICES)
    begin_time = models.DateTimeField()
    peak_time = models.DateTimeField()
    end_time = models.DateTimeField()
    source_location = models.CharField(max_length=200, blank=True)
    active_region_num = models.CharField(max_length=50, blank=True)
    linked_events = models.JSONField(default=list, blank=True)
    instruments = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-peak_time']
        verbose_name = "Solar Flare"
        verbose_name_plural = "Solar Flares"

    def __str__(self):
        return f"{self.flare_class}-Class Flare on {self.peak_time.strftime('%Y-%m-%d %H:%M')}"

    @property
    def intensity_value(self):
        """Get numeric intensity value for sorting"""
        intensity_map = {'A': 1, 'B': 2, 'C': 3, 'M': 4, 'X': 5}
        return intensity_map.get(self.flare_class, 0)

    def get_local_time(self, timezone_name='UTC'):
        """Convert UTC time to local timezone"""
        utc = pytz.timezone('UTC')
        local_tz = pytz.timezone(timezone_name)
        return self.peak_time.replace(tzinfo=utc).astimezone(local_tz)
