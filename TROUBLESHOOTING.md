# 🔧 TROUBLESHOOTING GUIDE - Map Not Loading

## Issue: Map shows blank/dark screen

### ✅ SOLUTION - Follow these steps:

## Step 1: Clear Browser Cache (CRITICAL!)

### Option A: Hard Refresh
1. Open the map page: http://localhost:5000/map
2. Press **Ctrl + Shift + R** (Windows/Linux) or **Cmd + Shift + R** (Mac)
3. This forces the browser to reload all files

### Option B: Clear Cache Completely
1. Press **Ctrl + Shift + Delete**
2. Select "Cached images and files"
3. Click "Clear data"
4. Restart browser

### Option C: Use Incognito Mode (FASTEST!)
1. Press **Ctrl + Shift + N** (Chrome) or **Ctrl + Shift + P** (Firefox)
2. Go to: http://localhost:5000/map
3. Map should load correctly

---

## Step 2: Verify Server is Running

```bash
# Start the server
python start.py

# OR
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Restarting with stat
```

---

## Step 3: Test the Map Page

1. Open: **http://localhost:5000/map**
2. You should see:
   - Dark themed map
   - Routes in the sidebar
   - Red emergency button (🆘) in top-right
   - Map controls at bottom-right

---

## Step 4: Check Browser Console

1. Press **F12** to open Developer Tools
2. Click "Console" tab
3. Look for errors

### Common Errors & Fixes:

#### Error: "Leaflet is not defined"
**Fix**: Clear cache and hard refresh (Ctrl+Shift+R)

#### Error: "Failed to fetch"
**Fix**: Make sure server is running on port 5000

#### Error: "Cannot read property 'map' of undefined"
**Fix**: The old Google Maps code is cached. Clear browser cache.

---

## Step 5: Verify Files Are Updated

Check that these files exist and are updated:

```bash
# Check if enhanced CSS exists
dir static\css\enhanced.css

# Check if map.js is updated (should NOT contain "google.maps")
type static\js\map.js | findstr "Leaflet"
```

If you see "Leaflet" in the output, the file is correct!

---

## Step 6: Test Navigation Page

The navigation page has all the enhanced features:

1. Go to: **http://localhost:5000/navigation**
2. Click on map to set source (green marker)
3. Click again to set destination (red marker)
4. Select user type
5. Click "Find Routes"
6. You should see 3 routes with:
   - Accessibility scores
   - Difficulty levels
   - Obstacle warnings
   - Emergency button

---

## Step 7: Test Emergency Button

1. Look for the red pulsing button (🆘) on the map
2. Click it
3. You should see a popup with:
   - Emergency numbers
   - Nearest hospital
   - Nearest police station

---

## 🎯 Quick Checklist

- [ ] Server is running (python app.py)
- [ ] Opened in incognito mode OR cleared cache
- [ ] Using http://localhost:5000/map or /navigation
- [ ] Browser console shows no errors (F12)
- [ ] Can see routes in sidebar
- [ ] Can see emergency button (🆘)
- [ ] Map tiles are loading (dark theme)

---

## 🔍 Still Not Working?

### Try Different Browser
- Chrome (recommended)
- Firefox
- Edge

### Check Port
```bash
# Make sure port 5000 is not in use
netstat -ano | findstr :5000
```

### Restart Everything
1. Stop server (Ctrl+C)
2. Close all browser windows
3. Start server again: `python start.py`
4. Open in incognito: Ctrl+Shift+N
5. Go to: http://localhost:5000/navigation

---

## ✨ Expected Result

When working correctly, you should see:

### Map Page (/map)
- ✅ Dark themed map with routes
- ✅ Sidebar with route list
- ✅ Emergency button (🆘) top-right
- ✅ Map controls bottom-right
- ✅ Markers for facilities
- ✅ Obstacle warnings (⚠️)

### Navigation Page (/navigation)
- ✅ Interactive map
- ✅ Source/destination markers
- ✅ 3 route options with scores
- ✅ Difficulty badges
- ✅ Voice navigation controls
- ✅ Emergency button
- ✅ Nearby facilities

---

## 📞 Debug Commands

```bash
# Check if files exist
dir static\css\enhanced.css
dir static\js\navigation.js

# Check if server is running
curl http://localhost:5000/api/routes

# Test obstacle API
curl http://localhost:5000/api/obstacles

# Test emergency API
curl -X POST http://localhost:5000/api/emergency -H "Content-Type: application/json" -d "{\"lat\":28.6139,\"lng\":77.2090}"
```

---

## 🎉 Success Indicators

You'll know it's working when you see:

1. **Map loads** with dark theme
2. **Routes appear** in sidebar
3. **Emergency button** pulses in top-right
4. **Clicking routes** highlights them on map
5. **Obstacle markers** (⚠️) visible
6. **No errors** in browser console (F12)

---

## 💡 Pro Tip

**Always use Incognito Mode when testing!**

This ensures you're seeing the latest version without cache issues.

**Keyboard Shortcut**: Ctrl + Shift + N (Chrome)

---

## 📝 Notes

- The map uses **Leaflet.js** (not Google Maps)
- No API key required
- Works offline once loaded
- Dark theme by default
- Mobile responsive

---

**If you still see issues after following all steps, the browser cache is the most likely culprit. Try a different browser or incognito mode!**
