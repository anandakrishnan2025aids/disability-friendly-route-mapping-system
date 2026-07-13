import base64
import re
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import math
import random
from route_calculator import generate_routes, find_nearest_facilities, calculate_accessibility_score
from models import init_db, get_db
import sqlite3

app = Flask(__name__)

# Initialize database
init_db()

# ── Seed data ────────────────────────────────────────────────
reports = []

# Coimbatore-based accessible routes
accessible_routes = [
    {
        "id": 1,
        "name": "RS Puram Accessible Loop",
        "description": "Fully paved, flat route with tactile guides and audio crossings in RS Puram area.",
        "distance": "2.8 km",
        "duration": "30 min",
        "surface": "Smooth tarmac",
        "gradient": "Flat (<1%)",
        "lighting": "Well lit",
        "features": ["Wheelchair ramps", "Tactile paving", "Audio signals", "Rest benches every 200m"],
        "tags": ["wheelchair", "visual", "family"],
        "accessibility_score": 98,
        "verified": True,
        "coordinates": [
            [11.0168, 76.9558],[11.0180, 76.9570],[11.0195, 76.9585],
            [11.0205, 76.9565],[11.0190, 76.9545],[11.0168, 76.9558]
        ]
    },
    {
        "id": 2,
        "name": "Gandhipuram Market Route",
        "description": "Urban accessible corridor with dropped kerbs and cleared footpaths.",
        "distance": "1.5 km",
        "duration": "18 min",
        "surface": "Concrete",
        "gradient": "Flat (<2%)",
        "lighting": "Brightly lit",
        "features": ["Dropped kerbs", "Wide pavements", "Braille signage", "Low-floor buses"],
        "tags": ["wheelchair", "visual", "transit"],
        "accessibility_score": 92,
        "verified": True,
        "coordinates": [
            [11.0230, 76.9650],[11.0240, 76.9660],[11.0250, 76.9670],
            [11.0260, 76.9665],[11.0255, 76.9650]
        ]
    },
    {
        "id": 3,
        "name": "Race Course Promenade",
        "description": "Scenic walkway with smooth surface and continuous handrails.",
        "distance": "2.2 km",
        "duration": "25 min",
        "surface": "Paved stone",
        "gradient": "Gentle (<3%)",
        "lighting": "Moderate",
        "features": ["Handrails", "Wide pathways", "Level crossings", "Accessible toilets"],
        "tags": ["wheelchair", "elderly", "scenic"],
        "accessibility_score": 88,
        "verified": True,
        "coordinates": [
            [11.0100, 76.9700],[11.0115, 76.9720],[11.0130, 76.9740],
            [11.0145, 76.9730],[11.0140, 76.9710]
        ]
    },
    {
        "id": 4,
        "name": "Brookefields Mall Link",
        "description": "Smooth, fully accessible route connecting the mall to the bus stand.",
        "distance": "0.8 km",
        "duration": "10 min",
        "surface": "Smooth tarmac",
        "gradient": "Flat (<1%)",
        "lighting": "Brightly lit",
        "features": ["Automatic doors", "Tactile strips", "Emergency call points", "Shelter"],
        "tags": ["wheelchair", "visual", "transit"],
        "accessibility_score": 96,
        "verified": True,
        "coordinates": [
            [11.0085, 76.9630],[11.0095, 76.9640],[11.0105, 76.9645],[11.0110, 76.9635]
        ]
    },
    {
        "id": 5,
        "name": "Singanallur Lake Path",
        "description": "Peaceful lakeside route with benches and accessible viewing points.",
        "distance": "3.5 km",
        "duration": "40 min",
        "surface": "Brick & tarmac",
        "gradient": "Moderate (<5%)",
        "lighting": "Well lit",
        "features": ["Accessible entry points", "Seating areas", "Accessible parking nearby", "Rest areas"],
        "tags": ["wheelchair", "elderly", "scenic"],
        "accessibility_score": 85,
        "verified": False,
        "coordinates": [
            [11.0050, 77.0000],[11.0065, 77.0015],[11.0080, 77.0030],
            [11.0095, 77.0020],[11.0090, 77.0005],[11.0070, 76.9995]
        ]
    }
]

# Coimbatore accessibility points
accessibility_points = [
    {"id": 1, "type": "ramp",    "name": "Wheelchair Ramp — RS Puram",   "lat": 11.0175, "lng": 76.9565, "status": "operational"},
    {"id": 2, "type": "toilet",  "name": "Accessible Toilet — Gandhipuram",           "lat": 11.0245, "lng": 76.9665, "status": "operational"},
    {"id": 3, "type": "bench",   "name": "Rest Bench — Race Course",          "lat": 11.0120, "lng": 76.9725, "status": "operational"},
    {"id": 4, "type": "audio",   "name": "Audio Crossing Signal — Brookefields",  "lat": 11.0100, "lng": 76.9638, "status": "operational"},
    {"id": 5, "type": "ramp",    "name": "Wheelchair Ramp — Singanallur",      "lat": 11.0070, "lng": 77.0010, "status": "maintenance"},
    {"id": 6, "type": "parking", "name": "Accessible Parking — Fun Mall",     "lat": 11.0135, "lng": 76.9755, "status": "operational"},
    {"id": 7, "type": "toilet",  "name": "Accessible Toilet — Prozone Mall",      "lat": 11.0145, "lng": 76.9762, "status": "operational"},
    {"id": 8, "type": "audio",   "name": "Audio Crossing — Avinashi Road",          "lat": 11.0258, "lng": 76.9668, "status": "operational"},
    {"id": 9, "type": "bench",   "name": "Rest Area — VOC Park",           "lat": 11.0098, "lng": 76.9710, "status": "operational"},
    {"id":10, "type": "parking", "name": "Accessible Parking — CMCH",       "lat": 11.0058, "lng": 76.9628, "status": "operational"},
]

# Pre-seed some example reports for Coimbatore
_seed_reports = [
    {"title": "Ramp blocked by construction barriers", "description": "The wheelchair ramp at RS Puram has been blocked for 2 weeks by construction equipment.", "location": "RS Puram, Coimbatore", "issue_type": "blocked_path", "severity": "high",     "lat": 11.0175, "lng": 76.9566, "upvotes": 7},
    {"title": "Cracked surface on Race Course path",     "description": "Large cracks on the paved section make it very difficult for wheelchair users.",                   "location": "Race Course, Coimbatore",  "issue_type": "poor_surface", "severity": "medium",   "lat": 11.0125, "lng": 76.9735, "upvotes": 4},
    {"title": "Audio signal not working",              "description": "The pedestrian audio crossing signal at Gandhipuram has been silent for over a week.",              "location": "Gandhipuram, Coimbatore",       "issue_type": "broken_signal","severity": "critical", "lat": 11.0258, "lng": 76.9668, "upvotes": 12},
]
for i, s in enumerate(_seed_reports):
    reports.append({
        "id": i + 1,
        "title": s["title"],
        "description": s["description"],
        "location": s["location"],
        "issue_type": s["issue_type"],
        "severity": s["severity"],
        "lat": s["lat"],
        "lng": s["lng"],
        "status": "open",
        "submitted_at": (datetime.now() - timedelta(hours=random.randint(2, 72))).isoformat(),
        "upvotes": s["upvotes"],
    })


# ── Pages ─────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def map_page():
    return render_template("map.html")

@app.route("/navigation")
def navigation_page():
    return render_template("navigation.html")

@app.route("/report")
def report_page():
    return render_template("report.html")

@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/color-demo")
def color_demo():
    return render_template("color_demo.html")

@app.route("/test-map")
def test_map():
    return render_template("test_map.html")


# ── API ────────────────────────────────────────────────────────
@app.route("/api/routes", methods=["GET"])
def get_routes():
    q     = request.args.get("q", "").lower()
    tag   = request.args.get("tag", "")
    min_s = int(request.args.get("min_score", 0))
    result = [
        r for r in accessible_routes
        if (not q or q in r["name"].lower() or q in r["description"].lower())
        and (not tag or tag in r.get("tags", []))
        and r["accessibility_score"] >= min_s
    ]
    return jsonify({"routes": result})

@app.route("/api/routes/<int:route_id>", methods=["GET"])
def get_route(route_id):
    route = next((r for r in accessible_routes if r["id"] == route_id), None)
    if not route:
        return jsonify({"error": "Not found"}), 404
    # Attach any open reports near this route
    nearby = [rep for rep in reports if rep["lat"] and rep["lng"]]
    return jsonify({"route": route, "nearby_reports": nearby[:3]})

@app.route("/api/points", methods=["GET"])
def get_points():
    status = request.args.get("status", "")
    ptype  = request.args.get("type", "")
    result = [
        p for p in accessibility_points
        if (not status or p["status"] == status)
        and (not ptype or p["type"] == ptype)
    ]
    return jsonify({"points": result})

@app.route("/api/reports", methods=["GET"])
def get_reports():
    status   = request.args.get("status", "")
    severity = request.args.get("severity", "")
    result   = [
        r for r in reports
        if (not status   or r["status"]   == status)
        and (not severity or r["severity"] == severity)
    ]
    return jsonify({"reports": result})

@app.route("/api/reports", methods=["POST"])
def submit_report():
    data = request.get_json()
    for field in ["title", "description", "location", "issue_type"]:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400
    report = {
        "id": len(reports) + 1,
        "title":       data["title"],
        "description": data["description"],
        "location":    data["location"],
        "issue_type":  data["issue_type"],
        "severity":    data.get("severity", "medium"),
        "lat":         data.get("lat"),
        "lng":         data.get("lng"),
        "status":      "open",
        "submitted_at": datetime.now().isoformat(),
        "upvotes":     0,
    }
    reports.append(report)
    return jsonify({"success": True, "report": report}), 201

@app.route("/api/reports/<int:report_id>/upvote", methods=["POST"])
def upvote_report(report_id):
    for r in reports:
        if r["id"] == report_id:
            r["upvotes"] += 1
            return jsonify({"success": True, "upvotes": r["upvotes"]})
    return jsonify({"error": "Not found"}), 404

@app.route("/api/reports/<int:report_id>/resolve", methods=["POST"])
def resolve_report(report_id):
    for r in reports:
        if r["id"] == report_id:
            r["status"] = "resolved"
            r["resolved_at"] = datetime.now().isoformat()
            return jsonify({"success": True})
    return jsonify({"error": "Not found"}), 404

@app.route("/api/stats", methods=["GET"])
def get_stats():
    by_type = {}
    by_severity = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for r in reports:
        by_type[r["issue_type"]] = by_type.get(r["issue_type"], 0) + 1
        by_severity[r.get("severity", "medium")] = by_severity.get(r.get("severity", "medium"), 0) + 1

    point_status = {"operational": 0, "maintenance": 0}
    for p in accessibility_points:
        point_status[p["status"]] = point_status.get(p["status"], 0) + 1

    return jsonify({
        "total_routes":            len(accessible_routes),
        "verified_routes":         sum(1 for r in accessible_routes if r.get("verified")),
        "total_points":            len(accessibility_points),
        "operational_points":      point_status["operational"],
        "maintenance_points":      point_status["maintenance"],
        "total_reports":           len(reports),
        "open_reports":            sum(1 for r in reports if r["status"] == "open"),
        "resolved_reports":        sum(1 for r in reports if r["status"] == "resolved"),
        "avg_accessibility_score": round(sum(r["accessibility_score"] for r in accessible_routes) / len(accessible_routes), 1),
        "reports_by_type":         by_type,
        "reports_by_severity":     by_severity,
        "route_scores":            [{"name": r["name"], "score": r["accessibility_score"]} for r in accessible_routes],
        "total_km_mapped":         round(sum(float(r["distance"].replace(" km","")) for r in accessible_routes), 1),
    })

# ── Nearby Help Places (Coimbatore) ───────────────────────────────────────
nearby_places = [
    # Hospitals in Coimbatore
    {"id":1,  "type":"hospital",  "name":"Coimbatore Medical College Hospital (CMCH)",          "address":"Avinashi Road, Coimbatore",       "phone":"0422-2530444", "accessible":True,  "lat":11.0058, "lng":76.9628, "open_24h":True},
    {"id":2,  "type":"hospital",  "name":"Kovai Medical Center and Hospital",       "address":"Avinashi Road, Coimbatore",     "phone":"0422-4324324", "accessible":True,  "lat":11.0240, "lng":76.9655, "open_24h":True},
    {"id":3,  "type":"hospital",  "name":"PSG Hospitals",                 "address":"Peelamedu, Coimbatore",  "phone":"0422-2570170", "accessible":True, "lat":11.0190, "lng":76.9710, "open_24h":True},
    {"id":4,  "type":"hospital",  "name":"Ganga Hospital",                "address":"313, Mettupalayam Road, Coimbatore",    "phone":"0422-2485000", "accessible":True,  "lat":11.0315, "lng":76.9675, "open_24h":True},
    {"id":5,  "type":"hospital",  "name":"Sri Ramakrishna Hospital",                "address":"395, Sarojini Street, Sidhapudur",    "phone":"0422-2473456", "accessible":True,  "lat":11.0045, "lng":76.9545, "open_24h":True},
    # Police Stations in Coimbatore
    {"id":6,  "type":"police",    "name":"RS Puram Police Station",          "address":"RS Puram, Coimbatore",  "phone":"100",           "accessible":True,  "lat":11.0155, "lng":76.9570, "open_24h":True},
    {"id":7,  "type":"police",    "name":"Gandhipuram Police Station",             "address":"Gandhipuram, Coimbatore",       "phone":"100",           "accessible":True, "lat":11.0220, "lng":76.9685, "open_24h":True},
    {"id":8,  "type":"police",    "name":"Race Course Police Station",       "address":"Race Course Road, Coimbatore",   "phone":"100",           "accessible":True,  "lat":11.0120, "lng":76.9758, "open_24h":True},
    {"id":9,  "type":"police",    "name":"Singanallur Police Station",        "address":"Singanallur, Coimbatore",        "phone":"100",           "accessible":False, "lat":11.0100, "lng":77.0005, "open_24h":True},
    # Accessible Places in Coimbatore
    {"id":10,  "type":"accessible","name":"Brookefields Mall",     "address":"Brookefields, Coimbatore",         "phone":"0422-4344344", "accessible":True,  "lat":11.0148, "lng":76.9708, "open_24h":False},
    {"id":11, "type":"accessible","name":"Fun Republic Mall",               "address":"Avinashi Road, Coimbatore",          "phone":"0422-4344555", "accessible":True,  "lat":11.0162, "lng":76.9792, "open_24h":False},
    {"id":12, "type":"accessible","name":"Prozone Mall",        "address":"Sathy Road, Coimbatore",         "phone":"0422-4344666", "accessible":True,  "lat":11.0205, "lng":76.9760, "open_24h":False},
    {"id":13, "type":"accessible","name":"VOC Park and Zoo",       "address":"VOC Park Road, Coimbatore",       "phone":"0422-2472777", "accessible":True,  "lat":11.0105, "lng":76.9720, "open_24h":False},
    {"id":14, "type":"accessible","name":"Coimbatore Railway Station",        "address":"Railway Station Road, Coimbatore",       "phone":"139", "accessible":True,  "lat":11.0070, "lng":76.9635, "open_24h":True},
    {"id":15, "type":"accessible","name":"Gandhipuram Bus Stand",        "address":"Gandhipuram, Coimbatore",  "phone":"0422-2472888", "accessible":True,  "lat":11.0245, "lng":76.9670, "open_24h":True},
]

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return round(R * 2 * math.asin(math.sqrt(a)), 2)

@app.route("/api/nearby", methods=["GET"])
def get_nearby():
    try:
        lat    = float(request.args.get("lat", 11.0168))  # Default to Coimbatore
        lng    = float(request.args.get("lng", 76.9558))
    except ValueError:
        return jsonify({"error": "Invalid coordinates"}), 400
    ptype  = request.args.get("type", "")   # hospital | police | accessible
    radius = float(request.args.get("radius", 5.0))  # km

    result = []
    for p in nearby_places:
        if ptype and p["type"] != ptype:
            continue
        dist = haversine(lat, lng, p["lat"], p["lng"])
        if dist <= radius:
            result.append({**p, "distance_km": dist})
    result.sort(key=lambda x: x["distance_km"])
    return jsonify({"places": result})


@app.route("/api/analyze-image", methods=["POST"])
def analyze_image():
    data     = request.get_json() or {}
    filename = (data.get("filename") or "").lower()
    b64      = data.get("image_b64", "")

    # Heuristic keyword rules — ordered by specificity
    rules = [
        (["ramp", "slope", "incline", "wheelchair"],          "broken_ramp",    "Damaged or Inaccessible Ramp",       "high",     "A ramp or sloped surface appears damaged or obstructed."),
        (["crack", "pothole", "broken", "damaged", "rough",
          "uneven", "surface", "pavement", "tarmac"],         "poor_surface",   "Damaged Pavement Surface",           "medium",   "The surface appears cracked, uneven, or damaged."),
        (["block", "obstruct", "barrier", "cone", "fence",
          "construction", "scaffold"],                        "blocked_path",   "Path Blocked by Obstruction",        "high",     "The path appears to be blocked or obstructed."),
        (["curb", "kerb", "cut", "drop", "crossing"],         "missing_curb",   "Missing or Damaged Curb Cut",        "medium",   "A curb cut or dropped kerb appears to be missing or damaged."),
        (["signal", "audio", "beep", "light", "traffic",
          "pedestrian", "crossing"],                          "broken_signal",  "Broken Pedestrian Signal",           "critical", "A pedestrian crossing signal appears to be broken or missing."),
        (["flood", "water", "puddle", "wet", "drain"],        "poor_surface",   "Flooding or Water Obstruction",      "high",     "Water or flooding is obstructing the accessible path."),
        (["step", "stair", "stairs"],                         "missing_curb",   "Unexpected Steps on Accessible Route","high",    "Steps detected on a route that should be step-free."),
    ]

    # Score each rule against filename + any readable b64 metadata
    text = filename
    best, best_score = None, 0
    for keywords, issue_type, title, severity, description in rules:
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best = (issue_type, title, severity, description)

    if best and best_score > 0:
        issue_type, title, severity, description = best
        confidence = min(round(40 + best_score * 20), 95)
    else:
        # Default fallback
        issue_type, title, severity, description = "other", "Accessibility Issue Detected", "medium", "An accessibility issue was detected in the uploaded image."
        confidence = 40

    return jsonify({
        "detected":    True,
        "issue_type":  issue_type,
        "title":       title,
        "severity":    severity,
        "description": description,
        "confidence":  confidence,
    })


@app.route("/api/calculate-routes", methods=["POST"])
def calculate_routes():
    """
    Calculate multiple routes with accessibility scores
    """
    data = request.get_json() or {}
    source = data.get('source')
    destination = data.get('destination')
    user_type = data.get('user_type', 'wheelchair')
    
    if not source or not destination:
        return jsonify({"error": "Source and destination required"}), 400
    
    # Generate routes
    routes = generate_routes(source, destination, user_type)
    
    # Find nearest facilities for each route
    for route in routes:
        route['nearest_hospital'] = find_nearest_facilities(
            route['coordinates'], nearby_places, 'hospital', 1
        )
        route['nearest_police'] = find_nearest_facilities(
            route['coordinates'], nearby_places, 'police', 1
        )
    
    return jsonify({"routes": routes, "user_type": user_type})

@app.route("/api/recommend", methods=["POST"])
def recommend_routes():
    data = request.get_json() or {}
    disability    = data.get("disability", "")
    max_gradient  = float(data.get("max_gradient", 5))
    min_score     = int(data.get("min_score", 0))
    avoid_reports = data.get("avoid_reports", True)
    max_distance  = float(data.get("max_distance", 99))

    open_report_count = sum(1 for r in reports if r["status"] == "open")
    gradient_map = {"Flat (<1%)": 0.5, "Flat (<2%)": 1.5, "Gentle (<3%)": 2.5, "Moderate (<5%)": 4.5}

    scored = []
    for route in accessible_routes:
        gradient_val = gradient_map.get(route["gradient"], 5.0)
        if gradient_val > max_gradient:
            continue
        if route["accessibility_score"] < min_score:
            continue
        if float(route["distance"].replace(" km", "")) > max_distance:
            continue

        score = route["accessibility_score"]
        if disability and disability in route.get("tags", []):
            score += 10
        if route.get("verified"):
            score += 5
        if route["lighting"] == "Brightly lit":
            score += 3
        elif route["lighting"] == "Well lit":
            score += 1
        if avoid_reports and open_report_count > 0:
            score -= min(open_report_count * 2, 10)
        score -= gradient_val * 1.5

        reasons = []
        if disability and disability in route.get("tags", []):
            reasons.append(f"Optimised for {disability} users")
        if route.get("verified"):
            reasons.append("Verified route")
        if gradient_val <= 1:
            reasons.append("Flat surface")
        if route["lighting"] in ("Brightly lit", "Well lit"):
            reasons.append("Good lighting")
        if route["accessibility_score"] >= 95:
            reasons.append("Top accessibility score")

        scored.append({**route, "ai_score": round(min(score, 100), 1), "reasons": reasons})

    scored.sort(key=lambda x: x["ai_score"], reverse=True)
    return jsonify({"recommendations": scored[:3]})


# ── Obstacle Management ───────────────────────────────────────
@app.route("/api/obstacles", methods=["GET"])
def get_obstacles():
    """Get all active obstacles"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM obstacles WHERE status = 'active' ORDER BY created_at DESC")
        obstacles = [dict(row) for row in c.fetchall()]
        conn.close()
        return jsonify({"obstacles": obstacles})
    except sqlite3.OperationalError:
        # Table doesn't exist yet
        return jsonify({"obstacles": []})

@app.route("/api/obstacles", methods=["POST"])
def report_obstacle():
    """Report a new obstacle"""
    data = request.get_json() or {}
    
    if not all(k in data for k in ['type', 'lat', 'lng']):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            INSERT INTO obstacles (type, description, lat, lng, severity, reported_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data['type'],
            data.get('description', ''),
            data['lat'],
            data['lng'],
            data.get('severity', 'medium'),
            data.get('reported_by', 'anonymous')
        ))
        conn.commit()
        obstacle_id = c.lastrowid
        conn.close()
        
        return jsonify({
            "success": True,
            "obstacle_id": obstacle_id,
            "message": "Obstacle reported successfully"
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/obstacles/<int:obstacle_id>/resolve", methods=["POST"])
def resolve_obstacle(obstacle_id):
    """Mark obstacle as resolved"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            UPDATE obstacles 
            SET status = 'resolved', resolved_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (obstacle_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Emergency Support ─────────────────────────────────────────
@app.route("/api/emergency", methods=["POST"])
def emergency_support():
    """Find nearest emergency facilities"""
    data = request.get_json() or {}
    
    try:
        lat = float(data.get('lat', 11.0168))  # Default to Coimbatore
        lng = float(data.get('lng', 76.9558))
    except ValueError:
        return jsonify({"error": "Invalid coordinates"}), 400
    
    # Find nearest hospital and police station
    hospitals = [p for p in nearby_places if p['type'] == 'hospital']
    police = [p for p in nearby_places if p['type'] == 'police']
    
    # Calculate distances
    for place in hospitals + police:
        place['distance_km'] = haversine(lat, lng, place['lat'], place['lng'])
    
    hospitals.sort(key=lambda x: x['distance_km'])
    police.sort(key=lambda x: x['distance_km'])
    
    return jsonify({
        "nearest_hospital": hospitals[0] if hospitals else None,
        "nearest_police": police[0] if police else None,
        "all_hospitals": hospitals[:3],
        "all_police": police[:3],
        "emergency_numbers": {
            "ambulance": "108",
            "police": "100",
            "fire": "101",
            "disaster": "1077"
        }
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)