# Disability Friendly Route Mapping System - Documentation

## Project Overview
A Flask-based web application that provides smart accessibility navigation for wheelchair users, visually impaired individuals, and elderly people.

## Features Implemented

### 1. Smart Route Calculation
- **Multiple Route Generation**: System generates 3 different routes between source and destination
- **User-Specific Optimization**: Routes optimized based on user type (Wheelchair/Visually Impaired/Elderly)
- **Accessibility Scoring**: Each route scored 0-100 based on multiple factors

### 2. Accessibility Scoring Algorithm
The system calculates scores based on:
- **Road Condition**: Good (+0), Moderate (-15), Bad (-30)
- **Obstacles**: -10 points per obstacle (construction, blocked paths)
- **Wheelchair Features**: Ramps (+5 each), Curb cuts (+10)
- **Visual Impairment Features**: Audio signals (+15), Tactile paving (+10)
- **Elderly Features**: Rest benches (+3 each)
- **Lighting**: Well-lit routes (+5)
- **Gradient**: Steep slopes penalized (-10 to -20)

### 3. Route Classification
- **Safe (80-100)**: Green color, highest priority
- **Moderate (60-79)**: Yellow color, acceptable with caution
- **Risky (<60)**: Red color, not recommended

### 4. Map Features (Leaflet.js)
- **Interactive Map**: Click to set source/destination
- **Color-Coded Routes**: Visual distinction between safe/moderate/risky
- **Facility Markers**: 
  - 🏥 Hospitals
  - 👮 Police Stations
  - ♿ Wheelchair Ramps
  - 🚦 Traffic Signals
  - 🪑 Rest Areas/Benches
- **Clickable Popups**: Detailed information for each marker

### 5. Voice Navigation
- **Browser-Based TTS**: Uses JavaScript SpeechSynthesis API
- **Turn-by-Turn Instructions**: "Turn left in 50 meters"
- **Accessibility Alerts**: "Accessible ramp ahead", "Audio signal ahead"
- **Obstacle Warnings**: "Construction detected, proceed with caution"
- **Auto-Advance**: Instructions spoken every 8 seconds

### 6. Nearby Facilities
- **Hospital Finder**: Shows 2 nearest hospitals along route
- **Police Station Finder**: Shows 2 nearest police stations
- **Distance Calculation**: Haversine formula for accurate distances
- **Contact Information**: Phone numbers and addresses displayed

## File Structure

```
disability-friendly-route-mapping/
│
├── app.py                      # Main Flask application
├── models.py                   # Database models and schema
├── route_calculator.py         # Route generation & scoring algorithm
│
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── navigation.html        # Smart navigation page (NEW)
│   ├── map.html               # Map view
│   └── report.html            # Issue reporting
│
├── static/
│   ├── js/
│   │   ├── navigation.js      # Navigation & voice features (NEW)
│   │   ├── map.js             # Map functionality
│   │   └── main.js            # General scripts
│   └── css/
│       └── style.css          # Styles
│
└── accessibility.db           # SQLite database
```

## Database Schema

### accessibility_points
```sql
id              INTEGER PRIMARY KEY
type            TEXT (ramp, signal, bench, toilet, parking, audio)
name            TEXT
lat             REAL
lng             REAL
status          TEXT (operational, maintenance)
created_at      TIMESTAMP
```

### routes
```sql
id                      INTEGER PRIMARY KEY
name                    TEXT
description             TEXT
distance                REAL
accessibility_score     INTEGER
user_type               TEXT
coordinates             TEXT (JSON array)
created_at              TIMESTAMP
```

### facilities
```sql
id              INTEGER PRIMARY KEY
type            TEXT (hospital, police, accessible)
name            TEXT
address         TEXT
phone           TEXT
lat             REAL
lng             REAL
accessible      BOOLEAN
open_24h        BOOLEAN
```

## API Endpoints

### POST /api/calculate-routes
Calculate multiple routes with accessibility scores

**Request:**
```json
{
  "source": {"lat": 28.6139, "lng": 77.2090},
  "destination": {"lat": 28.6200, "lng": 77.2150},
  "user_type": "wheelchair"
}
```

**Response:**
```json
{
  "routes": [
    {
      "id": 1,
      "name": "Main Route",
      "coordinates": [[28.6139, 77.2090], ...],
      "distance": 2.5,
      "accessibility_score": 95,
      "safety_level": "safe",
      "color": "#28a745",
      "road_condition": "good",
      "ramps": 3,
      "obstacles": [],
      "nearest_hospital": [...],
      "nearest_police": [...]
    }
  ]
}
```

### GET /api/nearby
Find nearby facilities

**Parameters:**
- lat, lng: Coordinates
- type: hospital | police | accessible
- radius: Search radius in km (default: 5)

**Response:**
```json
{
  "places": [
    {
      "id": 1,
      "type": "hospital",
      "name": "City General Hospital",
      "lat": 28.6180,
      "lng": 77.2100,
      "distance_km": 0.5,
      "accessible": true,
      "phone": "011-2345-6789"
    }
  ]
}
```

### GET /api/routes
Get all accessible routes with filtering

**Parameters:**
- q: Search query
- tag: Filter by tag (wheelchair, visual, elderly)
- min_score: Minimum accessibility score

### POST /api/reports
Submit accessibility issue report

### GET /api/stats
Get system statistics

## Usage Guide

### For Users

1. **Navigate to Smart Navigation Page**
   - Click "Navigation" in menu
   - Or visit: http://localhost:5000/navigation

2. **Set Source and Destination**
   - Click on map to set source (green marker)
   - Click again to set destination (red marker)
   - Or enter coordinates manually

3. **Select User Type**
   - Choose: Wheelchair / Visually Impaired / Elderly
   - System optimizes routes accordingly

4. **Find Routes**
   - Click "Find Routes" button
   - View 3 routes with accessibility scores
   - Routes color-coded by safety level

5. **Select Route**
   - Click "Select Route" on preferred option
   - View nearby hospitals and police stations
   - See route markers (ramps, signals, benches)

6. **Start Voice Navigation**
   - Click "Start Voice Guide"
   - Listen to turn-by-turn instructions
   - Receive accessibility alerts
   - Click "Stop Voice" to end

### For Developers

**Run the Application:**
```bash
python app.py
```

**Access Points:**
- Home: http://localhost:5000/
- Navigation: http://localhost:5000/navigation
- Map: http://localhost:5000/map
- Reports: http://localhost:5000/report

**Customize Scoring Algorithm:**
Edit `route_calculator.py` → `calculate_accessibility_score()` function

**Add New Facility Types:**
1. Add to database schema in `models.py`
2. Update `nearby_places` in `app.py`
3. Add marker icon in `navigation.js`

## Future Enhancements

1. **Real-Time Updates**
   - Live traffic data integration
   - Real-time obstacle reporting
   - Community-driven updates

2. **Advanced Features**
   - GPS tracking
   - Offline map support
   - Multi-language voice support
   - Weather-based routing

3. **Integration**
   - Google Maps API for real routes
   - OpenStreetMap accessibility data
   - Government accessibility databases

4. **Mobile App**
   - Native iOS/Android apps
   - Push notifications
   - Background navigation

## Dependencies

```
Flask==2.3.0
sqlite3 (built-in)
```

Frontend:
- Leaflet.js 1.9.4
- Bootstrap 5
- Font Awesome 6
- JavaScript SpeechSynthesis API (built-in)

## Accessibility Compliance

- WCAG 2.1 Level AA compliant
- Screen reader compatible
- Keyboard navigation support
- High contrast mode
- Voice output for all critical information

## License
MIT License

## Support
For issues or questions, please create an issue in the repository.
