from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import APOD
from .services import APODService


def apod_home(request):
    """
    Display the Astronomy Picture of the Day
    """
    try:
        # Get or fetch the latest APOD
        service = APODService()
        apod = service.get_latest_apod()
        
        if apod:
            context = {
                'apod': apod,
                'is_image': apod.media_type == 'image',
                'is_video': apod.media_type == 'video',
            }
        else:
            # Fallback data if API fails
            context = {
                'apod': None,
                'error_message': 'Unable to fetch today\'s Astronomy Picture of the Day. Please try again later.',
            }
            messages.warning(request, 'Unable to fetch APOD data from NASA API.')
            
    except Exception as e:
        context = {
            'apod': None,
            'error_message': 'An error occurred while fetching the Astronomy Picture of the Day.',
        }
        messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'apod/home.html', context)


def apod_archive(request):
    """
    Display a list of recent APOD entries
    """
    try:
        # Get recent APODs from database
        recent_apods = APOD.objects.all()[:20]  # Last 20 entries
        
        context = {
            'apods': recent_apods,
        }
        
    except Exception as e:
        context = {
            'apods': [],
            'error_message': 'Unable to load APOD archive.',
        }
        messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'apod/archive.html', context)


@require_http_methods(["POST"])
def refresh_apod(request):
    """
    AJAX endpoint to refresh APOD data
    """
    try:
        service = APODService()
        apod = service.fetch_apod()  # Force fetch new data
        
        if apod:
            return JsonResponse({
                'success': True,
                'apod': {
                    'title': apod.title,
                    'explanation': apod.explanation,
                    'url': apod.url,
                    'media_type': apod.media_type,
                    'date': apod.date.strftime('%Y-%m-%d'),
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Unable to fetch APOD data'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def apod_detail(request, date):
    """
    Display a specific APOD by date
    """
    try:
        apod = APOD.objects.get(date=date)
        context = {
            'apod': apod,
            'is_image': apod.media_type == 'image',
            'is_video': apod.media_type == 'video',
        }
        
    except APOD.DoesNotExist:
        # Try to fetch from API
        service = APODService()
        apod = service.fetch_apod(date)
        
        if apod:
            context = {
                'apod': apod,
                'is_image': apod.media_type == 'image',
                'is_video': apod.media_type == 'video',
            }
        else:
            context = {
                'apod': None,
                'error_message': f'No APOD found for {date}',
            }
            messages.warning(request, f'No APOD found for {date}')
    
    return render(request, 'apod/detail.html', context)
