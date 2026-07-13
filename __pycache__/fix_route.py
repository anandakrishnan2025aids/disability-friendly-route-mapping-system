# Fix app.py routes with Coimbatore coordinates
app_code = '''from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

reports = []

accessible_routes = [
    {
        "id": 1,
        "name": "Gandhipuram Central Loop",
        "description": "Fully paved flat route through Gandhipuram bus stand area with tactile guides.",
        "distance": "2.1 km",
        "duration": "25 min",
        "surface": "Smooth tarmac",
        "gradient": "Flat (<1%)",
        "lighting": "Well lit",
        "features": ["Wheelchair ramps", "Tactile paving", "Audio signals", "Rest benches"],
        "tags": ["wheelchair", "visual", "family"],
        "accessibility_score": 98,
        "verified": True,
        "coordinates": [
            [11.0168, 76.9558],
            [11.0180, 76.9570],
            [11.0195, 76.9580],
            [11.0210, 76.9575],
            [11.0205, 76.9560],
            [11.0168, 76.9558]
        ]
    },
    {
        "id": 2,
        "name": "RS Puram Riverside Walk",
        "description": "Scenic accessible walkway along Noyyal river with smooth surface and handrails.",
        "distance": "1.8 km",
        "duration": "20 min",
        "surface": "Paved stone",
        "gradient": "Gentle (<3%)",
        "lighting": "Moderate",
        "features": ["Handrails", "Wide pathways", "Level crossings", "Accessible toilets"],
        "tags": ["wheelchair", "elderly", "scenic"],
        "accessibility_score": 92,
        "verified": True,
        "coordinates": [
            [11.0050, 76.9600],
            [11.0065, 76.9620],
            [11.0080, 76.9640],
            [11.0095, 76.9630],
            [11.0090, 76.9610]
        ]
    },
    {
        "id": 3,
        "name": "Market Street Accessible Route",
        "description": "Urban accessible corridor through Coimbatore market with dropped kerbs.",
        "distance": "0.9 km",
        "duration": "12 min",
        "surface": "Concrete",
        "gradient": "Flat (<2%)",
        "lighting": "Brightly lit",
        "features": ["Dropped kerbs", "Wide pavements", "Braille signage", "Low-floor buses"],
        "tags": ["wheelchair", "visual", "transit"],
        "accessibility_score": 85,
        "verified": True,
        "coordinates": [
            [11.0120, 76.9650],
            [11.0130, 76.9660],
            [11.0140, 76.9670],
            [11.0150, 76.9665],
            [11.0145, 76.9650]
        ]
    },
    {
        "id": 4,
        "name": "Coimbatore Railway Station Path",
        "description": "Accessible route from railway station to main bus stand with shelter.",
        "distance": "1.2 km",
        "duration": "15 min",
        "surface": "Smooth tarmac",
        "gradient": "Flat (<1%)",
        "lighting": "Brightly lit",
        "features": ["Automatic doors", "Tactile strips", "Shelter", "Seating areas"],
        "tags": ["wheelchair", "visual", "transit"],
        "accessibility_score": 96,
        "verified": True,
        "coordinates": [
            [11.0010, 76.9630],
            [11.0025, 76.9640],
            [11.0040, 76.9650],
            [11.0055, 76.9645]
        ]
    },
    {
        "id": 5,
        "name": "KMCH Hospital Accessible Link",
        "description": "Smooth fully accessible route connecting KMCH hospital to main road.",
        "distance": "0.6 km",
        "duration": "8 min",
        "surface": "Smooth tarmac",
        "gradient": "Flat (<1%)",
        "lighting": "Brightly lit",
        "features": ["Automatic doors", "Tactile strips", "Emergency call points", "Shelter"],
        "tags": ["wheelchair", "visual", "medical"],
        "accessibility_score": 96,
        "verified": True,
        "coordinates": [
            [11.0250, 76.9500],
            [11.0260, 76.9510],
            [11.0270, 76.9520],
            [11.0275, 76.9510]
        ]
    }
]

accessibility_points = [
    {"id": 1,  "type": "ramp",    "name": "Wheelchair Ramp - Gandhipuram",     "lat": 11.0170, "lng": 76.9560, "status": "operational"},
    {"id": 2,  "type": "toilet",  "name": "Accessible Toilet - Bus Stand",      "lat": 11.0185, "lng": 76.9572, "status": "operational"},
    {"id": 3,  "type": "bench",   "name": "Rest Bench - Gandhipuram",           "lat": 11.0195, "lng": 76.9578, "status": "operational"},
    {"id": 4,  "type": "audio",   "name": "Audio Signal - Gandhipuram Junction","lat": 11.0160, "lng": 76.9550, "status": "operational"},
    {"id": 5,  "type": "ramp",    "name": "Wheelchair Ramp - RS Puram",         "lat": 11.0065, "lng": 76.9622, "status": "maintenance"},
    {"id": 6,  "type": "parking", "name": "Accessible Parking - Market",        "lat": 11.0130, "lng": 76.9658, "status": "operational"},
    {"id": 7,  "type": "toilet",  "name": "Accessible Toilet - Market",         "lat": 11.0140, "lng": 76.9665, "status": "operational"},
    {"id": 8,  "type": "audio",   "name": "Audio Signal - Market Square",       "lat": 11.0145, "lng": 76.9670, "status": "operational"},
    {"id": 9,  "type": "bench",   "name": "Rest Bench - Railway Station",       "lat": 11.0025, "lng": 76.9638, "status": "operational"},
    {"id": 10, "type": "parking", "name": "Accessible Parking - KMCH Hospital", "lat": 11.0255, "lng": 76.9505, "status": "operational"},
]

_seed_reports = [
    {"title": "Ramp blocked at Gandhipuram",    "description": "Wheelchair ramp at Gandhipuram bus stand blocked by construction.", "location": "Gandhipuram Bus Stand",    "issue_type": "blocked_path",  "severity": "high",     "lat": 11.0172, "lng": 76.9562, "upvotes": 7},
    {"title": "Broken surface on RS Puram walk","description": "Large cracks on the paved section near RS Puram river walk.",       "location": "RS Puram Riverside Walk", "issue_type": "poor_surface",  "severity": "medium",   "lat": 11.0080, "lng": 76.9638, "upvotes": 4},
    {"title": "Audio signal not working",       "description": "Pedestrian audio signal at Market Square has been silent.",          "location": "Market Square Junction",  "issue_type": "broken_signal", "severity": "critical", "lat": 11.0145, "lng": 76.9670, "upvotes": 12},
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def map_page():
    return render_template("map.html")

@app.route("/report")
def report_page():
    return render_template("report.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

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

@app.route("/api/points", methods=["GET"])
def get_points():
    return jsonify({"points": accessibility_points})

@app.route("/api/reports", methods=["GET"])
def get_reports():
    return jsonify({"reports": reports})

@app.route("/api/reports", methods=["POST"])
def submit_report():
    data = request.get_json()
    for field in ["title", "description", "location", "issue_type"]:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400
    report = {
        "id": len(reports) + 1,
        "title":        data["title"],
        "description":  data["description"],
        "location":     data["location"],
        "issue_type":   data["issue_type"],
        "severity":     data.get("severity", "medium"),
        "lat":          data.get("lat"),
        "lng":          data.get("lng"),
        "status":       "open",
        "submitted_at": datetime.now().isoformat(),
        "upvotes":      0,
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

@app.route("/api/stats", methods=["GET"])
def get_stats():
    return jsonify({
        "total_routes":            len(accessible_routes),
        "total_points":            len(accessibility_points),
        "total_reports":           len(reports),
        "open_reports":            sum(1 for r in reports if r["status"] == "open"),
        "avg_accessibility_score": round(sum(r["accessibility_score"] for r in accessible_routes) / len(accessible_routes), 1),
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)
print('app.py fixed with Coimbatore coordinates!')
print('Now run: python app.py')