// Leaflet Map with Enhanced Features - Coimbatore Focus
const COIMBATORE_CENTER = [11.0168, 76.9558];
const COIMBATORE_BOUNDS = {
    north: 11.1068,
    south: 10.9268,
    east: 77.0458,
    west: 76.8658
};
const DEFAULT_ZOOM = 13;
let map, allRoutes = [], routePolylines = [], pointMarkers = [], reportMarkers = [], obstacleMarkers = [];
let userLocation = null;
let currentLocationMarker = null;
let voiceEnabled = false;
let speechSynthesis = window.speechSynthesis;
let multipleRoutes = [];
let selectedRouteIndex = null;
let routeCalculator;

// Initialize Leaflet Map
document.addEventListener('DOMContentLoaded', function() {
    // Initialize route calculator
    routeCalculator = new RouteCalculator();
    
    // Create map centered on Coimbatore
    map = L.map('map', {
        zoomControl: true,
        attributionControl: true
    }).setView(COIMBATORE_CENTER, DEFAULT_ZOOM);
    
    // Add colorful CartoDB Voyager tile layer (Google Maps style)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap contributors © CARTO',
        maxZoom: 19,
        subdomains: 'abcd'
    }).addTo(map);
    
    // Get user location
    getUserLocation();
    
    // Add emergency button
    addEmergencyButton();
    
    // Add voice navigation toggle
    addVoiceToggle();
    
    // Load data
    loadRoutes();
    loadPoints();
    loadReports();
    loadObstacles();
    
    // Setup event listeners
    setupEventListeners();
    
    // Setup search with location
    setupLocationSearch();
});

function makeIcon(type) {
    const icons = {
        ramp:    { icon: '♿', color: '#4CAF50', bg: '#E8F5E9' },
        toilet:  { icon: '🚻', color: '#2196F3', bg: '#E3F2FD' },
        bench:   { icon: '🪑', color: '#9C27B0', bg: '#F3E5F5' },
        audio:   { icon: '🔊', color: '#FF9800', bg: '#FFF3E0' },
        parking: { icon: '🅿️', color: '#00BCD4', bg: '#E0F7FA' },
        report:  { icon: '⚠️', color: '#F44336', bg: '#FFEBEE' },
        hospital: { icon: '🏥', color: '#E91E63', bg: '#FCE4EC' },
        police:  { icon: '👮', color: '#3F51B5', bg: '#E8EAF6' },
        obstacle: { icon: '❌', color: '#D32F2F', bg: '#FFCDD2' }
    };
    const i = icons[type] || icons.ramp;
    return L.divIcon({
        html: `<div style="
            font-size:28px;
            background:${i.bg};
            border:3px solid ${i.color};
            border-radius:50%;
            width:48px;
            height:48px;
            display:flex;
            align-items:center;
            justify-content:center;
            box-shadow:0 4px 12px rgba(0,0,0,0.2);
            transition:transform 0.2s;
        ">${i.icon}</div>`,
        className: 'custom-marker-enhanced',
        iconSize: [48, 48],
        iconAnchor: [24, 24],
        popupAnchor: [0, -24]
    });
}

function buildPopup(route) {
    const sc = route.accessibility_score >= 90 ? '#4CAF50' : route.accessibility_score >= 75 ? '#FF9800' : '#F44336';
    const scBg = route.accessibility_score >= 90 ? '#E8F5E9' : route.accessibility_score >= 75 ? '#FFF3E0' : '#FFEBEE';
    return '<div style="font-family:system-ui,-apple-system,sans-serif;min-width:260px;background:#FFFFFF;color:#212121;padding:16px;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.15);">' +
        '<div style="font-size:1.1rem;font-weight:700;margin-bottom:8px;color:#1976D2;">' + route.name + '</div>' +
        '<div style="font-size:.9rem;color:#616161;margin-bottom:12px;line-height:1.5;">' + route.description + '</div>' +
        '<div style="display:flex;gap:8px;flex-wrap:wrap;">' +
        '<span style="font-size:.85rem;font-weight:700;background:' + scBg + ';color:' + sc + ';padding:6px 12px;border-radius:20px;border:2px solid ' + sc + ';">' + route.accessibility_score + '% accessible</span>' +
        '<span style="font-size:.85rem;color:#424242;background:#F5F5F5;padding:6px 12px;border-radius:20px;">📏 ' + route.distance + '</span>' +
        (route.duration ? '<span style="font-size:.85rem;color:#424242;background:#F5F5F5;padding:6px 12px;border-radius:20px;">⏱ ' + route.duration + '</span>' : '') +
        '</div></div>';
}

async function loadRoutes() {
    const data = await fetch('/api/routes').then(r => r.json());
    allRoutes = data.routes;
    renderList(allRoutes);
    allRoutes.forEach(route => {
        const routeColor = route.accessibility_score >= 90 ? '#4CAF50' : 
                          route.accessibility_score >= 75 ? '#2196F3' : '#FF9800';
        const poly = L.polyline(route.coordinates, {
            color: routeColor,
            weight: 6,
            opacity: 0.85,
            lineJoin: 'round',
            lineCap: 'round'
        }).addTo(map);
        
        poly.bindPopup(buildPopup(route));
        routePolylines.push({ id: route.id, poly });
    });
}

function renderList(routes) {
    const list = document.getElementById('routesList');
    if (!routes.length) {
        list.innerHTML = '<div style="text-align:center;padding:2rem;color:var(--text-muted);font-size:1rem;">No routes found.</div>';
        return;
    }
    list.innerHTML = routes.map(r => {
        const sc = r.accessibility_score >= 90 ? 'score-high' : r.accessibility_score >= 75 ? 'score-med' : 'score-low';
        const distance = userLocation ? calculateDistance(userLocation, r.coordinates[0]) : null;
        const distanceText = distance ? `<span class="rp-pill">📍 ${distance.toFixed(2)} km away</span>` : '';
        
        return '<div class="route-panel enhanced-card" id="rp-' + r.id + '" onclick="selectRoute(' + r.id + ')">' +
            '<div class="rp-name" style="font-size:1.1rem;font-weight:700;margin-bottom:0.5rem;">' + r.name + '</div>' +
            '<div class="rp-meta" style="margin-bottom:0.5rem;">' +
            '<span class="rp-pill" style="font-size:0.9rem;padding:4px 10px;">📏 ' + r.distance + '</span>' +
            (r.duration ? '<span class="rp-pill" style="font-size:0.9rem;padding:4px 10px;">⏱ ' + r.duration + '</span>' : '') +
            distanceText +
            '<span class="score-badge ' + sc + '" style="font-size:0.9rem;padding:4px 10px;">' + r.accessibility_score + '%</span>' +
            '</div>' +
            '<div style="font-size:0.9rem;color:var(--text-muted);margin-bottom:0.8rem;line-height:1.6;">' + r.description + '</div>' +
            '<div class="accessibility-icons" style="margin-bottom:0.8rem;">' +
            (r.tags.includes('wheelchair') ? '<span class="access-icon" title="Wheelchair Accessible">♿</span>' : '') +
            (r.tags.includes('visual') ? '<span class="access-icon" title="Visually Impaired Friendly">👁️</span>' : '') +
            (r.tags.includes('elderly') ? '<span class="access-icon" title="Elderly Friendly">🧑</span>' : '') +
            '</div>' +
            '<button class="rp-btn" style="font-size:0.95rem;padding:10px;" onclick="event.stopPropagation();selectRoute(' + r.id + ')">Show on Map →</button>' +
            '</div>';
    }).join('');
}

function selectRoute(id) {
    routePolylines.forEach(r => {
        const route = allRoutes.find(rt => rt.id === r.id);
        const defaultColor = route.accessibility_score >= 90 ? '#4CAF50' : 
                            route.accessibility_score >= 75 ? '#2196F3' : '#FF9800';
        r.poly.setStyle({ color: defaultColor, weight: 6, opacity: 0.85 });
    });
    document.querySelectorAll('.route-panel').forEach(e => e.classList.remove('active'));
    const found = routePolylines.find(r => r.id === id);
    const route = allRoutes.find(r => r.id === id);
    if (found && route) {
        found.poly.setStyle({ color: '#E91E63', weight: 9, opacity: 1 });
        const el = document.getElementById('rp-' + id);
        if (el) { el.classList.add('active'); el.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
        const bounds = L.latLngBounds(route.coordinates);
        map.fitBounds(bounds, { padding: [60, 60] });
        found.poly.openPopup();
    }
}

async function loadPoints() {
    const data = await fetch('/api/points').then(r => r.json());
    data.points.forEach(pt => {
        const m = L.marker([pt.lat, pt.lng], {
            icon: makeIcon(pt.type),
            title: pt.name
        }).addTo(map);
        
        // Use enhanced popup if mapEnhancer is available
        if (window.mapEnhancer) {
            mapEnhancer.createInteractivePopup(m, {
                name: pt.name,
                type: pt.type,
                lat: pt.lat,
                lng: pt.lng,
                icon: makeIcon(pt.type).options.html.match(/>(.*?)</)[1],
                color: '#10e8b8',
                description: `Status: ${pt.status}`,
                features: [pt.type, pt.status]
            });
        } else {
            m.bindPopup(
                '<div style="font-family:sans-serif;background:#111827;color:#e8eeff;padding:8px;border-radius:8px;min-width:180px;">' +
                '<div style="font-weight:700;margin-bottom:6px;">' + pt.name + '</div>' +
                '<span style="font-size:.75rem;padding:2px 8px;border-radius:50px;background:rgba(16,232,184,.14);color:' +
                (pt.status === 'operational' ? '#10e8b8' : '#ffc35a') + ';">' + pt.status + '</span></div>'
            );
        }
        
        pointMarkers.push(m);
    });
}

async function loadReports() {
    const data = await fetch('/api/reports').then(r => r.json());
    reportMarkers.forEach(m => map.removeLayer(m));
    reportMarkers = [];
    data.reports.forEach(r => {
        if (!r.lat || !r.lng) return;
        const m = L.marker([r.lat, r.lng], {
            icon: makeIcon('report'),
            title: r.title
        }).addTo(map);
        
        m.bindPopup(
            '<div style="font-family:sans-serif;background:#111827;color:#e8eeff;padding:8px;border-radius:8px;min-width:200px;">' +
            '<div style="font-weight:700;margin-bottom:4px;">' + r.title + '</div>' +
            '<div style="font-size:.82rem;color:#7a8aaa;margin-bottom:6px;">' + r.description + '</div>' +
            '<span style="font-size:.72rem;background:rgba(255,92,122,.15);color:#ff5c7a;padding:2px 8px;border-radius:50px;">' +
            r.issue_type.replace(/_/g, ' ') + '</span></div>'
        );
        reportMarkers.push(m);
    });
}

// Load obstacles
async function loadObstacles() {
    try {
        const response = await fetch('/api/obstacles');
        const data = await response.json();
        
        obstacleMarkers.forEach(m => map.removeLayer(m));
        obstacleMarkers = [];
        
        data.obstacles.forEach(obs => {
            const color = obs.severity === 'critical' ? '#ff5c7a' : obs.severity === 'high' ? '#ff8c42' : '#ffc35a';
            const icon = obs.severity === 'critical' ? '❌' : '⚠️';
            
            const marker = L.marker([obs.lat, obs.lng], {
                icon: L.divIcon({
                    html: `<div style="font-size:28px;filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.5))">${icon}</div>`,
                    className: 'obstacle-marker',
                    iconSize: [30, 30]
                })
            }).addTo(map);
            
            marker.bindPopup(`
                <div style="min-width:200px;font-family:sans-serif;background:#111827;color:#e8eeff;padding:10px;border-radius:8px;">
                    <strong style="color:${color}">${icon} ${obs.type.replace('_', ' ').toUpperCase()}</strong><br>
                    <small>${obs.description || 'No description'}</small><br>
                    <span style="background-color:${color};color:white;padding:2px 8px;border-radius:50px;font-size:0.7rem;margin-top:5px;display:inline-block;">Severity: ${obs.severity}</span>
                </div>
            `);
            
            obstacleMarkers.push(marker);
        });
    } catch (error) {
        console.error('Error loading obstacles:', error);
    }
}

// Emergency button
function addEmergencyButton() {
    const EmergencyControl = L.Control.extend({
        options: { position: 'topright' },
        onAdd: function(map) {
            const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
            container.innerHTML = `
                <a href="#" class="emergency-btn" style="
                    background: linear-gradient(135deg, #ff5c7a 0%, #ff3860 100%);
                    color: white;
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 28px;
                    text-decoration: none;
                    box-shadow: 0 4px 12px rgba(255,92,122,0.4);
                    border: 3px solid white;
                    animation: pulse 2s infinite;
                " title="Emergency Support">
                    🆘
                </a>
            `;
            
            L.DomEvent.on(container, 'click', function(e) {
                L.DomEvent.stopPropagation(e);
                L.DomEvent.preventDefault(e);
                showEmergencyPanel();
            });
            
            return container;
        }
    });
    
    map.addControl(new EmergencyControl());
    
    // Add pulse animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0%, 100% { transform: scale(1); box-shadow: 0 4px 12px rgba(255,92,122,0.4); }
            50% { transform: scale(1.05); box-shadow: 0 6px 20px rgba(255,92,122,0.6); }
        }
    `;
    document.head.appendChild(style);
}

async function showEmergencyPanel() {
    const currentPos = map.getCenter();
    
    try {
        const response = await fetch('/api/emergency', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({lat: currentPos.lat, lng: currentPos.lng})
        });
        
        const data = await response.json();
        
        const panel = document.createElement('div');
        panel.className = 'emergency-panel';
        panel.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            z-index: 10000;
            max-width: 400px;
            width: 90%;
        `;
        
        panel.innerHTML = `
            <div style="text-align:center;margin-bottom:20px">
                <h4 style="color:#ff5c7a;margin:0">🆘 Emergency Support</h4>
            </div>
            
            <div style="margin-bottom:15px;padding:15px;background:#fff5f5;border-radius:10px;border-left:4px solid #ff5c7a">
                <strong>🚨 Emergency Numbers</strong><br>
                <div style="margin-top:10px">
                    <a href="tel:${data.emergency_numbers.ambulance}" style="display:block;padding:8px;margin:5px 0;background:#10e8b8;color:white;text-decoration:none;border-radius:5px;text-align:center">
                        🚑 Ambulance: ${data.emergency_numbers.ambulance}
                    </a>
                    <a href="tel:${data.emergency_numbers.police}" style="display:block;padding:8px;margin:5px 0;background:#5b9dff;color:white;text-decoration:none;border-radius:5px;text-align:center">
                        👮 Police: ${data.emergency_numbers.police}
                    </a>
                </div>
            </div>
            
            ${data.nearest_hospital ? `
            <div style="margin-bottom:15px;padding:12px;background:#f0fdf4;border-radius:8px">
                <strong>🏥 Nearest Hospital</strong><br>
                <div style="margin-top:8px;font-size:14px">
                    ${data.nearest_hospital.name}<br>
                    <small style="color:#666">${data.nearest_hospital.distance_km.toFixed(2)} km away</small><br>
                    <a href="tel:${data.nearest_hospital.phone}" style="color:#10e8b8">📞 ${data.nearest_hospital.phone}</a>
                </div>
            </div>
            ` : ''}
            
            ${data.nearest_police ? `
            <div style="margin-bottom:15px;padding:12px;background:#eff6ff;border-radius:8px">
                <strong>👮 Nearest Police Station</strong><br>
                <div style="margin-top:8px;font-size:14px">
                    ${data.nearest_police.name}<br>
                    <small style="color:#666">${data.nearest_police.distance_km.toFixed(2)} km away</small>
                </div>
            </div>
            ` : ''}
            
            <button onclick="this.parentElement.remove()" style="
                width:100%;
                padding:12px;
                background:#1a1f2e;
                color:white;
                border:none;
                border-radius:8px;
                cursor:pointer;
                font-size:16px;
            ">Close</button>
        `;
        
        document.body.appendChild(panel);
        
        // Add markers for emergency facilities
        if (data.nearest_hospital) {
            L.marker([data.nearest_hospital.lat, data.nearest_hospital.lng], {
                icon: makeIcon('hospital')
            }).addTo(map).bindPopup(`<b>${data.nearest_hospital.name}</b><br>${data.nearest_hospital.distance_km.toFixed(2)} km`);
        }
        
        if (data.nearest_police) {
            L.marker([data.nearest_police.lat, data.nearest_police.lng], {
                icon: makeIcon('police')
            }).addTo(map).bindPopup(`<b>${data.nearest_police.name}</b><br>${data.nearest_police.distance_km.toFixed(2)} km`);
        }
        
    } catch (error) {
        console.error('Error loading emergency data:', error);
        alert('Failed to load emergency information');
    }
}

// Setup event listeners
function setupEventListeners() {
    const searchBox = document.getElementById('routeSearch');
    if (searchBox) {
        searchBox.addEventListener('input', function () {
            const q = this.value.trim().toLowerCase();
            if (!q) { 
                renderList(allRoutes); 
                routePolylines.forEach(r => map.addLayer(r.poly)); 
                return; 
            }
            const f = allRoutes.filter(r => r.name.toLowerCase().includes(q) || r.description.toLowerCase().includes(q));
            renderList(f);
            routePolylines.forEach(r => {
                if (f.find(x => x.id === r.id)) {
                    map.addLayer(r.poly);
                } else {
                    map.removeLayer(r.poly);
                }
            });
            if (f.length) selectRoute(f[0].id);
        });
    }

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const f = btn.dataset.filter;
            
            routePolylines.forEach(r => {
                if (f === 'all' || f === 'routes') map.addLayer(r.poly);
                else map.removeLayer(r.poly);
            });
            
            pointMarkers.forEach(m => {
                if (f === 'all' || f === 'points') map.addLayer(m);
                else map.removeLayer(m);
            });
            
            reportMarkers.forEach(m => {
                if (f === 'all' || f === 'reports') map.addLayer(m);
                else map.removeLayer(m);
            });
        });
    });

    const locateBtn = document.getElementById('locateMe');
    if (locateBtn) {
        locateBtn.addEventListener('click', () => {
            getUserLocation(true);
        });
    }

    const resetBtn = document.getElementById('resetView');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            map.setView(COIMBATORE_CENTER, DEFAULT_ZOOM);
            routePolylines.forEach(r => r.poly.setStyle({ color: '#10e8b8', weight: 5 }));
        });
    }
    
    const refreshBtn = document.getElementById('refreshReports');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            loadReports();
            loadObstacles();
        });
    }
}

// Get user location
function getUserLocation(zoomTo = false) {
    if (!navigator.geolocation) {
        console.log('Geolocation not supported, using Coimbatore as default');
        userLocation = { lat: COIMBATORE_CENTER[0], lng: COIMBATORE_CENTER[1] };
        addCurrentLocationMarker(userLocation);
        return;
    }
    
    navigator.geolocation.getCurrentPosition(
        (position) => {
            userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            
            // Check if user is in Coimbatore area
            if (!isInCoimbatore(userLocation)) {
                console.log('User location outside Coimbatore, using Coimbatore center');
                userLocation = { lat: COIMBATORE_CENTER[0], lng: COIMBATORE_CENTER[1] };
            }
            
            addCurrentLocationMarker(userLocation);
            
            if (zoomTo) {
                map.setView([userLocation.lat, userLocation.lng], 15);
                speak('Your current location has been found');
            }
            
            // Reload routes with distance info
            renderList(allRoutes);
        },
        (error) => {
            console.log('Geolocation error, using Coimbatore as default:', error);
            userLocation = { lat: COIMBATORE_CENTER[0], lng: COIMBATORE_CENTER[1] };
            addCurrentLocationMarker(userLocation);
        }
    );
}

// Check if location is in Coimbatore
function isInCoimbatore(location) {
    return location.lat >= COIMBATORE_BOUNDS.south &&
           location.lat <= COIMBATORE_BOUNDS.north &&
           location.lng >= COIMBATORE_BOUNDS.west &&
           location.lng <= COIMBATORE_BOUNDS.east;
}

// Add current location marker
function addCurrentLocationMarker(location) {
    if (currentLocationMarker) {
        map.removeLayer(currentLocationMarker);
    }
    
    currentLocationMarker = L.marker([location.lat, location.lng], {
        icon: L.divIcon({
            html: '<div style="font-size:36px;background:#1976D2;border:4px solid #FFFFFF;border-radius:50%;width:56px;height:56px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(25,118,210,0.4);animation:pulse-blue 2s infinite;">📍</div>',
            className: 'current-location-marker',
            iconSize: [56, 56],
            iconAnchor: [28, 28]
        })
    }).addTo(map);
    
    currentLocationMarker.bindPopup('<div style="font-family:system-ui,-apple-system,sans-serif;background:#FFFFFF;padding:12px;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.15);"><b style="color:#1976D2;font-size:1rem;">Your Location</b><br><span style="color:#616161;font-size:0.9rem;">Coimbatore, Tamil Nadu</span></div>');
    
    // Add pulse animation
    if (!document.getElementById('pulse-blue-animation')) {
        const style = document.createElement('style');
        style.id = 'pulse-blue-animation';
        style.textContent = `
            @keyframes pulse-blue {
                0%, 100% { transform: scale(1); box-shadow: 0 4px 16px rgba(25,118,210,0.4); }
                50% { transform: scale(1.1); box-shadow: 0 6px 24px rgba(25,118,210,0.6); }
            }
        `;
        document.head.appendChild(style);
    }
}

// Calculate distance between two points
function calculateDistance(point1, point2) {
    const R = 6371; // Earth's radius in km
    const lat1 = point1.lat * Math.PI / 180;
    const lat2 = (Array.isArray(point2) ? point2[0] : point2.lat) * Math.PI / 180;
    const lng1 = point1.lng * Math.PI / 180;
    const lng2 = (Array.isArray(point2) ? point2[1] : point2.lng) * Math.PI / 180;
    
    const dlat = lat2 - lat1;
    const dlng = lng2 - lng1;
    
    const a = Math.sin(dlat/2) * Math.sin(dlat/2) +
              Math.cos(lat1) * Math.cos(lat2) *
              Math.sin(dlng/2) * Math.sin(dlng/2);
    
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

// Voice navigation functions
function addVoiceToggle() {
    const VoiceControl = L.Control.extend({
        options: { position: 'topleft' },
        onAdd: function(map) {
            const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
            container.innerHTML = `
                <a href="#" id="voiceToggle" class="voice-toggle" style="
                    background: linear-gradient(135deg, #10e8b8 0%, #0bc9a0 100%);
                    color: white;
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    text-decoration: none;
                    box-shadow: 0 4px 12px rgba(16,232,184,0.4);
                    border: 2px solid white;
                " title="Toggle Voice Navigation">
                    🔊
                </a>
            `;
            
            L.DomEvent.on(container, 'click', function(e) {
                L.DomEvent.stopPropagation(e);
                L.DomEvent.preventDefault(e);
                toggleVoice();
            });
            
            return container;
        }
    });
    
    map.addControl(new VoiceControl());
}

function toggleVoice() {
    voiceEnabled = !voiceEnabled;
    const btn = document.getElementById('voiceToggle');
    
    if (voiceEnabled) {
        btn.style.background = 'linear-gradient(135deg, #ff5c7a 0%, #ff3860 100%)';
        btn.innerHTML = '🔇';
        speak('Voice navigation enabled');
    } else {
        btn.style.background = 'linear-gradient(135deg, #10e8b8 0%, #0bc9a0 100%)';
        btn.innerHTML = '🔊';
        speechSynthesis.cancel();
    }
}

function speak(text) {
    if (!voiceEnabled || !speechSynthesis) return;
    
    speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 1;
    speechSynthesis.speak(utterance);
}

// Location-based search using Nominatim
async function setupLocationSearch() {
    const searchBox = document.getElementById('routeSearch');
    if (!searchBox) return;
    
    let searchTimeout;
    searchBox.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length < 3) return;
        
        searchTimeout = setTimeout(() => {
            searchNominatim(query);
        }, 500);
    });
}

async function searchNominatim(query) {
    try {
        const url = `https://nominatim.openstreetmap.org/search?` +
            `q=${encodeURIComponent(query + ' Coimbatore Tamil Nadu')}&` +
            `format=json&` +
            `bounded=1&` +
            `viewbox=${COIMBATORE_BOUNDS.west},${COIMBATORE_BOUNDS.south},${COIMBATORE_BOUNDS.east},${COIMBATORE_BOUNDS.north}&` +
            `limit=5`;
        
        const response = await fetch(url);
        const results = await response.json();
        
        if (results.length > 0) {
            displaySearchResults(results);
            speak(`Found ${results.length} results for ${query}`);
        }
    } catch (error) {
        console.error('Search error:', error);
    }
}

function displaySearchResults(results) {
    const list = document.getElementById('routesList');
    
    list.innerHTML = '<div style="padding:1rem;font-size:1.1rem;font-weight:700;color:#10e8b8;">Search Results</div>' +
        results.map((result, index) => {
            const distance = userLocation ? 
                calculateDistance(userLocation, { lat: parseFloat(result.lat), lng: parseFloat(result.lon) }) : null;
            const distanceText = distance ? `${distance.toFixed(2)} km away` : '';
            
            return `<div class="route-panel enhanced-card" onclick="showSearchResult(${index}, ${result.lat}, ${result.lon})" style="cursor:pointer;">
                <div class="rp-name" style="font-size:1.1rem;font-weight:700;margin-bottom:0.5rem;">${result.display_name.split(',')[0]}</div>
                <div style="font-size:0.9rem;color:var(--text-muted);margin-bottom:0.5rem;">${result.display_name}</div>
                ${distanceText ? `<div class="rp-pill" style="font-size:0.9rem;">📍 ${distanceText}</div>` : ''}
                <button class="rp-btn" style="font-size:0.95rem;padding:10px;margin-top:0.5rem;">Show on Map</button>
            </div>`;
        }).join('');
    
    // Store results for later use
    window.searchResults = results;
}

function showSearchResult(index, lat, lng) {
    const result = window.searchResults[index];
    const destination = { lat: parseFloat(lat), lng: parseFloat(lng) };
    
    if (!userLocation) {
        alert('Getting your location... Please wait and try again.');
        getUserLocation(false);
        return;
    }
    
    // Calculate 3 different routes
    multipleRoutes = routeCalculator.calculateMultipleRoutes(userLocation, destination);
    
    // Display routes on map
    displayMultipleRoutes(multipleRoutes, result.display_name.split(',')[0]);
    
    // Show route selection panel
    displayRouteSelectionPanel(multipleRoutes, result.display_name.split(',')[0]);
    
    speak(`Found 3 routes to ${result.display_name.split(',')[0]}`);
}

// Display multiple routes on map
function displayMultipleRoutes(routes, destinationName) {
    // Clear existing route polylines
    routePolylines.forEach(r => map.removeLayer(r.poly));
    routePolylines = [];
    
    // Add all 3 routes to map with animation if enhancer available
    routes.forEach((route, index) => {
        let polyline;
        
        if (window.mapEnhancer) {
            // Use animated route drawing
            polyline = mapEnhancer.animateRoute(route.coordinates, route.color, 1500 + index * 500);
            
            // Setup hover and click interactions
            setTimeout(() => {
                mapEnhancer.setupRouteInteractions(polyline, route);
            }, 2000 + index * 500);
        } else {
            // Fallback to regular polyline
            polyline = L.polyline(route.coordinates, {
                color: route.color,
                weight: 5,
                opacity: 0.7,
                className: `route-${route.type}`
            }).addTo(map);
            
            polyline.bindPopup(buildRoutePopup(route, destinationName));
            polyline.on('click', () => selectMultipleRoute(index));
        }
        
        routePolylines.push({ id: route.id, poly: polyline, route: route });
    });
    
    // Fit map to show all routes with smooth animation
    const allCoords = routes.flatMap(r => r.coordinates);
    const bounds = L.latLngBounds(allCoords);
    map.flyToBounds(bounds, {
        padding: [50, 50],
        duration: 1.5,
        easeLinearity: 0.25
    });
    
    // Add destination marker
    const destCoord = routes[0].coordinates[routes[0].coordinates.length - 1];
    L.marker(destCoord, {
        icon: L.divIcon({
            html: '<div style="font-size:32px;filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.5))">🎯</div>',
            className: 'destination-marker',
            iconSize: [40, 40]
        })
    }).addTo(map).bindPopup(`<b>${destinationName}</b><br>Destination`);
    
    // Update Smart Panel with route comparison
    if (window.smartPanel) {
        smartPanel.updateRouteComparison(routes);
        // Auto-select the most accessible route
        const accessibleRoute = routes.find(r => r.type === 'accessible') || routes[0];
        const accessibleIndex = routes.indexOf(accessibleRoute);
        setTimeout(() => selectMultipleRoute(accessibleIndex), 2500);
    }
}

// Build route popup
function buildRoutePopup(route, destinationName) {
    return `
        <div style="font-family:sans-serif;background:#111827;color:#e8eeff;padding:12px;border-radius:10px;min-width:250px;">
            <div style="font-size:1.2rem;font-weight:700;margin-bottom:8px;color:${route.color}">
                ${route.icon} ${route.name}
            </div>
            <div style="font-size:0.9rem;color:#7a8aaa;margin-bottom:10px;">${route.description}</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;">
                <div style="background:rgba(16,232,184,0.1);padding:8px;border-radius:6px;">
                    <div style="font-size:0.75rem;color:#7a8aaa;">Distance</div>
                    <div style="font-size:1rem;font-weight:700;color:#10e8b8;">${route.distance.toFixed(2)} km</div>
                </div>
                <div style="background:rgba(91,157,255,0.1);padding:8px;border-radius:6px;">
                    <div style="font-size:0.75rem;color:#7a8aaa;">Time</div>
                    <div style="font-size:1rem;font-weight:700;color:#5b9dff;">${route.estimatedTime}</div>
                </div>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="background:${route.difficulty.color};color:white;padding:4px 10px;border-radius:12px;font-size:0.8rem;font-weight:600;">
                    ${route.difficulty.icon} ${route.difficulty.level}
                </span>
                <span style="background:rgba(16,232,184,0.15);color:#10e8b8;padding:4px 10px;border-radius:12px;font-size:0.8rem;font-weight:600;">
                    ${route.accessibilityScore}% Accessible
                </span>
            </div>
        </div>
    `;
}

// Display route selection panel
function displayRouteSelectionPanel(routes, destinationName) {
    const list = document.getElementById('routesList');
    
    list.innerHTML = `
        <div style="padding:1rem;border-bottom:2px solid rgba(16,232,184,0.3);">
            <div style="font-size:1.2rem;font-weight:700;color:#10e8b8;margin-bottom:0.5rem;">📍 Routes to ${destinationName}</div>
            <div style="font-size:0.85rem;color:#7a8aaa;">Select your preferred route</div>
        </div>
    ` + routes.map((route, index) => `
        <div class="route-panel enhanced-card multi-route-card" id="multi-route-${index}" onclick="selectMultipleRoute(${index})" style="border-left:4px solid ${route.color};">
            <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:0.8rem;">
                <div>
                    <div style="font-size:1.1rem;font-weight:700;color:${route.color};margin-bottom:0.3rem;">
                        ${route.icon} ${route.name}
                    </div>
                    <div style="font-size:0.85rem;color:#7a8aaa;line-height:1.4;">${route.description}</div>
                </div>
            </div>
            
            <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:0.5rem;margin-bottom:0.8rem;">
                <div class="route-stat">
                    <span style="font-size:0.75rem;color:#7a8aaa;">Distance</span>
                    <span style="font-size:1rem;font-weight:700;color:#10e8b8;">📏 ${route.distance.toFixed(2)} km</span>
                </div>
                <div class="route-stat">
                    <span style="font-size:0.75rem;color:#7a8aaa;">Time</span>
                    <span style="font-size:1rem;font-weight:700;color:#5b9dff;">⏱ ${route.estimatedTime}</span>
                </div>
            </div>
            
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:0.8rem;">
                <span style="background:${route.difficulty.color};color:white;padding:4px 10px;border-radius:12px;font-size:0.8rem;font-weight:600;">
                    ${route.difficulty.icon} ${route.difficulty.level}
                </span>
                <span style="background:rgba(16,232,184,0.15);color:#10e8b8;padding:4px 10px;border-radius:12px;font-size:0.8rem;font-weight:600;">
                    ${route.accessibilityScore}% Accessible
                </span>
            </div>
            
            <div style="display:flex;gap:0.3rem;flex-wrap:wrap;margin-bottom:0.8rem;">
                ${route.features.ramps ? `<span class="feature-tag">♿ ${route.features.ramps} Ramps</span>` : ''}
                ${route.features.benches ? `<span class="feature-tag">🪑 ${route.features.benches} Benches</span>` : ''}
                ${route.features.lighting ? `<span class="feature-tag">💡 ${route.features.lighting}</span>` : ''}
                ${route.features.surface ? `<span class="feature-tag">🛤️ ${route.features.surface}</span>` : ''}
            </div>
            
            <button class="rp-btn" style="background:${route.color};border:none;color:white;font-weight:600;" onclick="event.stopPropagation();selectMultipleRoute(${index})">
                Select This Route →
            </button>
        </div>
    `).join('');
    
    // Add route legend
    addRouteLegend();
}

// Select a specific route from multiple options
function selectMultipleRoute(index) {
    selectedRouteIndex = index;
    const selectedRoute = multipleRoutes[index];
    
    // Update polyline styles
    routePolylines.forEach((r, i) => {
        if (i === index) {
            r.poly.setStyle({ weight: 8, opacity: 1 });
        } else {
            r.poly.setStyle({ weight: 3, opacity: 0.3 });
        }
    });
    
    // Update card styles
    document.querySelectorAll('.multi-route-card').forEach((card, i) => {
        if (i === index) {
            card.style.background = 'rgba(16,232,184,0.05)';
            card.style.borderLeftWidth = '6px';
        } else {
            card.style.background = '';
            card.style.borderLeftWidth = '4px';
            card.style.opacity = '0.6';
        }
    });
    
    // Zoom to selected route
    const bounds = L.latLngBounds(selectedRoute.coordinates);
    map.fitBounds(bounds, { padding: [50, 50] });
    
    // Update Smart Info Panel
    if (window.smartPanel) {
        smartPanel.updateSmartPanel(selectedRoute);
        smartPanel.updateNearbyEssentials(userLocation || { lat: COIMBATORE_CENTER[0], lng: COIMBATORE_CENTER[1] });
    }
    
    // Speak selection
    speak(`Selected ${selectedRoute.name}. Distance: ${selectedRoute.distance.toFixed(1)} kilometers. Estimated time: ${selectedRoute.estimatedTime}`);
    
    // Show voice navigation option
    showVoiceNavigationOption(selectedRoute);
}

// Add route legend
function addRouteLegend() {
    const legendHtml = `
        <div style="padding:1rem;background:rgba(16,232,184,0.05);border-radius:10px;margin-top:1rem;">
            <div style="font-size:0.9rem;font-weight:700;color:#10e8b8;margin-bottom:0.8rem;">🗺️ Route Types</div>
            <div style="display:flex;flex-direction:column;gap:0.5rem;">
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <div style="width:30px;height:4px;background:#5b9dff;border-radius:2px;"></div>
                    <span style="font-size:0.85rem;color:#e8eeff;">⚡ Shortest - Fastest route</span>
                </div>
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <div style="width:30px;height:4px;background:#10e8b8;border-radius:2px;"></div>
                    <span style="font-size:0.85rem;color:#e8eeff;">♿ Accessible - Wheelchair-friendly</span>
                </div>
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <div style="width:30px;height:4px;background:#ffc35a;border-radius:2px;"></div>
                    <span style="font-size:0.85rem;color:#e8eeff;">🛡️ Safest - Avoid obstacles</span>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('routesList').insertAdjacentHTML('beforeend', legendHtml);
}

// Show voice navigation option
function showVoiceNavigationOption(route) {
    const existingPanel = document.getElementById('voiceNavPanel');
    if (existingPanel) existingPanel.remove();
    
    const panel = document.createElement('div');
    panel.id = 'voiceNavPanel';
    panel.style.cssText = `
        position:fixed;
        bottom:20px;
        left:50%;
        transform:translateX(-50%);
        background:linear-gradient(135deg,#10e8b8 0%,#0bc9a0 100%);
        color:white;
        padding:15px 25px;
        border-radius:50px;
        box-shadow:0 6px 20px rgba(16,232,184,0.4);
        z-index:10000;
        display:flex;
        align-items:center;
        gap:15px;
        cursor:pointer;
        animation:slideUp 0.3s ease;
    `;
    
    panel.innerHTML = `
        <span style="font-size:1.5rem;">🎤</span>
        <span style="font-weight:600;font-size:1rem;">Start Voice Navigation</span>
    `;
    
    panel.onclick = () => startRouteVoiceNavigation(route);
    document.body.appendChild(panel);
    
    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideUp {
            from { transform: translateX(-50%) translateY(100px); opacity: 0; }
            to { transform: translateX(-50%) translateY(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
}

// Start voice navigation for selected route
function startRouteVoiceNavigation(route) {
    if (!voiceEnabled) {
        toggleVoice();
    }
    
    const instructions = [
        `Starting navigation on ${route.name}`,
        `Total distance: ${route.distance.toFixed(1)} kilometers`,
        `Estimated time: ${route.estimatedTime}`,
        `Difficulty level: ${route.difficulty.level}`,
        `Accessibility score: ${route.accessibilityScore} percent`
    ];
    
    if (route.features.ramps) {
        instructions.push(`This route has ${route.features.ramps} wheelchair ramps`);
    }
    
    if (route.features.obstacles && route.features.obstacles.length > 0) {
        instructions.push(`Warning: ${route.features.obstacles.join(', ')} detected on route`);
    }
    
    if (route.features.benches) {
        instructions.push(`${route.features.benches} rest benches available along the way`);
    }
    
    instructions.push('Navigation started. Follow the highlighted route on the map.');
    
    // Speak instructions one by one
    let index = 0;
    const speakNext = () => {
        if (index < instructions.length && voiceEnabled) {
            speak(instructions[index]);
            index++;
            setTimeout(speakNext, 3000);
        }
    };
    speakNext();
}