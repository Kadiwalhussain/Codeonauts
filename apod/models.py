from django.db import models
from django.utils import timezone


class APOD(models.Model):
    """
    Model to store NASA's Astronomy Picture of the Day data
    """
    date = models.DateField(unique=True)
    title = models.CharField(max_length=500)
    explanation = models.TextField()
    url = models.URLField()
    media_type = models.CharField(max_length=20)  # 'image' or 'video'
    hdurl = models.URLField(blank=True, null=True)  # High definition URL
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Astronomy Picture of the Day"
        verbose_name_plural = "Astronomy Pictures of the Day"

    def __str__(self):
        return f"{self.date} - {self.title}"

    @property
    def is_today(self):
        """Check if this APOD is from today"""
        return self.date == timezone.now().date()
