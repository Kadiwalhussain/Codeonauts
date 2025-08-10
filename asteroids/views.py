import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Asteroid, CloseApproach
from .services import AsteroidService
from django.utils import timezone


def asteroids_home(request):
    """
    Display asteroids dashboard with visualizations
    """
    try:
        service = AsteroidService()
        
        # Get recent approaches and hazardous asteroids
        recent_approaches = service.get_recent_approaches(days=30)
        hazardous_asteroids = service.get_hazardous_asteroids()
        upcoming_approaches = service.get_upcoming_approaches(days=7)
        
        # Create visualizations
        scatter_chart = create_asteroid_scatter(recent_approaches)
        distance_chart = create_distance_timeline(upcoming_approaches)
        
        context = {
            'recent_approaches': recent_approaches[:10],  # Show last 10 approaches
            'hazardous_asteroids': hazardous_asteroids[:5],  # Show top 5 hazardous
            'upcoming_approaches': upcoming_approaches[:5],  # Show next 5 approaches
            'scatter_chart': scatter_chart,
            'distance_chart': distance_chart,
            'total_asteroids': Asteroid.objects.count(),
            'total_approaches': CloseApproach.objects.count(),
            'hazardous_count': hazardous_asteroids.count(),
        }
        
    except Exception as e:
        context = {
            'recent_approaches': [],
            'hazardous_asteroids': [],
            'upcoming_approaches': [],
            'scatter_chart': None,
            'distance_chart': None,
            'total_asteroids': 0,
            'total_approaches': 0,
            'hazardous_count': 0,
            'error_message': 'Unable to load asteroid data.',
        }
        messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'asteroids/home.html', context)


def asteroids_list(request):
    """
    Display a list of all asteroids with filtering options
    """
    try:
        asteroids = Asteroid.objects.all()
        
        # Filter by hazardous status
        hazardous_only = request.GET.get('hazardous')
        if hazardous_only == 'true':
            asteroids = asteroids.filter(is_potentially_hazardous=True)
        
        # Filter by sentry status
        sentry_only = request.GET.get('sentry')
        if sentry_only == 'true':
            asteroids = asteroids.filter(is_sentry_object=True)
        
        context = {
            'asteroids': asteroids[:50],  # Limit to 50 results
            'hazardous_only': hazardous_only == 'true',
            'sentry_only': sentry_only == 'true',
        }
        
    except Exception as e:
        context = {
            'asteroids': [],
            'error_message': 'Unable to load asteroid list.',
        }
        messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'asteroids/list.html', context)


def approaches_list(request):
    """
    Display a list of close approaches
    """
    try:
        approaches = CloseApproach.objects.select_related('asteroid').all()
        
        # Filter by future/past approaches
        future_only = request.GET.get('future')
        if future_only == 'true':
            approaches = approaches.filter(close_approach_date__gte=timezone.now())
        
        context = {
            'approaches': approaches[:50],  # Limit to 50 results
            'future_only': future_only == 'true',
        }
        
    except Exception as e:
        context = {
            'approaches': [],
            'error_message': 'Unable to load close approaches.',
        }
        messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'asteroids/approaches.html', context)


@require_http_methods(["POST"])
def refresh_asteroids(request):
    """
    AJAX endpoint to refresh asteroid data
    """
    try:
        service = AsteroidService()
        asteroids_created = service.fetch_asteroids()
        
        return JsonResponse({
            'success': True,
            'asteroids_created': asteroids_created,
            'message': f'Successfully fetched {asteroids_created} new asteroids'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def create_asteroid_scatter(approaches):
    """
    Create a scatter plot of asteroid approaches using Plotly
    """
    if not approaches:
        return None
    
    # Prepare data for scatter plot
    distances = [approach.miss_distance_kilometers for approach in approaches]
    velocities = [approach.relative_velocity_km_per_sec for approach in approaches]
    names = [approach.asteroid.name for approach in approaches]
    hazardous = [approach.asteroid.is_potentially_hazardous for approach in approaches]
    
    # Color based on hazardous status
    colors = ['red' if h else 'blue' for h in hazardous]
    
    # Create scatter plot
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=distances,
        y=velocities,
        mode='markers',
        marker=dict(
            size=10,
            color=colors,
            opacity=0.7
        ),
        text=names,
        hovertemplate='<b>%{text}</b><br>' +
                     'Distance: %{x:,.0f} km<br>' +
                     'Velocity: %{y:.2f} km/s<extra></extra>',
        name='Asteroid Approaches'
    ))
    
    fig.update_layout(
        title='Asteroid Close Approaches: Distance vs Velocity',
        xaxis_title='Miss Distance (km)',
        yaxis_title='Relative Velocity (km/s)',
        height=400,
        showlegend=False
    )
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)


def create_distance_timeline(approaches):
    """
    Create a timeline chart of upcoming close approaches
    """
    if not approaches:
        return None
    
    # Prepare data for timeline
    dates = [approach.close_approach_date for approach in approaches]
    distances = [approach.miss_distance_lunar for approach in approaches]  # In lunar distances
    names = [approach.asteroid.name for approach in approaches]
    hazardous = [approach.asteroid.is_potentially_hazardous for approach in approaches]
    
    # Color based on hazardous status
    colors = ['red' if h else 'blue' for h in hazardous]
    
    # Create timeline chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=distances,
        mode='markers+lines',
        marker=dict(
            size=12,
            color=colors,
            line=dict(width=2, color='black')
        ),
        line=dict(color='gray', width=1),
        text=names,
        hovertemplate='<b>%{text}</b><br>' +
                     'Date: %{x}<br>' +
                     'Distance: %{y:.2f} lunar distances<extra></extra>',
        name='Upcoming Approaches'
    ))
    
    fig.update_layout(
        title='Upcoming Asteroid Close Approaches',
        xaxis_title='Date',
        yaxis_title='Miss Distance (Lunar Distances)',
        height=400,
        showlegend=False
    )
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)
