import os

# ── New map.html using Google Maps ──
map_html = """{% extends "base.html" %}
{% block title %}Accessible Routes Map — AccessRoute{% endblock %}
{% block head %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/map.css') }}" />
<style>
#map { width:100%; height:100%; }
.search-box {
    padding:1rem 1.5rem;
    border-bottom:1px solid var(--border);
    background:var(--bg2);
}
.search-box input {
    width:100%;
    font-family:var(--bd);
    font-size:.88rem;
    padding:.7rem 1rem;
    border:1px solid var(--border);
    border-radius:10px;
    background:var(--surface3);
    color:var(--text);
    outline:none;
    transition:all .2s;
}
.search-box input:focus {
    border-color:rgba(16,232,184,.45);
    background:var(--surface2);
    box-shadow:0 0 0 3px rgba(16,232,184,.07);
}
.search-box input::placeholder { color:var(--text-dim); }
.gm-style .gm-style-iw-c {
    background:#111827 !important;
    color:#e8eeff !important;
    border-radius:12px !important;
}
.gm-style .gm-style-iw-d { color:#e8eeff !important; }
.gm-style .gm-style-iw-t::after { background:#111827 !important; }
.route-panel {
    background:var(--surface2);
    border:1px solid rgba(16,232,184,.3);
    border-radius:var(--r);
    padding:1rem 1.2rem;
    margin-bottom:.75rem;
    cursor:pointer;
    transition:all .2s;
}
.route-panel:hover { border-color:rgba(16,232,184,.6); box-shadow:0 0 16px rgba(16,232,184,.1); }
.route-panel.active { border-color:var(--accent); background:var(--accent-dim); }
.rp-name { font-family:var(--hd); font-weight:700; font-size:.95rem; margin-bottom:.35rem; }
.rp-meta { display:flex; gap:.5rem; flex-wrap:wrap; margin-bottom:.5rem; }
.rp-pill { font-size:.7rem; font-weight:600; padding:.18rem .55rem; border-radius:50px; background:var(--surface3); border:1px solid var(--border); color:var(--text-muted); }
.rp-btn { width:100%; font-size:.78rem; font-weight:700; padding:.5rem; border-radius:8px; border:1px solid rgba(16,232,184,.3); background:var(--accent-dim); color:var(--accent); cursor:pointer; transition:all .2s; font-family:var(--bd); }
.rp-btn:hover { background:var(--accent); color:#060b18; }
</style>
{% endblock %}

{% block content %}
<div class="map-page">
    <aside class="map-sidebar">
        <div class="sidebar-header">
            <h2>Accessible Routes</h2>
            <p>Coimbatore city — verified routes</p>
        </div>

        <div class="search-box">
            <input type="text" id="searchBox" placeholder="🔍  Search routes or places..." />
        </div>

        <div class="filter-bar">
            <button class="filter-btn active" data-filter="all">All</button>
            <button class="filter-btn" data-filter="routes">Routes</button>
            <button class="filter-btn" data-filter="points">Points</button>
            <button class="filter-btn" data-filter="reports">Reports</button>
        </div>

        <div class="routes-list" id="routesList">
            <div class="loading-spinner">Loading routes…</div>
        </div>

        <div class="legend">
            <div class="legend-title">Map Legend</div>
            <div class="legend-item"><span class="legend-dot route-dot"></span>Accessible Route</div>
            <div class="legend-item"><span class="legend-dot ramp-dot"></span>Wheelchair Ramp</div>
            <div class="legend-item"><span class="legend-dot toilet-dot"></span>Accessible Toilet</div>
            <div class="legend-item"><span class="legend-dot bench-dot"></span>Rest Bench</div>
            <div class="legend-item"><span class="legend-dot audio-dot"></span>Audio Signal</div>
            <div class="legend-item"><span class="legend-dot parking-dot"></span>Accessible Parking</div>
            <div class="legend-item"><span class="legend-dot report-dot"></span>Community Report</div>
        </div>
    </aside>

    <div class="map-container">
        <div id="map"></div>
        <div class="map-controls">
            <button class="map-ctrl-btn" id="locateMe" title="My Location">📍</button>
            <button class="map-ctrl-btn" id="resetView" title="Reset View">⌂</button>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/map.js') }}"></script>
<script>
function initMap() {
    window.mapReady = true;
    if (window.mapInitCallback) window.mapInitCallback();
}
</script>
<script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY&callback=initMap&libraries=geometry">
</script>
{% endblock %}
"""

with open('templates/map.html', 'w', encoding='utf-8') as f:
    f.write(map_html)
print('map.html written!')

# ── New map.js using Google Maps ──
map_js = """
// AccessRoute — Google Maps version
const DEFAULT_CENTER = { lat: 11.0168, lng: 76.9558 }; // Coimbatore
const DEFAULT_ZOOM   = 14;

let gmap, allRoutes = [];
let routePolylines = [], pointMarkers = [], reportMarkers = [];
let infoWindow;

function initGoogleMap() {
    gmap = new google.maps.Map(document.getElementById('map'), {
        center: DEFAULT_CENTER,
        zoom:   DEFAULT_ZOOM,
        mapId:  'DEMO_MAP_ID',
        styles: [
            { elementType: 'geometry',        stylers: [{ color: '#1a1f2e' }] },
            { elementType: 'labels.text.fill', stylers: [{ color: '#8892b0' }] },
            { elementType: 'labels.text.stroke',stylers:[{ color: '#0d1120' }] },
            { featureType: 'road',             elementType: 'geometry',        stylers: [{ color: '#2d3561' }] },
            { featureType: 'road',             elementType: 'geometry.stroke', stylers: [{ color: '#1a1f2e' }] },
            { featureType: 'road.highway',     elementType: 'geometry',        stylers: [{ color: '#3d4a7a' }] },
            { featureType: 'water',            elementType: 'geometry',        stylers: [{ color: '#0d2137' }] },
            { featureType: 'poi.park',         elementType: 'geometry',        stylers: [{ color: '#0d2d1a' }] },
            { featureType: 'poi',              stylers: [{ visibility: 'off' }]},
            { featureType: 'transit',          stylers: [{ visibility: 'off' }]},
            { featureType: 'administrative',   elementType: 'geometry',        stylers: [{ color: '#2d3561' }] },
        ],
        disableDefaultUI: false,
        zoomControl: true,
        streetViewControl: false,
        mapTypeControl: false,
        fullscreenControl: true,
    });

    infoWindow = new google.maps.InfoWindow({
        pixelOffset: new google.maps.Size(0, -10)
    });

    loadRoutes();
    loadPoints();
    loadReports();
}

// ── Wait for Google Maps to load ──
window.mapInitCallback = initGoogleMap;
if (window.mapReady) initGoogleMap();

// ── Routes ──
async function loadRoutes() {
    const res  = await fetch('/api/routes');
    const data = await res.json();
    allRoutes  = data.routes;
    renderRouteList(allRoutes);

    allRoutes.forEach(route => {
        const path = route.coordinates.map(c => ({ lat: c[0], lng: c[1] }));
        const poly = new google.maps.Polyline({
            path:          path,
            geodesic:      true,
            strokeColor:   '#10e8b8',
            strokeOpacity: 0.9,
            strokeWeight:  5,
            map:           gmap,
        });

        poly.addListener('click', e => {
            infoWindow.setContent(buildRoutePopup(route));
            infoWindow.setPosition(e.latLng);
            infoWindow.open(gmap);
        });

        routePolylines.push({ id: route.id, poly: poly });
    });
}

function buildRoutePopup(route) {
    const scoreColor = route.accessibility_score >= 90 ? '#10e8b8' : route.accessibility_score >= 75 ? '#ffc35a' : '#ff5c7a';
    return '<div style="font-family:sans-serif;min-width:220px;max-width:280px;background:#111827;color:#e8eeff;padding:8px;border-radius:8px;">' +
        '<div style="font-size:1rem;font-weight:700;margin-bottom:6px;">' + route.name + '</div>' +
        '<div style="font-size:.82rem;color:#7a8aaa;margin-bottom:8px;">' + route.description + '</div>' +
        '<div style="display:flex;gap:6px;flex-wrap:wrap;">' +
        '<span style="font-size:.75rem;font-weight:700;background:rgba(16,232,184,.15);color:' + scoreColor + ';padding:2px 8px;border-radius:50px;">' + route.accessibility_score + '% accessible</span>' +
        '<span style="font-size:.75rem;color:#7a8aaa;padding:2px 6px;">📏 ' + route.distance + '</span>' +
        '<span style="font-size:.75rem;color:#7a8aaa;padding:2px 6px;">⏱ ' + (route.duration || '') + '</span>' +
        '</div>' +
        '<div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:4px;">' +
        (route.features || []).slice(0,3).map(f =>
            '<span style="font-size:.7rem;background:#1f2640;border:1px solid rgba(255,255,255,.1);color:#8892b0;padding:2px 7px;border-radius:4px;">' + f + '</span>'
        ).join('') +
        '</div></div>';
}

function renderRouteList(routes) {
    const list = document.getElementById('routesList');
    if (!routes.length) {
        list.innerHTML = '<div style="text-align:center;padding:2rem;color:var(--text-muted);font-size:.88rem;">No routes found.</div>';
        return;
    }
    list.innerHTML = routes.map(route => {
        const sc = route.accessibility_score >= 90 ? 'score-high' : route.accessibility_score >= 75 ? 'score-med' : 'score-low';
        return '<div class="route-panel" id="rp-' + route.id + '" onclick="selectRoute(' + route.id + ')">' +
            '<div class="rp-name">' + route.name + '</div>' +
            '<div class="rp-meta">' +
            '<span class="rp-pill">📏 ' + route.distance + '</span>' +
            (route.duration ? '<span class="rp-pill">⏱ ' + route.duration + '</span>' : '') +
            '<span class="score-badge ' + sc + '">' + route.accessibility_score + '%</span>' +
            '</div>' +
            '<div style="font-size:.78rem;color:var(--text-muted);margin-bottom:.6rem;line-height:1.5;">' + route.description + '</div>' +
            '<button class="rp-btn" onclick="event.stopPropagation();selectRoute(' + route.id + ')">Show on Map →</button>' +
            '</div>';
    }).join('');
}

function selectRoute(id) {
    // Reset all styles
    routePolylines.forEach(r => {
        r.poly.setOptions({ strokeColor: '#10e8b8', strokeWeight: 5 });
    });
    document.querySelectorAll('.route-panel').forEach(el => el.classList.remove('active'));

    // Highlight selected
    const found = routePolylines.find(r => r.id === id);
    const route = allRoutes.find(r => r.id === id);

    if (found && route) {
        found.poly.setOptions({ strokeColor: '#ffc35a', strokeWeight: 8 });
        const el = document.getElementById('rp-' + id);
        if (el) { el.classList.add('active'); el.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }

        // Fit bounds
        const bounds = new google.maps.LatLngBounds();
        route.coordinates.forEach(c => bounds.extend({ lat: c[0], lng: c[1] }));
        gmap.fitBounds(bounds, { top: 60, right: 60, bottom: 60, left: 60 });

        // Show popup
        const center = bounds.getCenter();
        infoWindow.setContent(buildRoutePopup(route));
        infoWindow.setPosition(center);
        infoWindow.open(gmap);
    }
}

// ── Points ──
const POINT_ICONS = {
    ramp:    { text: '♿', bg: '#ff5c7a' },
    toilet:  { text: '🚻', bg: '#5b9dff' },
    bench:   { text: '🪑', bg: '#c084fc' },
    audio:   { text: '🔊', bg: '#ffc35a' },
    parking: { text: '🅿️', bg: '#22d3ee' },
    report:  { text: '⚠️', bg: '#ef4444' },
};

function makeMarkerIcon(type) {
    const ic = POINT_ICONS[type] || POINT_ICONS.ramp;
    return {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(
            '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36">' +
            '<circle cx="18" cy="18" r="16" fill="' + ic.bg + '" stroke="rgba(0,0,0,0.3)" stroke-width="2"/>' +
            '<text x="18" y="23" text-anchor="middle" font-size="14">' + ic.text + '</text>' +
            '</svg>'
        ),
        scaledSize: new google.maps.Size(36, 36),
        anchor:     new google.maps.Point(18, 18),
    };
}

async function loadPoints() {
    const res  = await fetch('/api/points');
    const data = await res.json();
    data.points.forEach(pt => {
        const marker = new google.maps.Marker({
            position: { lat: pt.lat, lng: pt.lng },
            map:      gmap,
            icon:     makeMarkerIcon(pt.type),
            title:    pt.name,
        });
        const statusColor = pt.status === 'operational' ? '#10e8b8' : '#ffc35a';
        marker.addListener('click', () => {
            infoWindow.setContent(
                '<div style="font-family:sans-serif;background:#111827;color:#e8eeff;padding:8px;border-radius:8px;min-width:180px;">' +
                '<div style="font-weight:700;margin-bottom:6px;">' + pt.name + '</div>' +
                '<span style="font-size:.75rem;padding:2px 8px;border-radius:50px;background:rgba(16,232,184,.14);color:' + statusColor + ';">' + pt.status + '</span>' +
                '</div>'
            );
            infoWindow.open(gmap, marker);
        });
        pointMarkers.push(marker);
    });
}

async function loadReports() {
    const res  = await fetch('/api/reports');
    const data = await res.json();
    reportMarkers.forEach(m => m.setMap(null));
    reportMarkers = [];
    data.reports.forEach(r => {
        if (!r.lat || !r.lng) return;
        const marker = new google.maps.Marker({
            position: { lat: r.lat, lng: r.lng },
            map:      gmap,
            icon:     makeMarkerIcon('report'),
            title:    r.title,
        });
        marker.addListener('click', () => {
            infoWindow.setContent(
                '<div style="font-family:sans-serif;background:#111827;color:#e8eeff;padding:8px;border-radius:8px;min-width:200px;">' +
                '<div style="font-weight:700;margin-bottom:4px;">' + r.title + '</div>' +
                '<div style="font-size:.82rem;color:#7a8aaa;margin-bottom:6px;">' + r.description + '</div>' +
                '<span style="font-size:.72rem;background:rgba(255,92,122,.15);color:#ff5c7a;padding:2px 8px;border-radius:50px;">' +
                r.issue_type.replace(/_/g,' ') + '</span>' +
                '</div>'
            );
            infoWindow.open(gmap, marker);
        });
        reportMarkers.push(marker);
    });
}

// ── Search ──
document.getElementById('searchBox').addEventListener('input', function() {
    const q = this.value.trim().toLowerCase();
    if (!q) {
        renderRouteList(allRoutes);
        routePolylines.forEach(r => r.poly.setMap(gmap));
        return;
    }
    const filtered = allRoutes.filter(r =>
        r.name.toLowerCase().includes(q) ||
        r.description.toLowerCase().includes(q) ||
        r.features.some(f => f.toLowerCase().includes(q))
    );
    renderRouteList(filtered);
    routePolylines.forEach(r => {
        r.poly.setMap(filtered.find(f => f.id === r.id) ? gmap : null);
    });
    if (filtered.length) selectRoute(filtered[0].id);
});

// ── Filter buttons ──
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const f = btn.dataset.filter;
        routePolylines.forEach(r  => r.poly.setMap(f==='all'||f==='routes' ? gmap : null));
        pointMarkers.forEach(m   => m.setMap(f==='all'||f==='points'  ? gmap : null));
        reportMarkers.forEach(m  => m.setMap(f==='all'||f==='reports' ? gmap : null));
    });
});

// ── Controls ──
document.getElementById('locateMe').addEventListener('click', () => {
    if (!navigator.geolocation) return alert('Geolocation not supported.');
    navigator.geolocation.getCurrentPosition(
        pos => { gmap.setCenter({ lat: pos.coords.latitude, lng: pos.coords.longitude }); gmap.setZoom(16); },
        ()  => alert('Could not get your location.')
    );
});
document.getElementById('resetView').addEventListener('click', () => {
    gmap.setCenter(DEFAULT_CENTER);
    gmap.setZoom(DEFAULT_ZOOM);
    routePolylines.forEach(r => r.poly.setOptions({ strokeColor: '#10e8b8', strokeWeight: 5 }));
});
"""

with open('static/js/map.js', 'w', encoding='utf-8') as f:
    f.write(map_js)
print('map.js written with Google Maps!')
print('\nDone! Now run: python app.py')
print('Open: http://127.0.0.1:5000/map')
print('Press Ctrl+Shift+R')