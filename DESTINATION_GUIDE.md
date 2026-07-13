# Destination-Based Route Finding Guide

## Overview

When you search for a destination, the system automatically calculates multiple accessible routes from your current location and highlights the **SAFEST ROUTE** based on accessibility scores.

---

## How It Works

### Step 1: Search for Your Destination

In the search bar at the top, type the name of where you want to go:

**Available Destinations:**
- 🏥 City General Hospital
- 👮 Central Police Station
- 🌳 Central Park
- 🌊 Riverside Promenade
- 🛍️ Market Square
- 🏛️ Heritage Quarter
- 🚇 Accessible Metro Station
- 🛒 Accessible Shopping Mall
- 📚 Inclusive Library
- ♿ Disability Support Centre

**Example Searches:**
```
Type: "hospital"     → Finds City General Hospital
Type: "park"         → Finds Central Park
Type: "metro"        → Finds Metro Station
Type: "market"       → Finds Market Square
Type: "library"      → Finds Library
```

### Step 2: Destination Detected

When a destination is found, you'll see:
- 📍 Destination name displayed
- 🗺️ "Find Accessible Routes" button
- ❌ Close button to cancel

### Step 3: Calculate Routes

Click **"🗺️ Find Accessible Routes"** button

The system will:
1. ✅ Get your current location (or use map center)
2. ✅ Calculate 3 different routes
3. ✅ Score each route for accessibility (0-100)
4. ✅ Rank routes by safety
5. ✅ Highlight the SAFEST route

### Step 4: View Results

You'll see **3 routes** displayed:

#### 🥇 Route #1 - SAFEST (Recommended)
- **Highest accessibility score** (usually 80-100)
- **Green color** on map
- **Solid line** (most visible)
- **"✅ Use Safest Route"** button
- **Highlighted with green border**

#### 🥈 Route #2 - Alternative
- **Medium accessibility score** (usually 60-79)
- **Yellow color** on map
- **Dashed line**
- **"🗺️ View This Route"** button

#### 🥉 Route #3 - Option 3
- **Lower accessibility score** (may be <60)
- **Red color** on map
- **Dashed line**
- **"🗺️ View This Route"** button

---

## Understanding Route Information

Each route card shows:

### Route Name
- Main Route
- Alternate Route
- Shortest Route

### Distance
- 📏 Distance in kilometers
- Example: "2.5 km"

### Accessibility Score
- **80-100**: 🟢 Safe (Green badge)
- **60-79**: 🟡 Moderate (Yellow badge)
- **0-59**: 🔴 Risky (Red badge)

### Safety Details
- **🛣️ Road Condition**: good / moderate / bad
- **♿ Ramps**: Number of wheelchair ramps
- **⚠️ Obstacles**: Number of obstacles (construction, blockages)

### Route Ranking
- **🥇 RECOMMENDED**: Safest route (highest score)
- **🥈 Alternative**: Second best option
- **🥉 Option 3**: Third option (use with caution)

---

## Map Display

### Markers:
- **🟢 Green Circle**: Your current location
- **🔴 Red Circle**: Your destination
- **Colored Lines**: Routes (green/yellow/red)

### Route Colors:
- **Green (Solid)**: Safest route - RECOMMENDED
- **Yellow (Dashed)**: Moderate route - Use with caution
- **Red (Dashed)**: Risky route - Not recommended

### Click on Routes:
- Click any route line on the map
- See popup with detailed information
- View accessibility score and features

---

## Selecting a Route

### Option 1: Click "Use Safest Route"
- Automatically selects the best route
- Highlights it on the map
- Prepares for voice navigation

### Option 2: Click "View This Route"
- View alternative routes
- Compare different options
- Choose based on your preference

### Option 3: Click Route Card
- Click anywhere on the route card
- Map zooms to show that route
- Popup opens with details

---

## Example Walkthrough

### Scenario: Going to the Hospital

**Step 1:** Type "hospital" in search bar
```
Search: "hospital"
Result: City General Hospital found
```

**Step 2:** Click "Find Accessible Routes"
```
System: Getting your location...
System: Calculating routes...
```

**Step 3:** View 3 Routes
```
🥇 Main Route
   Distance: 2.3 km
   Score: 95/100 (Safe)
   Road: good | Ramps: 3 | Obstacles: 0
   ✅ Use Safest Route

🥈 Alternate Route  
   Distance: 2.6 km
   Score: 78/100 (Moderate)
   Road: moderate | Ramps: 2 | Obstacles: 1
   🗺️ View This Route

🥉 Shortest Route
   Distance: 1.9 km
   Score: 52/100 (Risky)
   Road: bad | Ramps: 1 | Obstacles: 2
   🗺️ View This Route
```

**Step 4:** Select Safest Route
```
Click: "✅ Use Safest Route"
Result: Route highlighted, ready for navigation
```

---

## Accessibility Scoring Explained

### What Makes a Route "Safe"?

**High Score (80-100):**
- ✅ Good road condition
- ✅ Multiple wheelchair ramps
- ✅ No obstacles
- ✅ Well-lit paths
- ✅ Gentle slopes
- ✅ Audio signals (for visually impaired)
- ✅ Rest benches (for elderly)

**Medium Score (60-79):**
- ⚠️ Moderate road condition
- ⚠️ Some ramps available
- ⚠️ Minor obstacles
- ⚠️ Adequate lighting
- ⚠️ Some slopes

**Low Score (<60):**
- ❌ Poor road condition
- ❌ Few or no ramps
- ❌ Multiple obstacles
- ❌ Poor lighting
- ❌ Steep slopes

---

## User Type Optimization

The system optimizes routes based on your disability type:

### Wheelchair Users
- Prioritizes: Ramps, flat surfaces, curb cuts
- Avoids: Steep slopes, stairs, narrow paths
- Looks for: Smooth pavement, wide pathways

### Visually Impaired
- Prioritizes: Audio signals, tactile paving
- Avoids: Complex intersections without signals
- Looks for: Well-lit routes, clear pathways

### Elderly Users
- Prioritizes: Rest benches, gentle slopes
- Avoids: Long distances, steep hills
- Looks for: Shorter routes with rest areas

**To Set Your Type:**
Scroll down to "Smart Route Recommendation" panel and select your disability type.

---

## Tips for Best Results

### ✅ DO:
- Allow location access for accurate routes
- Choose the safest route (🥇 recommended)
- Check road conditions before traveling
- Use voice navigation for guidance
- Report any obstacles you encounter

### ❌ DON'T:
- Ignore low accessibility scores
- Choose risky routes without checking
- Travel without checking weather
- Forget to charge your phone

---

## Voice Navigation

After selecting a route:

1. **Scroll down** to Voice Navigation bar
2. **Select your route** from dropdown
3. **Click "▶ Start"** button
4. **Listen** to turn-by-turn instructions

Voice will announce:
- Route overview and distance
- Accessibility score
- Turn-by-turn directions
- Ramps and signals ahead
- Obstacles and warnings
- Arrival notification

---

## Troubleshooting

### Problem: "No routes found"
**Solutions:**
- Check if destination is spelled correctly
- Try a different destination
- Ensure you have internet connection
- Refresh the page

### Problem: Location not detected
**Solutions:**
- Allow location access in browser
- Check browser permissions
- System will use map center as fallback

### Problem: All routes show low scores
**Solutions:**
- This means the area has accessibility challenges
- Choose the highest scoring route available
- Report issues to help improve data
- Consider alternative destinations

### Problem: Routes not showing on map
**Solutions:**
- Zoom out to see full route
- Click "View This Route" button
- Refresh the page
- Check internet connection

---

## Advanced Features

### Compare Routes Side-by-Side
- View all 3 routes simultaneously
- Compare scores, distances, features
- Make informed decision

### Real-Time Updates
- Routes consider current reports
- Avoids areas with open issues
- Updates based on community feedback

### Nearby Facilities
- See hospitals along route
- Find police stations nearby
- Locate accessible facilities

---

## Keyboard Shortcuts

- **Type in search**: Start typing destination
- **Escape**: Clear search
- **Enter**: Find routes (when destination shown)
- **Click route card**: View on map
- **Click map**: Close popups

---

## Mobile Usage

On mobile devices:
- Search bar at top
- Swipe to scroll routes
- Tap route to view
- Tap "Use Safest Route" to select
- Map adjusts automatically

---

## Privacy & Location

- Location used only for route calculation
- Not stored or shared
- Can use map center instead
- No tracking or data collection

---

## Summary

```
1. Search destination → "hospital"
2. Click "Find Routes" → System calculates
3. View 3 routes → Ranked by safety
4. Select safest → Green route (🥇)
5. Start navigation → Voice guidance
```

**The safest route is always highlighted and recommended first!** 🎯

---

## Quick Reference

| Feature | Description |
|---------|-------------|
| 🥇 SAFEST | Highest score, green, recommended |
| 🥈 Alternative | Medium score, yellow, backup option |
| 🥉 Option 3 | Lower score, red, use with caution |
| 🟢 Green | Safe route (80-100) |
| 🟡 Yellow | Moderate route (60-79) |
| 🔴 Red | Risky route (<60) |
| 📏 Distance | Route length in km |
| ♿ Ramps | Wheelchair accessibility |
| ⚠️ Obstacles | Hazards on route |

---

**Start navigating safely today!** 🗺️♿✨
