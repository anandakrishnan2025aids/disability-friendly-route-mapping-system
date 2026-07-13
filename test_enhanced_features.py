"""
Test Script for Enhanced Features
Run this to verify all new features are working correctly
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_obstacles_api():
    """Test obstacle management endpoints"""
    print("\n=== Testing Obstacle API ===")
    
    # Test GET obstacles
    print("1. Getting all obstacles...")
    response = requests.get(f"{BASE_URL}/api/obstacles")
    if response.status_code == 200:
        print(f"✅ GET /api/obstacles - Success")
        print(f"   Found {len(response.json()['obstacles'])} obstacles")
    else:
        print(f"❌ GET /api/obstacles - Failed: {response.status_code}")
    
    # Test POST obstacle
    print("\n2. Reporting new obstacle...")
    test_obstacle = {
        "type": "construction",
        "description": "Test obstacle - road work",
        "lat": 28.6145,
        "lng": 77.2095,
        "severity": "high",
        "reported_by": "test_user"
    }
    response = requests.post(
        f"{BASE_URL}/api/obstacles",
        json=test_obstacle,
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 201:
        print(f"✅ POST /api/obstacles - Success")
        obstacle_id = response.json()['obstacle_id']
        print(f"   Created obstacle ID: {obstacle_id}")
        
        # Test resolve obstacle
        print(f"\n3. Resolving obstacle {obstacle_id}...")
        response = requests.post(f"{BASE_URL}/api/obstacles/{obstacle_id}/resolve")
        if response.status_code == 200:
            print(f"✅ POST /api/obstacles/{obstacle_id}/resolve - Success")
        else:
            print(f"❌ Resolve failed: {response.status_code}")
    else:
        print(f"❌ POST /api/obstacles - Failed: {response.status_code}")

def test_emergency_api():
    """Test emergency support endpoint"""
    print("\n=== Testing Emergency API ===")
    
    test_location = {
        "lat": 28.6139,
        "lng": 77.2090
    }
    
    print("Getting emergency facilities...")
    response = requests.post(
        f"{BASE_URL}/api/emergency",
        json=test_location,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print("✅ POST /api/emergency - Success")
        data = response.json()
        
        if data.get('nearest_hospital'):
            hospital = data['nearest_hospital']
            print(f"   Nearest Hospital: {hospital['name']}")
            print(f"   Distance: {hospital['distance_km']} km")
        
        if data.get('nearest_police'):
            police = data['nearest_police']
            print(f"   Nearest Police: {police['name']}")
            print(f"   Distance: {police['distance_km']} km")
        
        print(f"   Emergency Numbers: {data['emergency_numbers']}")
    else:
        print(f"❌ POST /api/emergency - Failed: {response.status_code}")

def test_route_calculation():
    """Test enhanced route calculation with difficulty"""
    print("\n=== Testing Route Calculation ===")
    
    route_request = {
        "source": {"lat": 28.6139, "lng": 77.2090},
        "destination": {"lat": 28.6200, "lng": 77.2150},
        "user_type": "wheelchair"
    }
    
    print("Calculating routes...")
    response = requests.post(
        f"{BASE_URL}/api/calculate-routes",
        json=route_request,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print("✅ POST /api/calculate-routes - Success")
        data = response.json()
        
        for i, route in enumerate(data['routes'], 1):
            print(f"\n   Route {i}: {route['name']}")
            print(f"   - Accessibility Score: {route['accessibility_score']}")
            print(f"   - Difficulty: {route.get('difficulty', 'N/A')}")
            print(f"   - Safety Level: {route['safety_level']}")
            print(f"   - Distance: {route['distance']:.2f} km")
            print(f"   - Obstacles: {len(route['obstacles'])}")
    else:
        print(f"❌ POST /api/calculate-routes - Failed: {response.status_code}")

def test_recommendation_api():
    """Test AI-based route recommendation"""
    print("\n=== Testing Route Recommendation ===")
    
    recommendation_request = {
        "disability": "wheelchair",
        "max_gradient": 3,
        "min_score": 80,
        "avoid_reports": True,
        "max_distance": 5
    }
    
    print("Getting route recommendations...")
    response = requests.post(
        f"{BASE_URL}/api/recommend",
        json=recommendation_request,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print("✅ POST /api/recommend - Success")
        data = response.json()
        
        for i, route in enumerate(data['recommendations'], 1):
            print(f"\n   Recommendation {i}: {route['name']}")
            print(f"   - AI Score: {route['ai_score']}")
            print(f"   - Accessibility Score: {route['accessibility_score']}")
            print(f"   - Reasons: {', '.join(route['reasons'])}")
    else:
        print(f"❌ POST /api/recommend - Failed: {response.status_code}")

def test_existing_endpoints():
    """Test that existing endpoints still work"""
    print("\n=== Testing Existing Endpoints ===")
    
    endpoints = [
        ("/api/routes", "GET"),
        ("/api/points", "GET"),
        ("/api/reports", "GET"),
        ("/api/stats", "GET"),
        ("/api/nearby?lat=28.6139&lng=77.2090&type=hospital", "GET")
    ]
    
    for endpoint, method in endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            print(f"✅ {method} {endpoint} - Success")
        else:
            print(f"❌ {method} {endpoint} - Failed: {response.status_code}")

def test_pages():
    """Test that all pages load"""
    print("\n=== Testing Page Loading ===")
    
    pages = [
        "/",
        "/map",
        "/navigation",
        "/report",
        "/about"
    ]
    
    for page in pages:
        response = requests.get(f"{BASE_URL}{page}")
        if response.status_code == 200:
            print(f"✅ {page} - Loaded successfully")
        else:
            print(f"❌ {page} - Failed: {response.status_code}")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("ENHANCED FEATURES TEST SUITE")
    print("=" * 60)
    
    try:
        # Test if server is running
        response = requests.get(BASE_URL, timeout=2)
        print(f"✅ Server is running at {BASE_URL}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Server is not running at {BASE_URL}")
        print("   Please start the server with: python app.py")
        return
    
    # Run all tests
    test_pages()
    test_existing_endpoints()
    test_obstacles_api()
    test_emergency_api()
    test_route_calculation()
    test_recommendation_api()
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETED")
    print("=" * 60)
    print("\n📋 Manual Testing Checklist:")
    print("   [ ] Open http://localhost:5000/navigation")
    print("   [ ] Click map to set source and destination")
    print("   [ ] Verify 3 routes display with difficulty badges")
    print("   [ ] Check obstacle markers on map (⚠️ icons)")
    print("   [ ] Click emergency button (🆘) - verify panel shows")
    print("   [ ] Select a route and start voice navigation")
    print("   [ ] Verify voice speaks instructions")
    print("   [ ] Test keyboard navigation (Tab key)")
    print("   [ ] Check mobile responsiveness (resize browser)")
    print("   [ ] Verify colors meet WCAG AAA standards")
    print("\n✨ All automated tests completed!")

if __name__ == "__main__":
    run_all_tests()
