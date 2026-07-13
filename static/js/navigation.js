// Smart Navigation with Voice Guidance
let map, sourceMarker, destMarker, routeLayers = [], obstacleMarkers = [];
let currentRoute = null;
let voiceActive = false;
let currentStepIndex = 0;
let emergencyButton;

// Initialize Map
document.addEventListener('DOMContentLoaded', function() {
    map = L.map('map').setView([28.6139, 77.2090], 13);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Add emergency button to map
    addEmergencyButton();
    
    // Load obstacles
    loadObstacles();
    
    // Click to set source/destination
    map.on('click', function(e) {
        if (!sourceMarker) {
            sourceMarker = L.marker(e.latlng, {
                icon: L.icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
                    iconSize: [25, 41],
                    iconAnchor: [12, 41]
                })
            }).addTo(map).bindPopup('Source').openPopup();
            document.getElementById('sourceLat').textContent = e.latlng.lat.toFixed(4);
            document.getElementById('sourceLng').textContent = e.latlng.lng.toFixed(4);
        } else if (!destMarker) {
            destMarker = L.marker(e.latlng, {
                icon: L.icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                    iconSize: [25, 41],
                    iconAnchor: [12, 41]
                })
            }).addTo(map).bindPopup('Destination').openPopup();
            document.getElementById('destLat').textContent = e.latlng.lat.toFixed(4);
            document.getElementById('destLng').textContent = e.latlng.lng.toFixed(4);
        }
    });
    
    // Form submission
    document.getElementById('routeForm').addEventListener('submit', findRoutes);
    document.getElementById('startVoice').addEventListener('click', startVoiceNavigation);
    document.getElementById('stopVoice').addEventListener('click', stopVoiceNavigation);
});

async function findRoutes(e) {
    e.preventDefault();
    
    if (!sourceMarker || !destMarker) {
        alert('Please select source and destination on the map');
        return;
    }
    
    const source = {
        lat: parseFloat(document.getElementById('sourceLat').textContent),
        lng: parseFloat(document.getElementById('sourceLng').textContent)
    };
    
    const destination = {
        lat: parseFloat(document.getElementById('destLat').textContent),
        lng: parseFloat(document.getElementById('destLng').textContent)
    };
    
    const userType = document.getElementById('userType').value;
    
    try {
        const response = await fetch('/api/calculate-routes', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({source, destination, user_type: userType})
        });
        
        const data = await response.json();
        displayRoutes(data.routes);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to calculate routes');
    }
}

function displayRoutes(routes) {
    // Clear previous routes
    routeLayers.forEach(layer => map.removeLayer(layer));
    routeLayers = [];
    
    const resultsDiv = document.getElementById('routeResults');
    resultsDiv.innerHTML = '<h6 class="mt-3">Available Routes</h6>';
    
    routes.forEach((route, index) => {
        // Draw route on map
        const polyline = L.polyline(route.coordinates, {
            color: route.color,
            weight: 5,
            opacity: 0.7
        }).addTo(map);
        
        routeLayers.push(polyline);
        
        // Difficulty badge
        const difficultyBadge = `<span class="badge" style="background-color:${route.difficulty_color}">${route.difficulty}</span>`;
        
        // Safety icon
        const safetyIcon = route.safety_level === 'safe' ? '✅' : route.safety_level === 'moderate' ? '⚠️' : '❌';
        
        // Add route card
        const routeCard = `
            <div class="card mb-2 route-card" data-route-id="${route.id}" style="border-left: 4px solid ${route.color}">
                <div class="card-body p-2">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${safetyIcon} ${route.name}</strong>
                            <br>
                            <small>📏 ${route.distance.toFixed(2)} km | ${difficultyBadge}</small>
                        </div>
                        <div class="text-end">
                            <span class="badge" style="background-color:${route.color}">
                                Score: ${route.accessibility_score}
                            </span>
                            <br>
                            <small class="text-muted">${route.safety_level}</small>
                        </div>
                    </div>
                    ${route.obstacles.length > 0 ? `<div class="alert alert-warning p-1 mt-1 mb-1"><small>⚠️ ${route.obstacles.length} obstacle(s) detected</small></div>` : ''}
                    <button class="btn btn-sm btn-primary w-100 mt-2" onclick="selectRoute(${index})">
                        Select Route
                    </button>
                </div>
            </div>
        `;
        resultsDiv.innerHTML += routeCard;
    });
    
    // Fit map to show all routes
    const bounds = L.latLngBounds(routes[0].coordinates);
    map.fitBounds(bounds, {padding: [50, 50]});
    
    // Store routes globally
    window.availableRoutes = routes;
}

function selectRoute(index) {
    currentRoute = window.availableRoutes[index];
    
    // Highlight selected route
    routeLayers.forEach((layer, i) => {
        layer.setStyle({
            weight: i === index ? 8 : 5,
            opacity: i === index ? 1 : 0.5
        });
    });
    
    // Show voice controls
    document.getElementById('voiceControls').style.display = 'block';
    
    // Load nearby facilities
    loadNearbyFacilities(currentRoute);
    
    // Add markers for route features
    addRouteMarkers(currentRoute);
}

function addRouteMarkers(route) {
    // Add markers for ramps, signals, benches
    const icons = {
        ramp: '♿',
        signal: '🚦',
        bench: '🪑',
        hospital: '🏥',
        police: '👮'
    };
    
    // Simulate markers along route
    route.coordinates.forEach((coord, i) => {
        if (i % 2 === 0 && route.ramps > 0) {
            L.marker(coord, {
                icon: L.divIcon({
                    html: '<div style="font-size:24px">♿</div>',
                    className: 'custom-marker'
                })
            }).addTo(map).bindPopup('Wheelchair Ramp');
        }
    });
}

async function loadNearbyFacilities(route) {
    const midPoint = route.coordinates[Math.floor(route.coordinates.length / 2)];
    
    try {
        const response = await fetch(`/api/nearby?lat=${midPoint[0]}&lng=${midPoint[1]}&radius=2`);
        const data = await response.json();
        
        const facilitiesDiv = document.getElementById('nearbyFacilities');
        facilitiesDiv.innerHTML = '<h6>Nearby Facilities</h6>';
        
        // Group by type
        const hospitals = data.places.filter(p => p.type === 'hospital').slice(0, 2);
        const police = data.places.filter(p => p.type === 'police').slice(0, 2);
        
        if (hospitals.length > 0) {
            facilitiesDiv.innerHTML += '<strong>🏥 Hospitals:</strong><br>';
            hospitals.forEach(h => {
                facilitiesDiv.innerHTML += `<small>${h.name} (${h.distance_km} km)</small><br>`;
                
                // Add marker
                L.marker([h.lat, h.lng], {
                    icon: L.divIcon({
                        html: '<div style="font-size:24px">🏥</div>',
                        className: 'custom-marker'
                    })
                }).addTo(map).bindPopup(`<b>${h.name}</b><br>${h.address}<br>📞 ${h.phone}`);
            });
        }
        
        if (police.length > 0) {
            facilitiesDiv.innerHTML += '<strong class="mt-2">👮 Police Stations:</strong><br>';
            police.forEach(p => {
                facilitiesDiv.innerHTML += `<small>${p.name} (${p.distance_km} km)</small><br>`;
                
                // Add marker
                L.marker([p.lat, p.lng], {
                    icon: L.divIcon({
                        html: '<div style="font-size:24px">👮</div>',
                        className: 'custom-marker'
                    })
                }).addTo(map).bindPopup(`<b>${p.name}</b><br>${p.address}`);
            });
        }
        
    } catch (error) {
        console.error('Error loading facilities:', error);
    }
}

// Voice Navigation Functions
function startVoiceNavigation() {
    if (!currentRoute) {
        alert('Please select a route first');
        return;
    }
    
    voiceActive = true;
    currentStepIndex = 0;
    
    // Generate navigation instructions
    const instructions = generateInstructions(currentRoute);
    
    // Speak first instruction
    speakInstruction(instructions[currentStepIndex]);
    
    // Auto-advance through instructions
    const interval = setInterval(() => {
        if (!voiceActive || currentStepIndex >= instructions.length - 1) {
            clearInterval(interval);
            return;
        }
        currentStepIndex++;
        speakInstruction(instructions[currentStepIndex]);
    }, 8000); // Every 8 seconds
}

function stopVoiceNavigation() {
    voiceActive = false;
    window.speechSynthesis.cancel();
}

function generateInstructions(route) {
    const instructions = [
        `Starting navigation on ${route.name}. Total distance: ${route.distance.toFixed(1)} kilometers.`,
        `This route has an accessibility score of ${route.accessibility_score} out of 100. Difficulty level: ${route.difficulty}.`
    ];
    
    // Add obstacle warnings
    if (route.obstacles.length > 0) {
        route.obstacles.forEach(obs => {
            const obsType = typeof obs === 'object' ? obs.type : obs;
            const severity = typeof obs === 'object' ? obs.severity : 'medium';
            instructions.push(`Warning: ${obsType.replace('_', ' ')} detected ahead. Severity: ${severity}. Please proceed with caution.`);
        });
    }
    
    // Add specific instructions based on route features
    if (route.ramps > 0) {
        instructions.push(`Accessible ramp ahead in 50 meters.`);
    }
    
    if (route.audio_signals) {
        instructions.push(`Audio crossing signal ahead. Listen for the beep.`);
    }
    
    if (route.benches > 0) {
        instructions.push(`Rest area with bench available in 100 meters.`);
    }
    
    if (route.gradient > 5) {
        instructions.push(`Caution: Steep gradient ahead. Gradient is ${route.gradient} percent.`);
    }
    
    // Add turn instructions (simulated)
    const coords = route.coordinates;
    for (let i = 1; i < coords.length - 1; i++) {
        const direction = Math.random() > 0.5 ? 'left' : 'right';
        instructions.push(`Turn ${direction} in ${(i * 50)} meters.`);
    }
    
    instructions.push(`You are approaching your destination.`);
    instructions.push(`You have arrived at your destination.`);
    
    return instructions;
}

function speakInstruction(text) {
    if (!voiceActive) return;
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 1;
    
    window.speechSynthesis.speak(utterance);
    
    // Show instruction on screen
    showNotification(text);
}

function showNotification(text) {
    const notification = document.createElement('div');
    notification.className = 'alert alert-info position-fixed top-0 start-50 translate-middle-x mt-3';
    notification.style.zIndex = '9999';
    notification.innerHTML = `<i class="fas fa-volume-up"></i> ${text}`;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 5000);
}

// Load obstacles from database
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
                <div style="min-width:200px">
                    <strong style="color:${color}">${icon} ${obs.type.replace('_', ' ').toUpperCase()}</strong><br>
                    <small>${obs.description || 'No description'}</small><br>
                    <span class="badge" style="background-color:${color};margin-top:5px">Severity: ${obs.severity}</span>
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
                icon: L.divIcon({
                    html: '<div style="font-size:32px">🏥</div>',
                    className: 'emergency-marker'
                })
            }).addTo(map).bindPopup(`<b>${data.nearest_hospital.name}</b><br>${data.nearest_hospital.distance_km.toFixed(2)} km`);
        }
        
        if (data.nearest_police) {
            L.marker([data.nearest_police.lat, data.nearest_police.lng], {
                icon: L.divIcon({
                    html: '<div style="font-size:32px">👮</div>',
                    className: 'emergency-marker'
                })
            }).addTo(map).bindPopup(`<b>${data.nearest_police.name}</b><br>${data.nearest_police.distance_km.toFixed(2)} km`);
        }
        
    } catch (error) {
        console.error('Error loading emergency data:', error);
        alert('Failed to load emergency information');
    }
}
