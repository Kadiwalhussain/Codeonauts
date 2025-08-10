from django.contrib import admin
from .models import APOD


@admin.register(APOD)
class APODAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'media_type', 'created_at')
    list_filter = ('media_type', 'created_at', 'date')
    search_fields = ('title', 'explanation')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('date', 'title', 'explanation')
        }),
        ('Media', {
            'fields': ('media_type', 'url', 'hdurl')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual addition - APODs should come from API"""
        return False
