# Space Weather Dashboard - Technical Documentation

## 🏗️ Architecture Overview

The Space Weather Dashboard is built using modern web technologies with a focus on performance, scalability, and user experience. The application follows the Model-View-Template (MVT) pattern using Django framework.

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  HTML5 Templates │ CSS3 Styling │ JavaScript │ Bootstrap 5     │
├─────────────────────────────────────────────────────────────────┤
│                      Django Framework                          │
├─────────────────────────────────────────────────────────────────┤
│   Views Layer    │  Models Layer  │  Services Layer           │
├─────────────────────────────────────────────────────────────────┤
│                    Data Integration                            │
├─────────────────────────────────────────────────────────────────┤
│  NASA APOD API   │  DONKI API    │  NeoWs API                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Backend Technologies
- **Framework**: Django 5.1.1 (Python web framework)
- **Language**: Python 3.13+
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **API Integration**: Python Requests library
- **Task Scheduling**: Django management commands
- **Caching**: Django cache framework

### Frontend Technologies
- **HTML**: HTML5 with semantic markup
- **CSS**: CSS3 with modern features (Grid, Flexbox, Custom Properties)
- **JavaScript**: Vanilla ES6+ for interactivity
- **Framework**: Bootstrap 5.3.0 for responsive design
- **Icons**: Font Awesome 6.0.0
- **Charts**: Plotly.js for data visualization

### Development Tools
- **Version Control**: Git
- **Package Management**: pip (Python)
- **Environment Management**: Virtual environments
- **Code Quality**: Django best practices
- **Testing**: Django testing framework

## 📁 Project Structure

```
Space/
│
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── db.sqlite3                        # SQLite database
├── README.md                         # Project overview
├── PROJECT_SUMMARY.md               # Project summary
│
├── space_weather_dashboard/          # Main project configuration
│   ├── __init__.py
│   ├── settings.py                   # Django settings
│   ├── urls.py                      # URL routing
│   ├── wsgi.py                      # WSGI configuration
│   └── asgi.py                      # ASGI configuration
│
├── apod/                            # APOD application
│   ├── models.py                    # Data models
│   ├── views.py                     # View functions
│   ├── urls.py                      # URL patterns
│   ├── services.py                  # API services
│   ├── admin.py                     # Admin configuration
│   ├── apps.py                      # App configuration
│   ├── tests.py                     # Unit tests
│   ├── management/commands/         # Management commands
│   │   └── fetch_apod.py           # APOD data fetching
│   └── migrations/                  # Database migrations
│
├── solarflares/                     # Solar flares application
│   ├── models.py                    # Flare data models
│   ├── views.py                     # Flare views
│   ├── urls.py                      # URL patterns
│   ├── services.py                  # DONKI API services
│   ├── management/commands/         # Management commands
│   │   └── fetch_solar_flares.py   # Flare data fetching
│   └── migrations/                  # Database migrations
│
├── asteroids/                       # Asteroids application
│   ├── models.py                    # Asteroid data models
│   ├── views.py                     # Asteroid views
│   ├── urls.py                      # URL patterns
│   ├── services.py                  # NeoWs API services
│   ├── management/commands/         # Management commands
│   │   └── fetch_asteroids.py      # Asteroid data fetching
│   └── migrations/                  # Database migrations
│
├── templates/                       # HTML templates
│   ├── base.html                    # Base template
│   ├── apod/                        # APOD templates
│   ├── solarflares/                 # Solar flare templates
│   └── asteroids/                   # Asteroid templates
│
├── static/                          # Static files
│   ├── css/                         # Stylesheets
│   │   ├── custom.css              # Main custom styles
│   │   ├── space-animations.css    # Animation effects
│   │   └── utilities.css           # Utility classes
│   └── js/                         # JavaScript files
│
└── docs/                           # Documentation
    ├── APOD_Guide.md               # APOD documentation
    ├── Website_Information.md      # Website info guide
    └── Technical_Documentation.md  # This file
```

## 💾 Database Schema

### APOD Application Models

```python
class APODEntry(models.Model):
    date = models.DateField(unique=True)
    title = models.CharField(max_length=255)
    explanation = models.TextField()
    url = models.URLField()
    hdurl = models.URLField(blank=True, null=True)
    media_type = models.CharField(max_length=20)
    copyright = models.CharField(max_length=255, blank=True, null=True)
    service_version = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Solar Flares Application Models

```python
class SolarFlare(models.Model):
    flare_id = models.CharField(max_length=100, unique=True)
    flr_id = models.CharField(max_length=50)
    instruments = models.JSONField()
    begin_time = models.DateTimeField()
    peak_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    class_type = models.CharField(max_length=10)
    source_location = models.CharField(max_length=50, blank=True)
    active_region_num = models.IntegerField(null=True, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Asteroids Application Models

```python
class Asteroid(models.Model):
    neo_reference_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    nasa_jpl_url = models.URLField()
    absolute_magnitude_h = models.FloatField()
    is_potentially_hazardous = models.BooleanField()
    estimated_diameter_km_min = models.FloatField()
    estimated_diameter_km_max = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CloseApproachData(models.Model):
    asteroid = models.ForeignKey(Asteroid, on_delete=models.CASCADE)
    close_approach_date = models.DateField()
    close_approach_date_full = models.DateTimeField()
    epoch_date_close_approach = models.BigIntegerField()
    relative_velocity_kms = models.FloatField()
    relative_velocity_kmh = models.FloatField()
    miss_distance_astronomical = models.FloatField()
    miss_distance_lunar = models.FloatField()
    miss_distance_kilometers = models.FloatField()
    miss_distance_miles = models.FloatField()
    orbiting_body = models.CharField(max_length=20)
```

## 🔌 API Integration

### NASA API Services

#### APOD Service (`apod/services.py`)
```python
class APODService:
    BASE_URL = "https://api.nasa.gov/planetary/apod"
    
    @classmethod
    def fetch_apod(cls, date=None):
        """Fetch APOD data for specific date or today"""
        params = {
            'api_key': settings.NASA_API_KEY,
            'date': date or timezone.now().date()
        }
        response = requests.get(cls.BASE_URL, params=params)
        return response.json()
```

#### Solar Flares Service (`solarflares/services.py`)
```python
class SolarFlaresService:
    BASE_URL = "https://api.nasa.gov/DONKI/FLR"
    
    @classmethod
    def fetch_solar_flares(cls, start_date, end_date):
        """Fetch solar flare data for date range"""
        params = {
            'api_key': settings.NASA_API_KEY,
            'startDate': start_date,
            'endDate': end_date
        }
        response = requests.get(cls.BASE_URL, params=params)
        return response.json()
```

#### Asteroids Service (`asteroids/services.py`)
```python
class AsteroidService:
    BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"
    
    @classmethod
    def fetch_asteroids(cls, start_date, end_date):
        """Fetch asteroid data for date range"""
        params = {
            'api_key': settings.NASA_API_KEY,
            'start_date': start_date,
            'end_date': end_date
        }
        response = requests.get(cls.BASE_URL, params=params)
        return response.json()
```

### Error Handling

All API services implement robust error handling:
- **Network Errors**: Connection timeouts and retries
- **API Limits**: Rate limiting and quota management
- **Data Validation**: Input sanitization and output validation
- **Graceful Degradation**: Fallback to cached data when APIs are unavailable

## 🎨 Frontend Implementation

### CSS Architecture

The stylesheet architecture follows a modular approach:

1. **custom.css**: Core styling and CSS variables
2. **space-animations.css**: Animation effects and interactions
3. **utilities.css**: Utility classes and accessibility features

#### CSS Custom Properties
```css
:root {
    --primary-bg: #0a0a0f;
    --secondary-bg: #151520;
    --accent-bg: #1e1e2e;
    --card-bg: #232338;
    --primary-text: #e8e8f0;
    --secondary-text: #b4b4c8;
    --accent-color: #4fc3f7;
    --accent-hover: #29b6f6;
    --glass-bg: rgba(35, 35, 56, 0.8);
    --glass-border: rgba(79, 195, 247, 0.2);
}
```

### JavaScript Implementation

#### AJAX Data Loading
```javascript
async function refreshAPOD() {
    try {
        showLoading('loading');
        const response = await fetch('/apod/api/refresh/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            location.reload();
        } else {
            showAlert('Failed to refresh APOD data', 'danger');
        }
    } catch (error) {
        showAlert('Network error occurred', 'danger');
    } finally {
        hideLoading('loading');
    }
}
```

#### Chart Visualization
```javascript
function createSolarFlareChart(data) {
    const trace = {
        x: data.dates,
        y: data.intensities,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Solar Flares'
    };
    
    const layout = {
        title: 'Solar Flare Activity',
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#e8e8f0' }
    };
    
    Plotly.newPlot('flare-chart', [trace], layout);
}
```

## 📊 Data Processing

### Management Commands

Each application includes management commands for data fetching:

#### APOD Data Fetching
```bash
python manage.py fetch_apod --date=2025-08-10
python manage.py fetch_apod --days=7  # Last 7 days
```

#### Solar Flares Data Fetching
```bash
python manage.py fetch_solar_flares --days=30
python manage.py fetch_solar_flares --start=2025-08-01 --end=2025-08-10
```

#### Asteroid Data Fetching
```bash
python manage.py fetch_asteroids --days=7
python manage.py fetch_asteroids --start=2025-08-10 --end=2025-08-17
```

### Data Validation and Cleaning

All incoming data goes through validation:
- **Schema Validation**: Ensure data matches expected structure
- **Date Validation**: Verify date formats and ranges
- **URL Validation**: Check image and video URLs
- **Duplicate Prevention**: Avoid storing duplicate entries

## 🔒 Security Considerations

### API Security
- **API Key Management**: Secure storage of NASA API keys
- **Rate Limiting**: Respect NASA API usage limits
- **Input Sanitization**: Clean all user inputs
- **CSRF Protection**: Django CSRF tokens for form submissions

### Data Security
- **SQL Injection Prevention**: Django ORM protection
- **XSS Prevention**: Template auto-escaping
- **Content Security Policy**: Secure content loading
- **HTTPS**: Secure data transmission

## 📈 Performance Optimization

### Caching Strategy
- **API Response Caching**: Cache NASA API responses
- **Template Caching**: Cache rendered templates
- **Static File Optimization**: Compress CSS and JavaScript
- **Image Optimization**: Lazy loading and compression

### Database Optimization
- **Indexing**: Proper database indexes on frequently queried fields
- **Query Optimization**: Efficient database queries
- **Connection Pooling**: Efficient database connections
- **Migration Management**: Proper schema changes

## 🧪 Testing

### Unit Tests
Each application includes comprehensive unit tests:
- **Model Tests**: Data model functionality
- **View Tests**: HTTP response testing
- **Service Tests**: API integration testing
- **Form Tests**: Input validation testing

### Integration Tests
- **End-to-End Testing**: Complete user workflows
- **API Integration Testing**: External API interactions
- **Browser Testing**: Cross-browser compatibility
- **Performance Testing**: Load and stress testing

## 🚀 Deployment

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd Space

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Production Deployment
- **Web Server**: Nginx or Apache
- **WSGI Server**: Gunicorn or uWSGI
- **Database**: PostgreSQL or MySQL
- **Static Files**: CDN or web server serving
- **SSL Certificate**: HTTPS encryption
- **Environment Variables**: Secure configuration management

### Environment Variables
```bash
# Required environment variables
NASA_API_KEY=your_nasa_api_key_here
SECRET_KEY=your_django_secret_key_here
DEBUG=False
DATABASE_URL=your_database_connection_string
```

## 📋 Maintenance

### Regular Tasks
- **Data Updates**: Scheduled API data fetching
- **Database Maintenance**: Regular database optimization
- **Security Updates**: Keep dependencies updated
- **Monitoring**: Application performance monitoring
- **Backup**: Regular data backups

### Monitoring and Logging
- **Application Logs**: Django logging framework
- **Error Tracking**: Exception monitoring
- **Performance Metrics**: Response time tracking
- **API Usage Monitoring**: NASA API quota tracking

---

*This technical documentation provides a comprehensive overview of the Space Weather Dashboard's architecture, implementation details, and operational considerations for developers and system administrators.*
