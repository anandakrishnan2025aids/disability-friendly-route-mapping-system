js = """
const DEFAULT_CENTER = [11.0168, 76.9558];
const DEFAULT_ZOOM = 14;

const map = L.map('map', { center: DEFAULT_CENTER, zoom: DEFAULT_ZOOM });

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19,
}).addTo(map);

function makeIcon(color, emoji) {
    return L.divIcon({
        className: '',
        html: '<div style="background:' + color + ';border:2px solid rgba(0,0,0,0.3);border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-size:14px;box-shadow:0 2px 8px rgba(0,0,0,0.4);">' + emoji + '</div>',
        iconSize: [32, 32], iconAnchor: [16, 16],
    });
}

const icons = {
    ramp:    makeIcon('#ff5c7a', '♿'),
    toilet:  makeIcon('#5b9dff', '🚻'),
    bench:   makeIcon('#c084fc', '🪑'),
    audio:   makeIcon('#ffc35a', '🔊'),
    parking: makeIcon('#22d3ee', '🅿️'),
    report:  makeIcon('#ef4444', '⚠️'),
};

let routeLayers = [];
let pointMarkers = [];
let reportMarkers = [];
let allRoutes = [];

async function loadRoutes() {
    const res = await fetch('/api/routes');
    const data = await res.json();
    allRoutes = data.routes;
    renderRouteList(allRoutes);
    allRoutes.forEach(route => drawRoute(route, '#10e8b8'));
}

function drawRoute(route, color) {
    const existing = routeLayers.find(r => r.id === route.id);
    if (existing) {
        existing.layer.setStyle({ color: color, weight: color === '#10e8b8' ? 5 : 8 });
        return;
    }
    const poly = L.polyline(route.coordinates, {
        color: color, weight: 5, opacity: 0.9,
    }).addTo(map);
    poly.bindPopup(
        '<div style="font-family:sans-serif;min-width:200px;background:#111827;color:#e8eeff;padding:6px;">' +
        '<strong style="font-size:1rem;">' + route.name + '</strong>' +
        '<p style="font-size:.82rem;color:#7a8aaa;margin:.35rem 0;">' + route.description + '</p>' +
        '<div style="display:flex;gap:.5rem;flex-wrap:wrap;">' +
        '<span style="font-size:.75rem;font-weight:700;background:rgba(16,232,184,.15);color:#10e8b8;padding:.15rem .5rem;border-radius:50px;">' + route.accessibility_score + '% score</span>' +
        '<span style="font-size:.75rem;color:#7a8aaa;">📏 ' + route.distance + '</span>' +
        '<span style="font-size:.75rem;color:#7a8aaa;">⏱ ' + route.duration + '</span>' +
        '</div></div>'
    );
    routeLayers.push({ id: route.id, layer: poly });
}

function renderRouteList(routes) {
    const list = document.getElementById('routesList');
    if (!routes.length) {
        list.innerHTML = '<div style="text-align:center;padding:2rem;color:var(--text-muted);font-size:.88rem;">No routes found.<br/>Try a different search.</div>';
        return;
    }
    list.innerHTML = routes.map(route => {
        const scoreClass = route.accessibility_score >= 90 ? 'score-high' : route.accessibility_score >= 75 ? 'score-med' : 'score-low';
        return '<div class="route-item" data-route-id="' + route.id + '" onclick="selectRoute(' + route.id + ')">' +
            '<div class="route-name">' + route.name + '</div>' +
            '<div class="route-desc">' + route.description + '</div>' +
            '<div class="route-meta">' +
            '<span class="route-distance">📏 ' + route.distance + '</span>' +
            '<span class="score-badge ' + scoreClass + '">' + route.accessibility_score + '%</span>' +
            '</div>' +
            '<div class="route-features">' +
            route.features.map(f => '<span class="feature-tag">' + f + '</span>').join('') +
            '</div>' +
            '</div>';
    }).join('');
}

function selectRoute(id) {
    document.querySelectorAll('.route-item').forEach(el => el.classList.remove('selected'));
    const el = document.querySelector('[data-route-id="' + id + '"]');
    if (el) { el.classList.add('selected'); el.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
    routeLayers.forEach(r => r.layer.setStyle({ color: '#10e8b8', weight: 5 }));
    const found = routeLayers.find(r => r.id === id);
    if (found) {
        found.layer.setStyle({ color: '#ffc35a', weight: 8 });
        const route = allRoutes.find(r => r.id === id);
        if (route) {
            map.fitBounds(L.latLngBounds(route.coordinates), { padding: [60, 60] });
            found.layer.openPopup();
        }
    }
}

async function loadPoints() {
    const res = await fetch('/api/points');
    const data = await res.json();
    data.points.forEach(pt => {
        const icon = icons[pt.type] || icons.ramp;
        const marker = L.marker([pt.lat, pt.lng], { icon }).addTo(map);
        marker.bindPopup(
            '<div style="font-family:sans-serif;background:#111827;color:#e8eeff;padding:4px;">' +
            '<strong>' + pt.name + '</strong><br/>' +
            '<span style="font-size:.75rem;padding:.15rem .5rem;border-radius:50px;background:' +
            (pt.status === 'operational' ? 'rgba(16,232,184,.14);color:#10e8b8' : 'rgba(255,195,90,.14);color:#ffc35a') +
            ';">' + pt.status + '</span></div>'
        );
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
        marker.bindPopup(
            '<div style="font-family:sans-serif;background:#111827;color:#e8eeff;padding:4px;min-width:180px;">' +
            '<strong>' + r.title + '</strong>' +
            '<p style="font-size:.82rem;color:#7a8aaa;margin:.35rem 0;">' + r.description + '</p>' +
            '<span style="font-size:.72rem;background:rgba(255,92,122,.15);color:#ff5c7a;padding:.15rem .5rem;border-radius:50px;">' +
            r.issue_type.replace(/_/g,' ') + '</span></div>'
        );
        reportMarkers.push(marker);
    });
}

// Search — filters existing routes, NO line drawing
const searchBox = document.getElementById('searchBox');
if (searchBox) {
    searchBox.addEventListener('input', function() {
        const q = this.value.trim().toLowerCase();
        if (!q) {
            renderRouteList(allRoutes);
            routeLayers.forEach(r => map.addLayer(r.layer));
            return;
        }
        const filtered = allRoutes.filter(r =>
            r.name.toLowerCase().includes(q) ||
            r.description.toLowerCase().includes(q) ||
            r.features.some(f => f.toLowerCase().includes(q))
        );
        renderRouteList(filtered);
        routeLayers.forEach(r => {
            const match = filtered.find(f => f.id === r.id);
            if (match) { map.addLayer(r.layer); r.layer.setStyle({ color: '#10e8b8', weight: 5 }); }
            else map.removeLayer(r.layer);
        });
        if (filtered.length > 0) {
            selectRoute(filtered[0].id);
        }
    });
}

// Filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        routeLayers.forEach(r  => { if (filter==='all'||filter==='routes')  map.addLayer(r.layer); else map.removeLayer(r.layer); });
        pointMarkers.forEach(m => { if (filter==='all'||filter==='points')  map.addLayer(m);       else map.removeLayer(m); });
        reportMarkers.forEach(m=> { if (filter==='all'||filter==='reports') map.addLayer(m);       else map.removeLayer(m); });
    });
});

// Map controls
document.getElementById('locateMe').addEventListener('click', () => {
    if (!navigator.geolocation) return alert('Geolocation not supported.');
    navigator.geolocation.getCurrentPosition(
        pos => map.setView([pos.coords.latitude, pos.coords.longitude], 16),
        ()  => alert('Could not get your location.')
    );
});
document.getElementById('resetView').addEventListener('click', () => {
    map.setView(DEFAULT_CENTER, DEFAULT_ZOOM);
    routeLayers.forEach(r => r.layer.setStyle({ color: '#10e8b8', weight: 5 }));
});

// Init
loadRoutes();
loadPoints();
loadReports();
"""

with open('static/js/map.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('map.js fixed!')

# Fix map.html search box id
html = open('templates/map.html', encoding='utf-8').read()
html = html.replace(
    'Search destination or routes...',
    'Search routes...'
)
# Fix search input id to searchBox
import re
html = re.sub(
    r'id=["\'](?:searchInput|search)["\']',
    'id="searchBox"',
    html
)
with open('templates/map.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('map.html fixed!')
print('Now run: python app.py')
print('Open: http://127.0.0.1:5000/map')
print('Press Ctrl+Shift+R to hard refresh!')