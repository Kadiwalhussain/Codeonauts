from django.contrib import admin
from .models import SolarFlare


@admin.register(SolarFlare)
class SolarFlareAdmin(admin.ModelAdmin):
    list_display = ('flare_id', 'flare_class', 'peak_time', 'source_location', 'created_at')
    list_filter = ('flare_class', 'created_at', 'peak_time')
    search_fields = ('flare_id', 'source_location', 'active_region_num')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'peak_time'
    
    fieldsets = (
        ('Flare Information', {
            'fields': ('flare_id', 'flare_class', 'source_location', 'active_region_num')
        }),
        ('Timing', {
            'fields': ('begin_time', 'peak_time', 'end_time')
        }),
        ('Additional Data', {
            'fields': ('linked_events', 'instruments'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual addition - Solar flares should come from API"""
        return False
