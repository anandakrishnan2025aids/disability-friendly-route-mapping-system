# Route Calculation & Accessibility Scoring Algorithm
import math

def calculate_accessibility_score(route_data, user_type):
    """
    Calculate accessibility score based on route features and user type
    Score: 0-100 (higher is better)
    """
    score = 100
    
    # Road condition penalty
    if route_data.get('road_condition') == 'bad':
        score -= 30
    elif route_data.get('road_condition') == 'moderate':
        score -= 15
    
    # Obstacle penalty (dynamic based on severity)
    obstacles = route_data.get('obstacles', [])
    for obs in obstacles:
        if isinstance(obs, dict):
            severity = obs.get('severity', 'medium')
            if severity == 'critical':
                score -= 25
            elif severity == 'high':
                score -= 15
            else:
                score -= 10
        else:
            score -= 10
    
    # Ramp bonus (for wheelchair users)
    if user_type == 'wheelchair':
        ramps = route_data.get('ramps', 0)
        score += min(ramps * 5, 20)
        if route_data.get('has_curb_cuts'):
            score += 10
    
    # Traffic signal bonus (for visually impaired)
    if user_type == 'visually_impaired':
        if route_data.get('audio_signals'):
            score += 15
        if route_data.get('tactile_paving'):
            score += 10
    
    # Rest areas bonus (for elderly)
    if user_type == 'elderly':
        benches = route_data.get('benches', 0)
        score += min(benches * 3, 15)
    
    # Lighting bonus
    if route_data.get('well_lit'):
        score += 5
    
    # Gradient penalty
    gradient = route_data.get('gradient', 0)
    if gradient > 5:
        score -= 20
    elif gradient > 3:
        score -= 10
    
    return max(0, min(100, score))

def calculate_difficulty_level(route_data):
    """
    Calculate route difficulty: Easy, Moderate, Difficult
    """
    difficulty_score = 0
    
    # Gradient impact
    gradient = route_data.get('gradient', 0)
    if gradient > 5:
        difficulty_score += 3
    elif gradient > 3:
        difficulty_score += 2
    elif gradient > 1:
        difficulty_score += 1
    
    # Distance impact
    distance = route_data.get('distance', 0)
    if distance > 3:
        difficulty_score += 2
    elif distance > 1.5:
        difficulty_score += 1
    
    # Surface condition
    if route_data.get('road_condition') == 'bad':
        difficulty_score += 2
    elif route_data.get('road_condition') == 'moderate':
        difficulty_score += 1
    
    # Obstacles
    obstacles = route_data.get('obstacles', [])
    difficulty_score += min(len(obstacles), 3)
    
    # Classify
    if difficulty_score <= 2:
        return 'Easy', '#10e8b8'
    elif difficulty_score <= 5:
        return 'Moderate', '#ffc35a'
    else:
        return 'Difficult', '#ff5c7a'

def haversine_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points in km"""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def generate_routes(source, destination, user_type):
    """
    Generate multiple routes with accessibility scores
    Returns list of routes sorted by safety
    """
    # Simulate 3 different routes
    routes = [
        {
            'id': 1,
            'name': 'Main Route',
            'coordinates': interpolate_points(source, destination, 5),
            'distance': haversine_distance(source['lat'], source['lng'], destination['lat'], destination['lng']),
            'road_condition': 'good',
            'ramps': 3,
            'obstacles': [],
            'audio_signals': True,
            'tactile_paving': True,
            'benches': 4,
            'well_lit': True,
            'gradient': 2,
            'has_curb_cuts': True
        },
        {
            'id': 2,
            'name': 'Alternate Route',
            'coordinates': interpolate_points(source, destination, 6, offset=0.002),
            'distance': haversine_distance(source['lat'], source['lng'], destination['lat'], destination['lng']) * 1.15,
            'road_condition': 'moderate',
            'ramps': 2,
            'obstacles': [{'type': 'construction', 'severity': 'medium'}],
            'audio_signals': False,
            'tactile_paving': True,
            'benches': 2,
            'well_lit': True,
            'gradient': 4,
            'has_curb_cuts': True
        },
        {
            'id': 3,
            'name': 'Shortest Route',
            'coordinates': interpolate_points(source, destination, 4, offset=-0.001),
            'distance': haversine_distance(source['lat'], source['lng'], destination['lat'], destination['lng']) * 0.9,
            'road_condition': 'bad',
            'ramps': 1,
            'obstacles': [{'type': 'blocked_path', 'severity': 'high'}],
            'audio_signals': False,
            'tactile_paving': False,
            'benches': 1,
            'well_lit': False,
            'gradient': 6,
            'has_curb_cuts': False
        }
    ]
    
    # Calculate accessibility scores and difficulty
    for route in routes:
        route['accessibility_score'] = calculate_accessibility_score(route, user_type)
        route['user_type'] = user_type
        route['difficulty'], route['difficulty_color'] = calculate_difficulty_level(route)
        
        # Classify route safety
        if route['accessibility_score'] >= 80:
            route['safety_level'] = 'safe'
            route['color'] = '#10e8b8'
        elif route['accessibility_score'] >= 60:
            route['safety_level'] = 'moderate'
            route['color'] = '#ffc35a'
        else:
            route['safety_level'] = 'risky'
            route['color'] = '#ff5c7a'
    
    # Sort by accessibility score
    routes.sort(key=lambda x: x['accessibility_score'], reverse=True)
    return routes

def interpolate_points(start, end, num_points, offset=0):
    """Generate intermediate points between start and end"""
    points = []
    for i in range(num_points + 1):
        ratio = i / num_points
        lat = start['lat'] + (end['lat'] - start['lat']) * ratio + offset
        lng = start['lng'] + (end['lng'] - start['lng']) * ratio + offset
        points.append([lat, lng])
    return points

def find_nearest_facilities(route_coords, facilities, facility_type, limit=2):
    """Find nearest facilities along the route"""
    nearest = []
    for facility in facilities:
        if facility['type'] != facility_type:
            continue
        
        # Calculate minimum distance to route
        min_dist = float('inf')
        for coord in route_coords:
            dist = haversine_distance(coord[0], coord[1], facility['lat'], facility['lng'])
            min_dist = min(min_dist, dist)
        
        facility['distance_to_route'] = min_dist
        nearest.append(facility)
    
    nearest.sort(key=lambda x: x['distance_to_route'])
    return nearest[:limit]
