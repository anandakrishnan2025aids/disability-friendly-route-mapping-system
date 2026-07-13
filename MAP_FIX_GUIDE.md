# Map Not Loading - Fix Guide

## Issue: "Oops! Something went wrong" Error

### What Happened:
The template was trying to load Google Maps but the JavaScript uses Leaflet.js (OpenStreetMap). This mismatch caused the error.

### ✅ FIXED:
The map now properly uses **Leaflet.js** which:
- ✅ Works without API key
- ✅ Free to use
- ✅ No billing required
- ✅ Better for accessibility features

---

## How to Fix (Already Done)

### Changes Made:

1. **Removed Google Maps API**
   - Deleted Google Maps script tag
   - Removed invalid API key

2. **Added Leaflet.js Properly**
   - Added Leaflet CSS link
   - Added Leaflet JS script
   - Proper initialization

3. **Updated Template**
   - Fixed search bar
   - Added tag filters
   - Added all controls

---

## Test the Fix

### Step 1: Clear Browser Cache
```
Press: Ctrl + Shift + Delete
Select: Cached images and files
Click: Clear data
```

### Step 2: Restart Server
```bash
# Stop server (Ctrl + C)
# Start again
python app.py
```

### Step 3: Open Fresh Browser
```
Close all browser tabs
Open new window
Go to: http://localhost:5000/map
```

### Step 4: Verify Map Loads
You should see:
- ✅ OpenStreetMap tiles loading
- ✅ Routes displayed as green lines
- ✅ Markers for accessibility points
- ✅ No error messages

---

## If Map Still Doesn't Load

### Check 1: Internet Connection
Leaflet.js loads map tiles from internet
```
Test: Can you browse other websites?
Solution: Connect to internet
```

### Check 2: Browser Console
```
Press F12 → Console tab
Look for errors in red
```

**Common Errors:**

**Error: "Leaflet is not defined"**
```
Cause: Leaflet.js not loaded
Solution: Check internet connection
```

**Error: "map is not defined"**
```
Cause: JavaScript loading order issue
Solution: Refresh page (Ctrl + F5)
```

**Error: "Cannot read property 'coordinates'"**
```
Cause: Routes not loaded from API
Solution: Check if server is running
```

### Check 3: Verify Files
```bash
# Check if files exist
dir "static\js\map.js"
dir "static\css\map.css"
dir "templates\map.html"
```

All should exist.

### Check 4: Server Running
```bash
python app.py
```
Should show:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

---

## Manual Fix (If Needed)

### Fix 1: Update map.html

Open: `templates/map.html`

**In the `<head>` section, add:**
```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
```

**Before `</body>`, add:**
```html
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="{{ url_for('static', filename='js/map.js') }}"></script>
```

**Remove any Google Maps scripts:**
```html
<!-- DELETE THIS -->
<script src="https://maps.googleapis.com/maps/api/js?key=..."></script>
```

### Fix 2: Verify map.js

Open: `static/js/map.js`

**First lines should be:**
```javascript
const DEFAULT_CENTER = [28.6139, 77.2090]; // Delhi area
const DEFAULT_ZOOM = 13;

const map = L.map('map', {
    center: DEFAULT_CENTER,
    zoom: DEFAULT_ZOOM,
    zoomControl: true,
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19,
}).addTo(map);
```

---

## Why Leaflet.js Instead of Google Maps?

### Advantages:

✅ **Free**: No API key needed
✅ **No Billing**: Never get charged
✅ **Open Source**: Community maintained
✅ **Privacy**: No tracking
✅ **Customizable**: Easy to style
✅ **Lightweight**: Faster loading
✅ **Offline**: Can cache tiles

### Google Maps Issues:

❌ Requires API key
❌ Requires billing account
❌ Can be expensive
❌ Tracks users
❌ Complex setup
❌ Restricted usage

---

## Verify Map is Working

### Checklist:

```
✓ Map tiles loading (streets visible)
✓ Can zoom in/out
✓ Can pan around
✓ Routes showing as green lines
✓ Markers visible
✓ Search bar working
✓ No error messages
✓ Console shows no errors
```

### Test Features:

1. **Zoom Controls**
   - Click + button (zoom in)
   - Click - button (zoom out)

2. **Pan Map**
   - Click and drag map
   - Should move smoothly

3. **Routes**
   - Should see green lines
   - Click route to see popup

4. **Search**
   - Type "hospital"
   - Should show results

5. **Markers**
   - Should see icons on map
   - Click to see details

---

## Browser Compatibility

### Recommended Browsers:

✅ **Chrome** 90+ (Best)
✅ **Firefox** 88+
✅ **Edge** 90+
✅ **Safari** 14+

### Not Supported:

❌ Internet Explorer (any version)
❌ Old browsers (pre-2020)

---

## Network Issues

### If Map Tiles Don't Load:

**Symptom**: Gray squares instead of map
**Cause**: Can't reach OpenStreetMap servers

**Solutions:**

1. **Check Internet**
   ```
   Open: google.com
   If loads: Internet OK
   If not: Fix internet connection
   ```

2. **Check Firewall**
   ```
   Firewall might block OpenStreetMap
   Allow: tile.openstreetmap.org
   ```

3. **Try Different Network**
   ```
   Switch to mobile hotspot
   Or different WiFi
   ```

4. **Check Proxy**
   ```
   If behind corporate proxy
   May need to configure
   ```

---

## Performance Issues

### Map Loads Slowly:

**Solutions:**

1. **Reduce Zoom Level**
   ```javascript
   const DEFAULT_ZOOM = 12; // Instead of 13
   ```

2. **Limit Routes Displayed**
   ```javascript
   // Show only top 5 routes
   routes.slice(0, 5)
   ```

3. **Disable Animations**
   ```javascript
   map.setView(center, zoom, {animate: false});
   ```

---

## Complete Reset

### If Nothing Works:

```bash
# 1. Stop server
Ctrl + C

# 2. Clear browser completely
# - Close all tabs
# - Clear cache
# - Close browser

# 3. Delete browser cache folder
# Chrome: C:\Users\[user]\AppData\Local\Google\Chrome\User Data\Default\Cache
# Firefox: C:\Users\[user]\AppData\Local\Mozilla\Firefox\Profiles\

# 4. Restart computer
# (Clears all caches)

# 5. Start fresh
python app.py

# 6. Open browser
http://localhost:5000/map
```

---

## Success Indicators

### Map is Working When:

✅ Streets and buildings visible
✅ Can zoom and pan smoothly
✅ Routes show as colored lines
✅ Markers clickable
✅ Search returns results
✅ No error messages
✅ Console clean (no red errors)

---

## Get Help

### Still Not Working?

1. **Check Console**
   ```
   F12 → Console
   Copy any red errors
   ```

2. **Check Network**
   ```
   F12 → Network tab
   Look for failed requests (red)
   ```

3. **Check Server Logs**
   ```
   Look at terminal where app.py runs
   Any error messages?
   ```

4. **Try Different Browser**
   ```
   Chrome → Firefox → Edge
   One might work better
   ```

---

## Summary

**Problem**: Google Maps error
**Solution**: Switched to Leaflet.js
**Result**: Map works without API key

**To Test:**
1. Clear cache
2. Restart server
3. Refresh page
4. Map should load!

---

**The map should now work perfectly!** 🗺️✅
