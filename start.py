"""
Quick Start Script - Run this to start your enhanced application
"""

import os
import sys

print("=" * 60)
print("🚀 STARTING DISABILITY FRIENDLY ROUTE MAPPING SYSTEM")
print("=" * 60)
print()

# Check if we're in the right directory
if not os.path.exists('app.py'):
    print("❌ Error: app.py not found!")
    print("   Please run this script from the project directory")
    sys.exit(1)

print("✅ Found app.py")
print()

# Check for required files
required_files = [
    'models.py',
    'route_calculator.py',
    'static/js/map.js',
    'static/js/navigation.js',
    'static/css/enhanced.css',
    'templates/map.html',
    'templates/navigation.html'
]

print("📋 Checking required files...")
all_found = True
for file in required_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - MISSING!")
        all_found = False

print()

if not all_found:
    print("⚠️  Some files are missing. The application may not work correctly.")
    print()

# Start the application
print("=" * 60)
print("🎯 STARTING SERVER...")
print("=" * 60)
print()
print("📍 The application will be available at:")
print("   🌐 http://localhost:5000")
print()
print("📄 Available pages:")
print("   • Home:       http://localhost:5000/")
print("   • Map:        http://localhost:5000/map")
print("   • Navigation: http://localhost:5000/navigation")
print("   • Report:     http://localhost:5000/report")
print()
print("🆘 Emergency Features:")
print("   • Click the red 🆘 button on the map for emergency support")
print("   • View obstacles with ⚠️ markers")
print("   • Use voice navigation for turn-by-turn directions")
print()
print("⌨️  Press Ctrl+C to stop the server")
print("=" * 60)
print()

# Import and run the app
try:
    from app import app
    app.run(debug=True, port=5000)
except KeyboardInterrupt:
    print("\n\n👋 Server stopped. Goodbye!")
except Exception as e:
    print(f"\n❌ Error starting server: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure Flask is installed: pip install Flask")
    print("2. Check if port 5000 is available")
    print("3. Review the error message above")
