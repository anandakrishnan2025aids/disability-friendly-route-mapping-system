js = """// AccessRoute Map JS
const DEFAULT_CENTER = [11.0168, 76.9558]; // Coimbatore, Tamil Nadu
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

function makeIcon(color, emoji) {
    return L.divIcon({
        className: '',
        html: '<div style="background:' + color + ';border:2px solid rgba(0,0,0,0.3);border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-size:14px;box-shadow:0 2px 8px rgba(0,0,0,0.4);">' + emoji + '</div>',
        iconSize: [32, 32],
        iconAnchor: [16, 16],
    });
}

const icons = {
    ramp: makeIcon('#ff5c7a', '♿'),
    toilet: makeIcon('#5b9dff', '🚻'),
    bench: makeIcon('#c084fc', '🪑'),
    audio: makeIcon('#ffc35a', '🔊'),
    parking: makeIcon('#22d3ee', '🅿️'),
    report: makeIcon('#ef4444', '⚠️'),
};

let routeLayers = [];
let pointMarkers = [];
let reportMarkers = [];

async function loadRoutes() {
    const res = await fetch('/api/routes');
    const data = await res.json();
    const list = document.getElementById('routesList');
    list.innerHTML = '';

    data.routes.forEach(route => {
        const poly = L.polyline(route.coordinates, {
            color: '#10e8b8',
            weight: 5,
            opacity: 0.9,
        }).addTo(map);

        poly.bindPopup('<div style="font-family:sans-serif;min-width:200px;background:#111827;color:#e8eeff;padding:4px;"><strong style="font-size:1rem;">' + route.name + '</strong><p style="font-size:0.82rem;color:#7a8aaa;margin:0.35rem 0;">' + route.description + '</p><span style="font-size:0.78rem;font-weight:700;background:rgba(16,232,184,0.15);color:#10e8b8;padding:0.15rem 0.5rem;border-radius:50px;">' + route.accessibility_score + '% accessible</span></div>');
        routeLayers.push({ id: route.id, layer: poly });

        const scoreClass = route.accessibility_score >= 90 ? 'score-high' : route.accessibility_score >= 75 ? 'score-med' : 'score-low';
        const item = document.createElement('div');
        item.className = 'route-item';
        item.dataset.routeId = route.id;
        item.innerHTML = '<div class="route-name">' + route.name + '</div><div class="route-desc">' + route.description + '</div><div class="route-meta"><span class="route-distance">📏 ' + route.distance + '</span><span class="score-badge ' + scoreClass + '">' + route.accessibility_score + '%</span></div><div class="route-features">' + route.features.map(f => '<span class="feature-tag">' + f + '</span>').join('') + '</div>';
        item.addEventListener('click', () => selectRoute(route.id, route.coordinates));
        list.appendChild(item);
    });
}

function selectRoute(id, coords) {
    document.querySelectorAll('.route-item').forEach(el => el.classList.remove('selected'));
    document.querySelector('[data-route-id="' + id + '"]').classList.add('selected');
    const bounds = L.latLngBounds(coords);
    map.fitBounds(bounds, { padding: [40, 40] });
}

async function loadPoints() {
    const res = await fetch('/api/points');
    const data = await res.json();
    data.points.forEach(pt => {
        const icon = icons[pt.type] || icons.ramp;
        const marker = L.marker([pt.lat, pt.lng], { icon }).addTo(map);
        marker.bindPopup('<div style="font-family:sans-serif;background:#111827;color:#e8eeff;padding:4px;"><strong>' + pt.name + '</strong><br/><span style="font-size:0.75rem;background:rgba(16,232,184,0.14);color:#10e8b8;padding:0.15rem 0.5rem;border-radius:50px;">' + pt.status + '</span></div>');
        pointMarkers.push(marker);
    });
}

async function loadReports() {
    const res = await fetch('/api/reports');
    const data = await res.json();
    reportMarkers.forEach(m => map.removeLayer(m));
    reportMarkers = [];
    data.reports.forEach(r => {
        if (!r.lat || !r.lng) return;
        const marker = L.marker([r.lat, r.lng], { icon: icons.report }).addTo(map);
        marker.bindPopup('<div style="font-family:sans-serif;background:#111827;color:#e8eeff;padding:4px;"><strong>' + r.title + '</strong><p style="font-size:0.82rem;color:#7a8aaa;margin:0.35rem 0;">' + r.description + '</p></div>');
        reportMarkers.push(marker);
    });
}

document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        routeLayers.forEach(r => { if (filter === 'all' || filter === 'routes') map.addLayer(r.layer); else map.removeLayer(r.layer); });
        pointMarkers.forEach(m => { if (filter === 'all' || filter === 'points') map.addLayer(m); else map.removeLayer(m); });
        reportMarkers.forEach(m => { if (filter === 'all' || filter === 'reports') map.addLayer(m); else map.removeLayer(m); });
    });
});

document.getElementById('locateMe').addEventListener('click', () => {
    if (!navigator.geolocation) return alert('Geolocation not supported.');
    navigator.geolocation.getCurrentPosition(pos => {
        map.setView([pos.coords.latitude, pos.coords.longitude], 15);
    }, () => alert('Could not get your location.'));
});

document.getElementById('resetView').addEventListener('click', () => {
    map.setView(DEFAULT_CENTER, DEFAULT_ZOOM);
});

loadRoutes();
loadPoints();
loadReports();
"""

with open('static/js/map.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('map.js written successfully!')

report_js = """let reportMap, reportMarker;
let selectedLat = null, selectedLng = null;
let currentStep = 1;

function goToStep(n) {
    if (n === 2 && !validateStep1()) return;
    if (n === 3 && !validateStep2()) return;
    currentStep = n;
    document.querySelectorAll('.form-step').forEach((s, i) => { s.classList.toggle('hidden', i + 1 !== n); });
    document.querySelectorAll('.step').forEach((s, i) => { s.classList.toggle('active', i + 1 === n); s.classList.toggle('done', i + 1 < n); });
    if (n === 2 && !reportMap) initReportMap();
    if (n === 3) buildReview();
}

function validateStep1() {
    let ok = true;
    const issueType = document.querySelector('input[name="issue_type"]:checked');
    const title = document.getElementById('title').value.trim();
    const desc = document.getElementById('description').value.trim();
    setError('issueTypeError', !issueType, 'Please select an issue type.');
    setError('titleError', !title, 'Please enter a title.');
    setError('descriptionError', !desc, 'Please describe the issue.');
    if (!issueType || !title || !desc) ok = false;
    return ok;
}

function validateStep2() {
    const loc = document.getElementById('location').value.trim();
    setError('locationError', !loc, 'Please enter a location.');
    return !!loc;
}

function setError(id, show, msg) {
    const el = document.getElementById(id);
    if (el) el.textContent = show ? msg : '';
}

function initReportMap() {
    reportMap = L.map('reportMap').setView([11.0168, 76.9558], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap contributors' }).addTo(reportMap);
    reportMap.on('click', e => {
        selectedLat = e.latlng.lat.toFixed(5);
        selectedLng = e.latlng.lng.toFixed(5);
        document.getElementById('coordsDisplay').textContent = '📍 ' + selectedLat + ', ' + selectedLng;
        if (reportMarker) reportMap.removeLayer(reportMarker);
        reportMarker = L.marker(e.latlng).addTo(reportMap);
    });
}

function buildReview() {
    const issueType = document.querySelector('input[name="issue_type"]:checked')?.value || '';
    const title = document.getElementById('title').value.trim();
    const desc = document.getElementById('description').value.trim();
    const severity = document.querySelector('input[name="severity"]:checked')?.value || 'medium';
    const location = document.getElementById('location').value.trim();
    document.getElementById('reviewBox').innerHTML = '<div class="review-row"><span class="review-label">Issue Type</span><span class="review-value">' + issueType.replace(/_/g, ' ') + '</span></div><div class="review-row"><span class="review-label">Title</span><span class="review-value">' + title + '</span></div><div class="review-row"><span class="review-label">Description</span><span class="review-value">' + desc + '</span></div><div class="review-row"><span class="review-label">Severity</span><span class="review-value">' + severity.toUpperCase() + '</span></div><div class="review-row"><span class="review-label">Location</span><span class="review-value">' + location + '</span></div>' + (selectedLat ? '<div class="review-row"><span class="review-label">Coordinates</span><span class="review-value" style="font-family:monospace;">' + selectedLat + ', ' + selectedLng + '</span></div>' : '');
}

document.getElementById('reportForm').addEventListener('submit', async e => {
    e.preventDefault();
    const btn = document.getElementById('submitBtn');
    btn.disabled = true;
    const payload = {
        issue_type: document.querySelector('input[name="issue_type"]:checked')?.value,
        title: document.getElementById('title').value.trim(),
        description: document.getElementById('description').value.trim(),
        severity: document.querySelector('input[name="severity"]:checked')?.value || 'medium',
        location: document.getElementById('location').value.trim(),
        lat: selectedLat ? parseFloat(selectedLat) : null,
        lng: selectedLng ? parseFloat(selectedLng) : null,
    };
    try {
        const res = await fetch('/api/reports', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        if (res.ok) {
            document.getElementById('reportFormCard').classList.add('hidden');
            document.getElementById('successCard').classList.remove('hidden');
            loadRecentReports();
        } else { alert('Submission failed. Please try again.'); }
    } catch { alert('Network error. Please try again.'); }
    btn.disabled = false;
});

function resetForm() {
    document.getElementById('reportFormCard').classList.remove('hidden');
    document.getElementById('successCard').classList.add('hidden');
    document.getElementById('reportForm').reset();
    goToStep(1);
    selectedLat = null; selectedLng = null;
    document.getElementById('coordsDisplay').textContent = '';
    if (reportMarker && reportMap) { reportMap.removeLayer(reportMarker); reportMarker = null; }
}

async function loadRecentReports() {
    const res = await fetch('/api/reports');
    const data = await res.json();
    const container = document.getElementById('recentReports');
    if (!data.reports.length) { container.innerHTML = '<p class="no-reports">No reports yet. Be the first!</p>'; return; }
    const sorted = [...data.reports].reverse().slice(0, 8);
    container.innerHTML = sorted.map(r => '<div class="report-card"><div class="report-card-title">' + r.title + '</div><div class="report-card-meta"><span class="report-type-badge">' + r.issue_type.replace(/_/g, ' ') + '</span><span class="report-time">' + timeAgo(r.submitted_at) + '</span><button class="upvote-btn" onclick="upvote(' + r.id + ', this)">▲ ' + r.upvotes + '</button></div></div>').join('');
}

async function upvote(id, btn) {
    const res = await fetch('/api/reports/' + id + '/upvote', { method: 'POST' });
    const data = await res.json();
    if (data.success) btn.textContent = '▲ ' + data.upvotes;
}

function timeAgo(iso) {
    const diff = Date.now() - new Date(iso).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return mins + 'm ago';
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return hrs + 'h ago';
    return Math.floor(hrs / 24) + 'd ago';
}

loadRecentReports();
"""

with open('static/js/report.js', 'w', encoding='utf-8') as f:
    f.write(report_js)
print('report.js written successfully!')

with open('static/js/main.js', 'w', encoding='utf-8') as f:
    f.write("function toggleMenu(){const m=document.getElementById('mobileMenu');if(m)m.classList.toggle('open');}")
print('main.js written successfully!')

print('\nAll JS files written! Now run: python app.py')