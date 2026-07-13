# Example Usage and Testing Script
import requests
import json

BASE_URL = "http://localhost:5000"

def test_route_calculation():
    """Test route calculation API"""
    print("=" * 50)
    print("Testing Route Calculation")
    print("=" * 50)
    
    data = {
        "source": {"lat": 28.6139, "lng": 77.2090},
        "destination": {"lat": 28.6200, "lng": 77.2150},
        "user_type": "wheelchair"
    }
    
    response = requests.post(f"{BASE_URL}/api/calculate-routes", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Found {len(result['routes'])} routes")
        
        for route in result['routes']:
            print(f"\n{route['name']}:")
            print(f"  - Distance: {route['distance']:.2f} km")
            print(f"  - Accessibility Score: {route['accessibility_score']}/100")
            print(f"  - Safety Level: {route['safety_level']}")
            print(f"  - Road Condition: {route['road_condition']}")
            print(f"  - Ramps: {route['ramps']}")
            print(f"  - Obstacles: {', '.join(route['obstacles']) if route['obstacles'] else 'None'}")
    else:
        print(f"✗ Error: {response.status_code}")

def test_nearby_facilities():
    """Test nearby facilities API"""
    print("\n" + "=" * 50)
    print("Testing Nearby Facilities")
    print("=" * 50)
    
    params = {
        "lat": 28.6139,
        "lng": 77.2090,
        "type": "hospital",
        "radius": 3
    }
    
    response = requests.get(f"{BASE_URL}/api/nearby", params=params)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Found {len(result['places'])} hospitals within 3 km")
        
        for place in result['places'][:3]:
            print(f"\n{place['name']}:")
            print(f"  - Distance: {place['distance_km']} km")
            print(f"  - Address: {place['address']}")
            print(f"  - Phone: {place['phone']}")
            print(f"  - Accessible: {'Yes' if place['accessible'] else 'No'}")
    else:
        print(f"✗ Error: {response.status_code}")

def test_accessibility_scoring():
    """Demonstrate accessibility scoring algorithm"""
    print("\n" + "=" * 50)
    print("Accessibility Scoring Examples")
    print("=" * 50)
    
    from route_calculator import calculate_accessibility_score
    
    # Example 1: Perfect wheelchair route
    route1 = {
        'road_condition': 'good',
        'obstacles': [],
        'ramps': 4,
        'has_curb_cuts': True,
        'audio_signals': False,
        'tactile_paving': False,
        'benches': 2,
        'well_lit': True,
        'gradient': 1
    }
    score1 = calculate_accessibility_score(route1, 'wheelchair')
    print(f"\nPerfect Wheelchair Route: {score1}/100")
    
    # Example 2: Route with obstacles
    route2 = {
        'road_condition': 'moderate',
        'obstacles': ['construction', 'blocked_path'],
        'ramps': 1,
        'has_curb_cuts': False,
        'audio_signals': False,
        'tactile_paving': False,
        'benches': 1,
        'well_lit': False,
        'gradient': 5
    }
    score2 = calculate_accessibility_score(route2, 'wheelchair')
    print(f"Route with Obstacles: {score2}/100")
    
    # Example 3: Visually impaired optimized
    route3 = {
        'road_condition': 'good',
        'obstacles': [],
        'ramps': 2,
        'has_curb_cuts': True,
        'audio_signals': True,
        'tactile_paving': True,
        'benches': 3,
        'well_lit': True,
        'gradient': 2
    }
    score3 = calculate_accessibility_score(route3, 'visually_impaired')
    print(f"Visually Impaired Route: {score3}/100")

def test_voice_instructions():
    """Demonstrate voice navigation instructions"""
    print("\n" + "=" * 50)
    print("Voice Navigation Instructions Example")
    print("=" * 50)
    
    instructions = [
        "Starting navigation on Main Route. Total distance: 2.5 kilometers.",
        "This route has an accessibility score of 95 out of 100.",
        "Accessible ramp ahead in 50 meters.",
        "Audio crossing signal ahead. Listen for the beep.",
        "Rest area with bench available in 100 meters.",
        "Turn left in 50 meters.",
        "Turn right in 100 meters.",
        "You are approaching your destination.",
        "You have arrived at your destination."
    ]
    
    print("\nSample voice instructions:")
    for i, instruction in enumerate(instructions, 1):
        print(f"{i}. {instruction}")

def print_system_info():
    """Print system information"""
    print("\n" + "=" * 50)
    print("System Information")
    print("=" * 50)
    
    print("\nSupported User Types:")
    print("  1. Wheelchair Users")
    print("     - Optimized for ramps and curb cuts")
    print("     - Avoids steep gradients")
    print("     - Prioritizes smooth surfaces")
    
    print("\n  2. Visually Impaired")
    print("     - Prioritizes audio signals")
    print("     - Requires tactile paving")
    print("     - Well-lit routes preferred")
    
    print("\n  3. Elderly")
    print("     - Frequent rest areas")
    print("     - Gentle gradients")
    print("     - Shorter distances preferred")
    
    print("\nAccessibility Features Tracked:")
    print("  ♿ Wheelchair ramps")
    print("  🚦 Traffic signals (audio)")
    print("  🪑 Rest benches")
    print("  🚧 Obstacles and construction")
    print("  🏥 Nearby hospitals")
    print("  👮 Nearby police stations")

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Disability Friendly Route Mapping System")
    print("Example Usage and Testing")
    print("=" * 50)
    
    # Print system info
    print_system_info()
    
    # Test accessibility scoring (doesn't require server)
    test_accessibility_scoring()
    
    # Test voice instructions
    test_voice_instructions()
    
    # Test API endpoints (requires server running)
    try:
        test_route_calculation()
        test_nearby_facilities()
    except requests.exceptions.ConnectionError:
        print("\n⚠ Server not running. Start with: python app.py")
    
    print("\n" + "=" * 50)
    print("Testing Complete!")
    print("=" * 50)
