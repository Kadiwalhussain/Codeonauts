# NASA APIs Integration Guide - Space Weather Dashboard

## 🛰️ Overview

This document provides comprehensive information about the NASA APIs integrated into our Space Weather Dashboard, including their capabilities, data formats, usage patterns, and integration details.

## 🌌 NASA API Ecosystem

NASA provides a rich ecosystem of APIs that give public access to a vast collection of NASA data, including imagery, climate data, and space weather information. Our dashboard integrates with three primary APIs:

### API Access Requirements
- **API Key**: Required for all NASA APIs (free registration)
- **Rate Limits**: 1,000 requests per hour per API key
- **Attribution**: Required for all data usage
- **Terms of Service**: Must comply with NASA's usage guidelines

## 📸 APOD API (Astronomy Picture of the Day)

### API Information
- **Base URL**: `https://api.nasa.gov/planetary/apod`
- **Method**: GET
- **Authentication**: API key required
- **Data Format**: JSON
- **Historical Data**: Available from June 16, 1995 to present

### Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `api_key` | string | Yes | NASA API key | `DEMO_KEY` |
| `date` | string | No | YYYY-MM-DD format | `2025-08-10` |
| `start_date` | string | No | YYYY-MM-DD format | `2025-08-01` |
| `end_date` | string | No | YYYY-MM-DD format | `2025-08-10` |
| `count` | integer | No | Random images count | `5` |
| `thumbs` | boolean | No | Include thumbnail URLs | `true` |

### Response Format

```json
{
  "copyright": "John Smith",
  "date": "2025-08-10",
  "explanation": "The Andromeda Galaxy, also known as M31, is a spiral galaxy approximately 2.5 million light-years from Earth...",
  "hdurl": "https://apod.nasa.gov/apod/image/2508/AndromedaGalaxy_4k.jpg",
  "media_type": "image",
  "service_version": "v1",
  "title": "The Andromeda Galaxy in High Resolution",
  "url": "https://apod.nasa.gov/apod/image/2508/AndromedaGalaxy_1k.jpg"
}
```

### Response Fields Explained

- **copyright**: Image copyright holder (photographer/institution)
- **date**: Publication date of the APOD entry
- **explanation**: Scientific explanation written by professional astronomers
- **hdurl**: High-definition image URL (if available)
- **media_type**: Content type (`image` or `video`)
- **service_version**: API version
- **title**: Title of the astronomical subject
- **url**: Standard resolution image or video embed URL

### Usage Examples

#### Get Today's APOD
```bash
curl "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
```

#### Get APOD for Specific Date
```bash
curl "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=2025-08-10"
```

#### Get Date Range
```bash
curl "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&start_date=2025-08-01&end_date=2025-08-10"
```

#### Get Random APODs
```bash
curl "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=5"
```

### Media Types

#### Images
- **Standard Resolution**: Optimized for web viewing (typically 1024px wide)
- **High Definition**: Full resolution images (can be several MB)
- **Format**: Usually JPEG, occasionally PNG or GIF
- **Quality**: Professional astronomical photography

#### Videos
- **Sources**: YouTube embeds, NASA video content, animations
- **Format**: HTML iframe embed codes
- **Duration**: Varies from seconds to several minutes
- **Content**: Time-lapse, animations, mission footage

### Integration in Our Dashboard

```python
class APODService:
    BASE_URL = "https://api.nasa.gov/planetary/apod"
    
    @classmethod
    def fetch_apod(cls, date=None):
        params = {
            'api_key': settings.NASA_API_KEY,
            'date': date or timezone.now().date().strftime('%Y-%m-%d')
        }
        
        try:
            response = requests.get(cls.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"APOD API error: {e}")
            return None
```

## ☀️ DONKI API (Space Weather Database)

### API Information
- **Base URL**: `https://api.nasa.gov/DONKI/`
- **Method**: GET
- **Authentication**: API key required
- **Data Format**: JSON
- **Coverage**: Space weather events from 2009 to present

### Available Endpoints

#### Solar Flares (FLR)
- **Endpoint**: `/DONKI/FLR`
- **Description**: Solar flare events detected by GOES satellites

#### Coronal Mass Ejections (CME)
- **Endpoint**: `/DONKI/CME`
- **Description**: Solar wind disturbances

#### Geomagnetic Storms (GST)
- **Endpoint**: `/DONKI/GST`
- **Description**: Earth's magnetic field disturbances

#### Interplanetary Shocks (IPS)
- **Endpoint**: `/DONKI/IPS`
- **Description**: Solar wind shock waves

#### Magnetopause Crossings (MPC)
- **Endpoint**: `/DONKI/MPC`
- **Description**: Solar wind boundary interactions

#### Radiation Belt Enhancements (RBE)
- **Endpoint**: `/DONKI/RBE`
- **Description**: Charged particle increases

#### Solar Energetic Particles (SEP)
- **Endpoint**: `/DONKI/SEP`
- **Description**: High-energy particle events

#### Solar Wind High Speed Streams (HSS)
- **Endpoint**: `/DONKI/HSS`
- **Description**: Fast solar wind regions

### Solar Flares Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `api_key` | string | Yes | NASA API key | `DEMO_KEY` |
| `startDate` | string | No | YYYY-MM-DD format | `2025-08-01` |
| `endDate` | string | No | YYYY-MM-DD format | `2025-08-10` |

### Solar Flares Response Format

```json
[
  {
    "flrID": "2025-08-10T12:34:00-FLR-001",
    "instruments": [
      {
        "displayName": "GOES-16: SUVI 195"
      }
    ],
    "beginTime": "2025-08-10T12:34Z",
    "peakTime": "2025-08-10T12:45Z",
    "endTime": "2025-08-10T12:52Z",
    "classType": "M2.5",
    "sourceLocation": "S15W30",
    "activeRegionNum": 3421,
    "note": "This flare was associated with a Type II radio burst.",
    "submissionTime": "2025-08-10T13:15Z",
    "link": "https://kauai.ccmc.gsfc.nasa.gov/..."
  }
]
```

### Flare Classification System

#### X-Class (X1.0 - X20+)
- **Intensity**: Most powerful flares
- **Frequency**: ~10 per solar maximum year
- **Effects**: Global radio blackouts, satellite damage, power grid issues
- **Duration**: Minutes to hours

#### M-Class (M1.0 - M9.9)
- **Intensity**: Medium-level flares
- **Frequency**: ~500 per solar maximum year
- **Effects**: Regional radio blackouts, minor satellite effects
- **Duration**: Minutes to hours

#### C-Class (C1.0 - C9.9)
- **Intensity**: Common, small flares
- **Frequency**: ~2000 per solar maximum year
- **Effects**: Minor radio communication impacts
- **Duration**: Minutes

#### B-Class (B1.0 - B9.9)
- **Intensity**: Background level
- **Frequency**: Very common
- **Effects**: No significant effects
- **Duration**: Minutes

### Integration in Our Dashboard

```python
class SolarFlaresService:
    BASE_URL = "https://api.nasa.gov/DONKI/FLR"
    
    @classmethod
    def fetch_solar_flares(cls, start_date, end_date):
        params = {
            'api_key': settings.NASA_API_KEY,
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d')
        }
        
        try:
            response = requests.get(cls.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"DONKI API error: {e}")
            return []
```

## ☄️ NeoWs API (Near Earth Object Web Service)

### API Information
- **Base URL**: `https://api.nasa.gov/neo/rest/v1/`
- **Method**: GET
- **Authentication**: API key required
- **Data Format**: JSON
- **Coverage**: All cataloged near-Earth objects

### Available Endpoints

#### Feed (Close Approaches)
- **Endpoint**: `/neo/rest/v1/feed`
- **Description**: Asteroids approaching Earth within date range
- **Date Range Limit**: Maximum 7 days

#### Lookup (Asteroid Details)
- **Endpoint**: `/neo/rest/v1/neo/{asteroid_id}`
- **Description**: Detailed information about specific asteroid

#### Browse
- **Endpoint**: `/neo/rest/v1/neo/browse`
- **Description**: Paginated list of all near-Earth objects

#### Stats
- **Endpoint**: `/neo/rest/v1/stats`
- **Description**: Summary statistics about near-Earth objects

#### Today's Feed
- **Endpoint**: `/neo/rest/v1/feed/today`
- **Description**: Asteroids approaching today

### Feed Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `api_key` | string | Yes | NASA API key | `DEMO_KEY` |
| `start_date` | string | Yes | YYYY-MM-DD format | `2025-08-10` |
| `end_date` | string | Yes | YYYY-MM-DD format | `2025-08-17` |
| `detailed` | boolean | No | Include orbital data | `true` |

### Feed Response Format

```json
{
  "links": {
    "next": "http://...",
    "prev": "http://...",
    "self": "http://..."
  },
  "element_count": 25,
  "near_earth_objects": {
    "2025-08-10": [
      {
        "id": "54016849",
        "neo_reference_id": "54016849",
        "name": "(2020 QG5)",
        "nasa_jpl_url": "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=54016849",
        "absolute_magnitude_h": 21.77,
        "estimated_diameter": {
          "kilometers": {
            "estimated_diameter_min": 0.1092742805,
            "estimated_diameter_max": 0.2443193171
          },
          "meters": {
            "estimated_diameter_min": 109.2742805293,
            "estimated_diameter_max": 244.3193170921
          },
          "miles": {
            "estimated_diameter_min": 0.0678787829,
            "estimated_diameter_max": 0.1517669551
          },
          "feet": {
            "estimated_diameter_min": 358.5113735018,
            "estimated_diameter_max": 801.5725215252
          }
        },
        "is_potentially_hazardous_asteroid": false,
        "close_approach_data": [
          {
            "close_approach_date": "2025-08-10",
            "close_approach_date_full": "2025-Aug-10 14:26",
            "epoch_date_close_approach": 1754992400000,
            "relative_velocity": {
              "kilometers_per_second": "8.0415894776",
              "kilometers_per_hour": "28949.5221194",
              "miles_per_hour": "17989.5537789"
            },
            "miss_distance": {
              "astronomical": "0.2845641121",
              "lunar": "110.6354396",
              "kilometers": "42567970.862513927",
              "miles": "26451821.8903895"
            },
            "orbiting_body": "Earth"
          }
        ],
        "is_sentry_object": false
      }
    ]
  }
}
```

### Key Data Fields

#### Physical Characteristics
- **absolute_magnitude_h**: Brightness measure (lower = larger/brighter)
- **estimated_diameter**: Size estimates in various units
- **is_potentially_hazardous**: PHO classification (size > 140m, distance < 7.5M km)
- **is_sentry_object**: Continuously monitored for impact risk

#### Orbital Data
- **close_approach_date**: Date of closest approach
- **epoch_date_close_approach**: Unix timestamp
- **relative_velocity**: Speed relative to Earth
- **miss_distance**: How close it gets to Earth
- **orbiting_body**: What it's orbiting (Earth, Mars, etc.)

### Size Classifications

#### By Diameter
- **Small** (< 25m): City block size, burns up in atmosphere
- **Medium** (25m - 140m): Regional damage potential
- **Large** (140m - 1km): PHO threshold, significant damage
- **Very Large** (1km - 10km): Global effects
- **Extremely Large** (> 10km): Mass extinction potential

#### By Absolute Magnitude (H)
- **H < 17.75**: Diameter > 1 km (global threat)
- **H 17.75-22**: Diameter 140m-1km (regional threat)
- **H 22-25**: Diameter 40-140m (local threat)
- **H > 25**: Diameter < 40m (atmospheric burnup)

### Integration in Our Dashboard

```python
class AsteroidService:
    BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"
    
    @classmethod
    def fetch_asteroids(cls, start_date, end_date):
        # Ensure date range is within 7-day limit
        delta = end_date - start_date
        if delta.days > 7:
            end_date = start_date + timedelta(days=7)
        
        params = {
            'api_key': settings.NASA_API_KEY,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'detailed': 'true'
        }
        
        try:
            response = requests.get(cls.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"NeoWs API error: {e}")
            return {'near_earth_objects': {}}
```

## 🔧 API Best Practices

### Rate Limiting
- **Respect Limits**: Stay within 1,000 requests per hour
- **Implement Caching**: Store responses to reduce API calls
- **Use Batch Requests**: Request date ranges instead of individual dates
- **Monitor Usage**: Track API usage to avoid hitting limits

### Error Handling
- **HTTP Status Codes**: Check for 200 OK responses
- **Timeout Handling**: Set reasonable request timeouts
- **Retry Logic**: Implement exponential backoff for failures
- **Fallback Data**: Use cached data when APIs are unavailable

### Performance Optimization
- **Asynchronous Requests**: Use async/await for multiple API calls
- **Connection Pooling**: Reuse HTTP connections
- **Data Compression**: Request compressed responses when available
- **Selective Fields**: Only request needed data fields

### Security Considerations
- **API Key Security**: Never expose keys in client-side code
- **Environment Variables**: Store keys securely
- **HTTPS Only**: Always use encrypted connections
- **Input Validation**: Validate all user inputs before API calls

## 📊 Data Processing Pipeline

### Data Flow Architecture
```
NASA APIs → Raw JSON Data → Data Validation → Database Storage → 
Web Interface → User Visualization
```

### Processing Steps
1. **API Request**: Scheduled or user-triggered requests
2. **Response Validation**: Verify data structure and content
3. **Data Transformation**: Convert to internal data models
4. **Database Storage**: Persist data with timestamps
5. **Cache Updates**: Update cached responses
6. **User Interface**: Display processed data to users

### Scheduled Updates
- **APOD**: Daily at midnight UTC
- **Solar Flares**: Every 6 hours
- **Asteroids**: Daily for upcoming week
- **Manual Refresh**: User-triggered updates available

---

*This API documentation provides comprehensive information about NASA's data services and how they're integrated into our Space Weather Dashboard, enabling developers and researchers to understand and potentially extend the platform's capabilities.*
