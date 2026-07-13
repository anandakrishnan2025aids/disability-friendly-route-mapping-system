// Interactive Map Enhancements - Advanced Features
class MapEnhancer {
    constructor(map) {
        this.map = map;
        this.userLocationMarker = null;
        this.userLocationCircle = null;
        this.watchId = null;
        this.animatedRoutes = [];
        this.heatmapLayer = null;
        this.alertMarkers = [];
        this.init();
    }

    init() {
        this.setupInteractiveMarkers();
        this.setupAnimatedRoutes();
        this.setupHoverEffects();
        this.setupLiveLocationTracking();
        this.setupAccessibilityHeatmap();
        this.setupSmartSuggestions();
        this.setupVoiceVisualFeedback();
        this.enhanceFloatingButtons();
    }

    // 1. Interactive Popups for All Markers
    createInteractivePopup(marker, data) {
        const popupContent = `
            <div class="interactive-popup">
                <div class="popup-header" style="background: linear-gradient(135deg, ${data.color || '#10e8b8'} 0%, ${this.darkenColor(data.color || '#10e8b8')} 100%);">
                    <div class="popup-icon">${data.icon || '📍'}</div>
                    <div class="popup-title">${data.name}</div>
                </div>
                
                <div class="popup-body">
                    ${data.distance ? `
                        <div class="popup-metric">
                            <span class="metric-icon">📏</span>
                            <span class="metric-label">Distance:</span>
                            <span class="metric-value">${data.distance.toFixed(2)} km</span>
                        </div>
                    ` : ''}
                    
                    ${data.accessibilityScore ? `
                        <div class="popup-metric">
                            <span class="metric-icon">♿</span>
                            <span class="metric-label">Accessibility:</span>
                            <span class="metric-value" style="color: ${this.getScoreColor(data.accessibilityScore)}">${data.accessibilityScore}%</span>
                        </div>
                    ` : ''}
                    
                    ${data.description ? `
                        <div class="popup-description">${data.description}</div>
                    ` : ''}
                    
                    ${data.features ? `
                        <div class="popup-features">
                            ${data.features.map(f => `<span class="feature-badge">${f}</span>`).join('')}
                        </div>
                    ` : ''}
                </div>
                
                <div class="popup-actions">
                    <button class="popup-btn navigate-btn" onclick="mapEnhancer.navigateTo(${data.lat}, ${data.lng}, '${data.name}')">
                        <span class="btn-icon">🧭</span>
                        <span class="btn-text">Navigate</span>
                    </button>
                    <button class="popup-btn report-btn" onclick="mapEnhancer.reportIssue(${data.lat}, ${data.lng}, '${data.name}')">
                        <span class="btn-icon">⚠️</span>
                        <span class="btn-text">Report</span>
                    </button>
                    ${data.phone ? `
                        <button class="popup-btn call-btn" onclick="window.location.href='tel:${data.phone}'">
                            <span class="btn-icon">📞</span>
                            <span class="btn-text">Call</span>
                        </button>
                    ` : ''}
                </div>
            </div>
        `;

        marker.bindPopup(popupContent, {
            maxWidth: 300,
            className: 'enhanced-popup',
            closeButton: true
        });

        // Add tooltip on hover
        if (data.name) {
            marker.bindTooltip(data.name, {
                permanent: false,
                direction: 'top',
                className: 'marker-tooltip',
                offset: [0, -20]
            });
        }

        return marker;
    }

    // 2. Animated Route Drawing with Direction Indicators
    animateRoute(coordinates, color, duration = 2000) {
        const animatedPolyline = L.polyline([], {
            color: color,
            weight: 6,
            opacity: 0.8,
            smoothFactor: 1
        }).addTo(this.map);

        let index = 0;
        const totalPoints = coordinates.length;
        const interval = duration / totalPoints;

        const animate = () => {
            if (index < totalPoints) {
                animatedPolyline.addLatLng(coordinates[index]);
                
                // Add direction arrow every 5 points
                if (index % 5 === 0 && index > 0) {
                    this.addDirectionArrow(
                        coordinates[index - 1],
                        coordinates[index],
                        color
                    );
                }
                
                index++;
                setTimeout(animate, interval);
            } else {
                // Add pulsing effect at end
                this.addPulsingMarker(coordinates[totalPoints - 1], color);
            }
        };

        animate();
        this.animatedRoutes.push(animatedPolyline);
        return animatedPolyline;
    }

    addDirectionArrow(from, to, color) {
        const angle = Math.atan2(to[0] - from[0], to[1] - from[1]) * 180 / Math.PI;
        
        const arrowIcon = L.divIcon({
            html: `<div style="transform: rotate(${angle}deg); color: ${color}; font-size: 20px;">➤</div>`,
            className: 'direction-arrow',
            iconSize: [20, 20]
        });

        L.marker(from, { icon: arrowIcon }).addTo(this.map);
    }

    addPulsingMarker(coords, color) {
        const pulsingIcon = L.divIcon({
            html: `
                <div class="pulsing-marker" style="background: ${color};">
                    <div class="pulse-ring" style="border-color: ${color};"></div>
                </div>
            `,
            className: 'pulsing-marker-container',
            iconSize: [30, 30]
        });

        L.marker(coords, { icon: pulsingIcon }).addTo(this.map);
    }

    // 3. Hover and Click Effects on Routes
    setupRouteInteractions(polyline, routeData) {
        polyline.on('mouseover', (e) => {
            polyline.setStyle({
                weight: 8,
                opacity: 1
            });
            
            // Show route info tooltip
            const tooltip = L.tooltip({
                permanent: false,
                direction: 'top',
                className: 'route-tooltip'
            })
            .setContent(`
                <div class="route-tooltip-content">
                    <strong>${routeData.name}</strong><br>
                    ${routeData.distance.toFixed(2)} km • ${routeData.estimatedTime}
                </div>
            `)
            .setLatLng(e.latlng)
            .addTo(this.map);

            polyline._tooltip = tooltip;
        });

        polyline.on('mouseout', (e) => {
            if (!polyline._selected) {
                polyline.setStyle({
                    weight: 5,
                    opacity: 0.7
                });
            }
            
            if (polyline._tooltip) {
                this.map.removeLayer(polyline._tooltip);
            }
        });

        polyline.on('click', (e) => {
            this.selectRoute(polyline, routeData);
        });
    }

    selectRoute(selectedPolyline, routeData) {
        // Fade all other routes
        this.animatedRoutes.forEach(route => {
            if (route !== selectedPolyline) {
                route.setStyle({
                    weight: 3,
                    opacity: 0.3
                });
                route._selected = false;
            }
        });

        // Highlight selected route
        selectedPolyline.setStyle({
            weight: 8,
            opacity: 1
        });
        selectedPolyline._selected = true;

        // Smooth zoom to route
        const bounds = selectedPolyline.getBounds();
        this.map.flyToBounds(bounds, {
            padding: [50, 50],
            duration: 1.5,
            easeLinearity: 0.25
        });

        // Update smart panel
        if (window.smartPanel) {
            smartPanel.updateSmartPanel(routeData);
        }

        // Voice announcement
        if (voiceEnabled) {
            speak(`Selected ${routeData.name}`);
        }
    }

    // 4. Live User Location Tracking
    setupLiveLocationTracking() {
        if (!navigator.geolocation) {
            console.log('Geolocation not supported');
            return;
        }

        const locationOptions = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        };

        this.watchId = navigator.geolocation.watchPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                const accuracy = position.coords.accuracy;

                this.updateUserLocation(lat, lng, accuracy);
            },
            (error) => {
                console.error('Location error:', error);
            },
            locationOptions
        );
    }

    updateUserLocation(lat, lng, accuracy) {
        // Remove old marker and circle
        if (this.userLocationMarker) {
            this.map.removeLayer(this.userLocationMarker);
        }
        if (this.userLocationCircle) {
            this.map.removeLayer(this.userLocationCircle);
        }

        // Create pulsing user location marker
        const userIcon = L.divIcon({
            html: `
                <div class="user-location-marker">
                    <div class="user-location-dot"></div>
                    <div class="user-location-pulse"></div>
                </div>
            `,
            className: 'user-location-container',
            iconSize: [40, 40]
        });

        this.userLocationMarker = L.marker([lat, lng], { icon: userIcon })
            .addTo(this.map)
            .bindPopup(`
                <div class="user-location-popup">
                    <strong>📍 Your Location</strong><br>
                    Accuracy: ±${accuracy.toFixed(0)}m
                </div>
            `);

        // Add accuracy circle
        this.userLocationCircle = L.circle([lat, lng], {
            radius: accuracy,
            color: '#10e8b8',
            fillColor: '#10e8b8',
            fillOpacity: 0.1,
            weight: 2
        }).addTo(this.map);

        // Update user location globally
        userLocation = { lat, lng };

        // Update nearby essentials
        if (window.smartPanel) {
            smartPanel.updateNearbyEssentials(userLocation);
        }
    }

    // 5. Accessibility Heatmap Overlay
    setupAccessibilityHeatmap() {
        // Create heatmap data based on accessibility scores
        const heatmapData = this.generateHeatmapData();

        // Use Leaflet.heat plugin or custom implementation
        this.heatmapLayer = L.layerGroup();

        heatmapData.forEach(point => {
            const color = this.getAccessibilityColor(point.score);
            const circle = L.circle([point.lat, point.lng], {
                radius: 100,
                color: color,
                fillColor: color,
                fillOpacity: 0.3,
                weight: 1
            });

            circle.bindTooltip(`Accessibility: ${point.score}%`, {
                permanent: false,
                direction: 'top'
            });

            this.heatmapLayer.addLayer(circle);
        });

        // Add toggle control
        this.addHeatmapToggle();
    }

    generateHeatmapData() {
        // Generate sample heatmap data
        const data = [];
        const bounds = this.map.getBounds();
        const latStep = (bounds.getNorth() - bounds.getSouth()) / 20;
        const lngStep = (bounds.getEast() - bounds.getWest()) / 20;

        for (let lat = bounds.getSouth(); lat < bounds.getNorth(); lat += latStep) {
            for (let lng = bounds.getWest(); lng < bounds.getEast(); lng += lngStep) {
                data.push({
                    lat: lat,
                    lng: lng,
                    score: Math.floor(Math.random() * 40) + 60 // 60-100
                });
            }
        }

        return data;
    }

    addHeatmapToggle() {
        const HeatmapControl = L.Control.extend({
            options: { position: 'topleft' },
            onAdd: function(map) {
                const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
                container.innerHTML = `
                    <a href="#" class="heatmap-toggle" title="Toggle Accessibility Heatmap">
                        <span class="heatmap-icon">🗺️</span>
                    </a>
                `;
                
                L.DomEvent.on(container, 'click', function(e) {
                    L.DomEvent.stopPropagation(e);
                    L.DomEvent.preventDefault(e);
                    mapEnhancer.toggleHeatmap();
                });
                
                return container;
            }
        });

        this.map.addControl(new HeatmapControl());
    }

    toggleHeatmap() {
        if (this.map.hasLayer(this.heatmapLayer)) {
            this.map.removeLayer(this.heatmapLayer);
        } else {
            this.map.addLayer(this.heatmapLayer);
        }
    }

    // 6. Real-time Alert Popups for Obstacles
    addObstacleAlert(lat, lng, obstacleData) {
        const alertIcon = L.divIcon({
            html: `
                <div class="obstacle-alert-marker" style="background: ${this.getSeverityColor(obstacleData.severity)};">
                    <div class="alert-icon">${this.getSeverityIcon(obstacleData.severity)}</div>
                    <div class="alert-pulse"></div>
                </div>
            `,
            className: 'obstacle-alert-container',
            iconSize: [40, 40]
        });

        const alertMarker = L.marker([lat, lng], { icon: alertIcon })
            .addTo(this.map);

        const popupContent = `
            <div class="obstacle-alert-popup">
                <div class="alert-header" style="background: ${this.getSeverityColor(obstacleData.severity)};">
                    <span class="alert-header-icon">${this.getSeverityIcon(obstacleData.severity)}</span>
                    <span class="alert-header-text">${obstacleData.type}</span>
                </div>
                <div class="alert-body">
                    <p>${obstacleData.description}</p>
                    <div class="alert-meta">
                        <span>Severity: <strong>${obstacleData.severity}</strong></span>
                        <span>Reported: ${this.timeAgo(obstacleData.created_at)}</span>
                    </div>
                </div>
                <div class="alert-actions">
                    <button class="alert-btn" onclick="mapEnhancer.avoidObstacle(${lat}, ${lng})">
                        🚫 Avoid
                    </button>
                    <button class="alert-btn" onclick="mapEnhancer.confirmObstacle(${obstacleData.id})">
                        ✓ Confirm
                    </button>
                </div>
            </div>
        `;

        alertMarker.bindPopup(popupContent, {
            className: 'obstacle-popup',
            maxWidth: 300
        });

        // Auto-open popup for critical obstacles
        if (obstacleData.severity === 'critical') {
            alertMarker.openPopup();
            
            // Voice alert
            if (voiceEnabled) {
                speak(`Critical obstacle detected: ${obstacleData.type}`);
            }
        }

        this.alertMarkers.push(alertMarker);
        return alertMarker;
    }

    // 7. Smart Suggestions on Map Load
    setupSmartSuggestions() {
        setTimeout(() => {
            this.showSmartSuggestions();
        }, 2000);
    }

    async showSmartSuggestions() {
        if (!userLocation) return;

        try {
            const response = await fetch(`/api/nearby?lat=${userLocation.lat}&lng=${userLocation.lng}&radius=1`);
            const data = await response.json();

            const suggestions = data.places.slice(0, 3);

            if (suggestions.length > 0) {
                const suggestionPanel = L.control({ position: 'bottomleft' });
                
                suggestionPanel.onAdd = function() {
                    const div = L.DomUtil.create('div', 'smart-suggestions');
                    div.innerHTML = `
                        <div class="suggestions-header">
                            <span class="suggestions-icon">💡</span>
                            <span class="suggestions-title">Nearby Facilities</span>
                            <button class="suggestions-close" onclick="this.parentElement.parentElement.remove()">×</button>
                        </div>
                        <div class="suggestions-list">
                            ${suggestions.map(s => `
                                <div class="suggestion-item" onclick="mapEnhancer.navigateTo(${s.lat}, ${s.lng}, '${s.name}')">
                                    <span class="suggestion-icon">${this.getTypeIcon(s.type)}</span>
                                    <div class="suggestion-info">
                                        <div class="suggestion-name">${s.name}</div>
                                        <div class="suggestion-distance">${s.distance_km.toFixed(2)} km away</div>
                                    </div>
                                    <span class="suggestion-arrow">→</span>
                                </div>
                            `).join('')}
                        </div>
                    `;
                    return div;
                };

                suggestionPanel.addTo(this.map);

                // Auto-hide after 10 seconds
                setTimeout(() => {
                    const panel = document.querySelector('.smart-suggestions');
                    if (panel) {
                        panel.style.animation = 'slideOut 0.3s ease';
                        setTimeout(() => panel.remove(), 300);
                    }
                }, 10000);
            }
        } catch (error) {
            console.error('Error loading suggestions:', error);
        }
    }

    // 8. Voice Navigation Visual Feedback
    setupVoiceVisualFeedback() {
        const voiceIndicator = L.control({ position: 'topright' });
        
        voiceIndicator.onAdd = function() {
            const div = L.DomUtil.create('div', 'voice-indicator');
            div.innerHTML = `
                <div class="voice-wave">
                    <div class="wave-bar"></div>
                    <div class="wave-bar"></div>
                    <div class="wave-bar"></div>
                    <div class="wave-bar"></div>
                </div>
                <div class="voice-text">Listening...</div>
            `;
            div.style.display = 'none';
            return div;
        };

        voiceIndicator.addTo(this.map);
    }

    showVoiceIndicator() {
        const indicator = document.querySelector('.voice-indicator');
        if (indicator) {
            indicator.style.display = 'flex';
        }
    }

    hideVoiceIndicator() {
        const indicator = document.querySelector('.voice-indicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    }

    // 9. Enhanced Floating Buttons
    enhanceFloatingButtons() {
        const buttons = document.querySelectorAll('.floating-btn');
        
        buttons.forEach(btn => {
            // Add hover label
            const label = btn.getAttribute('title');
            if (label) {
                const labelDiv = document.createElement('div');
                labelDiv.className = 'floating-btn-label';
                labelDiv.textContent = label;
                btn.appendChild(labelDiv);
            }

            // Add ripple effect
            btn.addEventListener('click', (e) => {
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                btn.appendChild(ripple);

                const rect = btn.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = e.clientX - rect.left - size / 2 + 'px';
                ripple.style.top = e.clientY - rect.top - size / 2 + 'px';

                setTimeout(() => ripple.remove(), 600);
            });
        });
    }

    // Helper Methods
    navigateTo(lat, lng, name) {
        this.map.flyTo([lat, lng], 16, {
            duration: 1.5,
            easeLinearity: 0.25
        });

        if (voiceEnabled) {
            speak(`Navigating to ${name}`);
        }
    }

    reportIssue(lat, lng, name) {
        // Open report modal or redirect
        console.log(`Report issue at ${name}`);
        if (voiceEnabled) {
            speak(`Opening report form for ${name}`);
        }
    }

    avoidObstacle(lat, lng) {
        console.log(`Avoiding obstacle at ${lat}, ${lng}`);
        // Recalculate route avoiding this point
    }

    confirmObstacle(id) {
        console.log(`Confirming obstacle ${id}`);
        // Update obstacle confirmation count
    }

    getScoreColor(score) {
        if (score >= 90) return '#10e8b8';
        if (score >= 75) return '#ffc35a';
        return '#ff5c7a';
    }

    getAccessibilityColor(score) {
        if (score >= 90) return '#10e8b8';
        if (score >= 80) return '#5b9dff';
        if (score >= 70) return '#ffc35a';
        return '#ff5c7a';
    }

    getSeverityColor(severity) {
        const colors = {
            critical: '#ff5c7a',
            high: '#ff8c42',
            medium: '#ffc35a',
            low: '#10e8b8'
        };
        return colors[severity] || '#ffc35a';
    }

    getSeverityIcon(severity) {
        const icons = {
            critical: '🚫',
            high: '⚠️',
            medium: '⚡',
            low: 'ℹ️'
        };
        return icons[severity] || '⚠️';
    }

    getTypeIcon(type) {
        const icons = {
            hospital: '🏥',
            police: '👮',
            toilet: '🚻',
            parking: '🅿️',
            accessible: '♿'
        };
        return icons[type] || '📍';
    }

    darkenColor(color) {
        // Simple color darkening
        return color.replace(/[0-9a-f]/gi, (c) => {
            const val = parseInt(c, 16);
            return Math.max(0, val - 2).toString(16);
        });
    }

    timeAgo(timestamp) {
        const now = new Date();
        const then = new Date(timestamp);
        const diff = Math.floor((now - then) / 1000);

        if (diff < 60) return 'Just now';
        if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
        if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
        return `${Math.floor(diff / 86400)}d ago`;
    }

    // Cleanup
    destroy() {
        if (this.watchId) {
            navigator.geolocation.clearWatch(this.watchId);
        }
        this.animatedRoutes.forEach(route => this.map.removeLayer(route));
        this.alertMarkers.forEach(marker => this.map.removeLayer(marker));
    }
}

// Initialize Map Enhancer
let mapEnhancer;
