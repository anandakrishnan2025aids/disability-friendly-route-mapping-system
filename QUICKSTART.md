# Quick Start Guide

## Installation

1. **Install Dependencies**
```bash
pip install Flask
```

2. **Initialize Database**
```bash
python -c "from models import init_db; init_db()"
```

3. **Run Application**
```bash
python app.py
```

4. **Open Browser**
Navigate to: http://localhost:5000

## Using Smart Navigation

### Step 1: Access Navigation Page
- Click "Navigation" in the menu
- Or go to: http://localhost:5000/navigation

### Step 2: Set Locations
**Option A - Click on Map:**
- First click = Source (green marker)
- Second click = Destination (red marker)

**Option B - Manual Entry:**
- Coordinates auto-update when you click the map

### Step 3: Select User Type
Choose from dropdown:
- **Wheelchair User**: Optimized for ramps, flat surfaces
- **Visually Impaired**: Prioritizes audio signals, tactile paving
- **Elderly**: Focuses on rest areas, gentle slopes

### Step 4: Find Routes
- Click "Find Routes" button
- System generates 3 routes with scores
- Routes displayed in different colors:
  - 🟢 Green = Safe (80-100)
  - 🟡 Yellow = Moderate (60-79)
  - 🔴 Red = Risky (<60)

### Step 5: Select Route
- Click "Select Route" on your preferred option
- View nearby hospitals and police stations
- See accessibility features marked on map

### Step 6: Voice Navigation
- Click "Start Voice Guide"
- Listen to instructions through speakers
- Instructions include:
  - Turn-by-turn directions
  - Accessibility alerts
  - Obstacle warnings
  - Distance updates
- Click "Stop Voice" to end

## Understanding Accessibility Scores

### Score Components:
- **Road Condition**: Good surfaces score higher
- **Ramps**: More ramps = higher score (wheelchair users)
- **Audio Signals**: Important for visually impaired
- **Rest Areas**: Benches for elderly users
- **Lighting**: Well-lit routes preferred
- **Gradient**: Flat routes score higher
- **Obstacles**: Construction/blockages reduce score

### Example Scores:
- **95-100**: Excellent accessibility, highly recommended
- **80-94**: Good accessibility, safe to use
- **60-79**: Moderate accessibility, use with caution
- **Below 60**: Poor accessibility, not recommended

## Map Markers

| Icon | Meaning |
|------|---------|
| ♿ | Wheelchair Ramp |
| 🚦 | Traffic Signal |
| 🪑 | Rest Bench |
| 🏥 | Hospital |
| 👮 | Police Station |

## Voice Commands

The system automatically speaks:
1. Route overview and distance
2. Accessibility score
3. Turn instructions
4. Feature alerts (ramps, signals)
5. Obstacle warnings
6. Arrival notification

## Troubleshooting

### No Voice Output?
- Check browser permissions for audio
- Ensure speakers/headphones connected
- Try Chrome/Edge (best support)

### Routes Not Showing?
- Ensure source and destination are set
- Check console for errors (F12)
- Verify server is running

### Map Not Loading?
- Check internet connection (Leaflet.js requires online)
- Clear browser cache
- Refresh page

## API Testing

Test with curl:

```bash
# Calculate routes
curl -X POST http://localhost:5000/api/calculate-routes \
  -H "Content-Type: application/json" \
  -d '{
    "source": {"lat": 28.6139, "lng": 77.2090},
    "destination": {"lat": 28.6200, "lng": 77.2150},
    "user_type": "wheelchair"
  }'

# Find nearby hospitals
curl "http://localhost:5000/api/nearby?lat=28.6139&lng=77.2090&type=hospital&radius=3"
```

## Tips for Best Experience

1. **Use Headphones**: For clear voice instructions
2. **Test Routes**: Try different user types to see optimization
3. **Check Facilities**: Always note nearest hospital/police
4. **Report Issues**: Use report page for obstacles
5. **Update Data**: Keep accessibility points current

## Next Steps

- Explore the Map page for pre-defined routes
- Submit accessibility reports
- View dashboard for statistics
- Check documentation for API details

## Support

For issues:
1. Check README.md for detailed documentation
2. Run example_usage.py for testing
3. Review console logs (F12 in browser)

Happy navigating! 🗺️♿
