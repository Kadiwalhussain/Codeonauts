import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import SolarFlare
from .services import SolarFlareService


def solar_flares_home(request):
    """
    Display solar flares dashboard with visualizations
    """
    try:
        service = SolarFlareService()
        
        # Get recent flares
        recent_flares = service.get_recent_flares(days=30)
        
        # Create visualizations
        timeline_chart = create_flare_timeline(recent_flares)
        class_distribution = create_flare_class_distribution(recent_flares)
        
        context = {
            'recent_flares': recent_flares[:10],  # Show last 10 flares
            'timeline_chart': timeline_chart,
            'class_distribution': class_distribution,
            'total_flares': recent_flares.count(),
        }
        
    except Exception as e:
        context = {
            'recent_flares': [],
            'timeline_chart': None,
            'class_distribution': None,
            'total_flares': 0,
            'error_message': 'Unable to load solar flare data.',
        }
        messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'solarflares/home.html', context)


def solar_flares_list(request):
    """
    Display a list of all solar flares with filtering options
    """
    try:
        flares = SolarFlare.objects.all()
        
        # Filter by class if specified
        flare_class = request.GET.get('class')
        if flare_class:
            flares = flares.filter(flare_class=flare_class)
        
        # Filter by date range if specified
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date:
            flares = flares.filter(peak_time__date__gte=start_date)
        if end_date:
            flares = flares.filter(peak_time__date__lte=end_date)
        
        context = {
            'flares': flares[:50],  # Limit to 50 results
            'flare_classes': SolarFlare.FLARE_CLASS_CHOICES,
            'selected_class': flare_class,
            'start_date': start_date,
            'end_date': end_date,
        }
        
    except Exception as e:
        context = {
            'flares': [],
            'flare_classes': SolarFlare.FLARE_CLASS_CHOICES,
            'error_message': 'Unable to load solar flare list.',
        }
        messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'solarflares/list.html', context)


@require_http_methods(["POST"])
def refresh_solar_flares(request):
    """
    AJAX endpoint to refresh solar flare data
    """
    try:
        service = SolarFlareService()
        flares_created = service.fetch_solar_flares()
        
        return JsonResponse({
            'success': True,
            'flares_created': flares_created,
            'message': f'Successfully fetched {flares_created} new solar flares'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def create_flare_timeline(flares):
    """
    Create a timeline chart of solar flares using Plotly
    """
    if not flares:
        return None
    
    # Prepare data for timeline
    dates = [flare.peak_time for flare in flares]
    classes = [flare.flare_class for flare in flares]
    titles = [f"{flare.flare_class}-Class Flare" for flare in flares]
    
    # Color mapping for flare classes
    color_map = {
        'A': '#87CEEB',  # Light blue
        'B': '#98FB98',  # Light green
        'C': '#FFD700',  # Gold
        'M': '#FFA500',  # Orange
        'X': '#FF0000',  # Red
    }
    
    colors = [color_map.get(cls, '#808080') for cls in classes]
    
    # Create timeline chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=classes,
        mode='markers',
        marker=dict(
            size=15,
            color=colors,
            line=dict(width=2, color='black')
        ),
        text=titles,
        hovertemplate='<b>%{text}</b><br>' +
                     'Peak Time: %{x}<br>' +
                     'Class: %{y}<extra></extra>',
        name='Solar Flares'
    ))
    
    fig.update_layout(
        title='Solar Flare Timeline (Last 30 Days)',
        xaxis_title='Date',
        yaxis_title='Flare Class',
        yaxis=dict(
            categoryorder='array',
            categoryarray=['A', 'B', 'C', 'M', 'X']
        ),
        height=400,
        showlegend=False
    )
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)


def create_flare_class_distribution(flares):
    """
    Create a pie chart showing distribution of flare classes
    """
    if not flares:
        return None
    
    # Count flares by class
    class_counts = {}
    for flare in flares:
        class_counts[flare.flare_class] = class_counts.get(flare.flare_class, 0) + 1
    
    if not class_counts:
        return None
    
    # Prepare data for pie chart
    labels = list(class_counts.keys())
    values = list(class_counts.values())
    
    # Color mapping
    color_map = {
        'A': '#87CEEB',
        'B': '#98FB98',
        'C': '#FFD700',
        'M': '#FFA500',
        'X': '#FF0000',
    }
    
    colors = [color_map.get(label, '#808080') for label in labels]
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker_colors=colors
    )])
    
    fig.update_layout(
        title='Solar Flare Class Distribution',
        height=400,
        showlegend=True
    )
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)
