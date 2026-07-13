# How to Run the Application with New Features

## Step-by-Step Guide

### Step 1: Install Dependencies

Open your terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

This will install Flask and other required packages.

---

### Step 2: Initialize the System

Run the setup script to initialize the database:

```bash
python setup.py
```

This will:
- Check if all dependencies are installed
- Verify all files are present
- Create the SQLite database
- Show you next steps

**Alternative**: If setup.py doesn't work, manually initialize:
```bash
python -c "from models import init_db; init_db()"
```

---

### Step 3: Start the Flask Application

Run the main application:

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**Keep this terminal window open** - the server needs to keep running.

---

### Step 4: Access the Application

Open your web browser and go to:

**Main Page:**
```
http://localhost:5000
```

**Smart Navigation (NEW FEATURE):**
```
http://localhost:5000/navigation
```

---

## Using the New Smart Navigation Feature

### 1. Set Source and Destination

**Method A - Click on Map:**
- First click on the map = Source location (green marker)
- Second click on the map = Destination location (red marker)

**Method B - Use Default Coordinates:**
- The form already has default coordinates
- Just select user type and click "Find Routes"

### 2. Select User Type

Choose from the dropdown:
- **Wheelchair** - Optimized for ramps, flat surfaces, curb cuts
- **Visually Impaired** - Prioritizes audio signals, tactile paving
- **Elderly** - Focuses on rest areas, gentle slopes

### 3. Find Routes

Click the **"Find Routes"** button

The system will:
- Generate 3 different routes
- Calculate accessibility scores (0-100)
- Display routes on the map in different colors:
  - 🟢 **Green** = Safe (80-100 score)
  - 🟡 **Yellow** = Moderate (60-79 score)
  - 🔴 **Red** = Risky (<60 score)

### 4. Select a Route

Click **"Select Route"** on your preferred option

You'll see:
- Route highlighted on the map
- Nearby hospitals (🏥)
- Nearby police stations (👮)
- Accessibility markers (♿ ramps, 🚦 signals, 🪑 benches)

### 5. Start Voice Navigation

Click **"Start Voice Guide"** button

The system will:
- Speak turn-by-turn instructions
- Alert you about accessibility features
- Warn about obstacles
- Show visual notifications on screen

**To stop:** Click **"Stop Voice"** button

---

## Testing the API Endpoints

### Test Route Calculation

Open a new terminal (keep the server running) and run:

```bash
python example_usage.py
```

This will test all features and show you example outputs.

### Manual API Testing

**Calculate Routes:**
```bash
curl -X POST http://localhost:5000/api/calculate-routes -H "Content-Type: application/json" -d "{\"source\": {\"lat\": 28.6139, \"lng\": 77.2090}, \"destination\": {\"lat\": 28.6200, \"lng\": 77.2150}, \"user_type\": \"wheelchair\"}"
```

**Find Nearby Hospitals:**
```bash
curl "http://localhost:5000/api/nearby?lat=28.6139&lng=77.2090&type=hospital&radius=3"
```

---

## Troubleshooting

### Problem: "Module not found" error

**Solution:**
```bash
pip install flask
```

### Problem: "No module named 'models'"

**Solution:** Make sure you're in the correct directory:
```bash
cd "c:\Users\anand\OneDrive\disability friendly route mapping system"
python app.py
```

### Problem: Voice navigation not working

**Solutions:**
1. Use Chrome or Edge browser (best support for Speech API)
2. Check browser permissions for audio
3. Make sure speakers/headphones are connected
4. Try refreshing the page

### Problem: Map not loading

**Solutions:**
1. Check your internet connection (Leaflet.js needs online access)
2. Clear browser cache (Ctrl + F5)
3. Check browser console for errors (F12)

### Problem: Routes not showing

**Solutions:**
1. Make sure you clicked on the map to set source and destination
2. Check that both markers (green and red) are visible
3. Look at the browser console (F12) for error messages

### Problem: Database error

**Solution:** Reinitialize the database:
```bash
python -c "from models import init_db; init_db()"
```

---

## Quick Test Checklist

✅ **Step 1:** Server running? (python app.py)
✅ **Step 2:** Can access http://localhost:5000 ?
✅ **Step 3:** Can access http://localhost:5000/navigation ?
✅ **Step 4:** Can click on map to set markers?
✅ **Step 5:** Can find routes?
✅ **Step 6:** Can select a route?
✅ **Step 7:** Can start voice navigation?

---

## Features Overview

### What's New:

1. **Smart Navigation Page** (`/navigation`)
   - Interactive map with Leaflet.js
   - Click to set source/destination
   - User type selection

2. **Route Calculation Algorithm**
   - Generates 3 routes with different characteristics
   - Scores based on accessibility features
   - User-specific optimization

3. **Voice Navigation**
   - Browser-based text-to-speech
   - Turn-by-turn instructions
   - Accessibility alerts
   - Obstacle warnings

4. **Nearby Facilities**
   - Shows nearest hospitals
   - Shows nearest police stations
   - Distance calculation
   - Contact information

5. **Visual Markers**
   - 🏥 Hospitals
   - 👮 Police stations
   - ♿ Wheelchair ramps
   - 🚦 Traffic signals
   - 🪑 Rest benches

---

## Example Workflow

1. **Start server:** `python app.py`
2. **Open browser:** http://localhost:5000/navigation
3. **Click map twice:** Set source (green) and destination (red)
4. **Select user type:** Choose "Wheelchair"
5. **Click "Find Routes":** See 3 routes with scores
6. **Click "Select Route":** Choose the green (safe) route
7. **View facilities:** See nearby hospitals and police stations
8. **Click "Start Voice Guide":** Listen to navigation instructions
9. **Click "Stop Voice":** End navigation

---

## Additional Resources

- **Complete Documentation:** README.md
- **Quick Start Guide:** QUICKSTART.md
- **Algorithm Details:** ALGORITHM.md
- **Implementation Summary:** IMPLEMENTATION_SUMMARY.md

---

## Need Help?

1. Check the browser console (F12) for error messages
2. Check the terminal where app.py is running for server errors
3. Run `python example_usage.py` to test the system
4. Review the documentation files

---

## Stopping the Application

To stop the server:
- Press **Ctrl + C** in the terminal where app.py is running

---

## Summary Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database
python setup.py

# 3. Start application
python app.py

# 4. Test features (in new terminal)
python example_usage.py

# 5. Open browser
# Go to: http://localhost:5000/navigation
```

That's it! You're ready to use the smart navigation features! 🎉🗺️♿
