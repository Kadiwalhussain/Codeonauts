from django.contrib import admin
from .models import Asteroid, CloseApproach


class CloseApproachInline(admin.TabularInline):
    model = CloseApproach
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('close_approach_date', 'miss_distance_kilometers', 'relative_velocity_km_per_sec', 'orbiting_body')


@admin.register(Asteroid)
class AsteroidAdmin(admin.ModelAdmin):
    list_display = ('name', 'neo_reference_id', 'is_potentially_hazardous', 'is_sentry_object', 'created_at')
    list_filter = ('is_potentially_hazardous', 'is_sentry_object', 'created_at')
    search_fields = ('name', 'neo_reference_id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CloseApproachInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('neo_reference_id', 'name', 'nasa_jpl_url')
        }),
        ('Physical Properties', {
            'fields': ('absolute_magnitude_h', 'estimated_diameter_min', 'estimated_diameter_max')
        }),
        ('Classification', {
            'fields': ('is_potentially_hazardous', 'is_sentry_object')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual addition - Asteroids should come from API"""
        return False


@admin.register(CloseApproach)
class CloseApproachAdmin(admin.ModelAdmin):
    list_display = ('asteroid', 'close_approach_date', 'miss_distance_kilometers', 'relative_velocity_km_per_sec', 'orbiting_body')
    list_filter = ('orbiting_body', 'close_approach_date', 'created_at')
    search_fields = ('asteroid__name', 'asteroid__neo_reference_id')
    readonly_fields = ('created_at',)
    date_hierarchy = 'close_approach_date'
    
    fieldsets = (
        ('Approach Information', {
            'fields': ('asteroid', 'close_approach_date', 'orbiting_body')
        }),
        ('Distance Data', {
            'fields': ('miss_distance_astronomical', 'miss_distance_lunar', 'miss_distance_kilometers')
        }),
        ('Velocity Data', {
            'fields': ('relative_velocity_km_per_sec', 'relative_velocity_km_per_hour')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual addition - Close approaches should come from API"""
        return False
