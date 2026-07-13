// Smart Info Panel - Dynamic Route Information Display
class SmartInfoPanel {
    constructor() {
        this.currentRoute = null;
        this.nearbyEssentials = [];
        this.userPreferences = {
            mode: 'wheelchair', // wheelchair, elderly, visually_impaired
            voiceEnabled: false,
            alertsEnabled: true
        };
        this.init();
    }

    init() {
        this.createSmartPanel();
        this.createNearbyEssentialsPanel();
        this.createRouteComparisonPanel();
        this.createAccessibilityModeSelector();
        this.createFloatingControls();
        this.setupVoiceCommands();
    }

    // Create main Smart Info Panel
    createSmartPanel() {
        const panel = document.createElement('div');
        panel.id = 'smartInfoPanel';
        panel.className = 'smart-panel';
        panel.innerHTML = `
            <div class="smart-panel-header">
                <h3>📊 Route Information</h3>
                <button class="panel-toggle" onclick="smartPanel.togglePanel('info')">
                    <span class="toggle-icon">−</span>
                </button>
            </div>
            <div class="smart-panel-content" id="smartPanelContent">
                <div class="no-route-message">
                    <div class="empty-state-icon">🗺️</div>
                    <p>Search for a destination to see route details</p>
                </div>
            </div>
        `;
        
        // Insert after the filter bar
        const sidebar = document.querySelector('.map-sidebar');
        if (sidebar) {
            const filterBar = sidebar.querySelector('.filter-bar');
            if (filterBar) {
                filterBar.after(panel);
            }
        }
    }

    // Update Smart Panel with route data
    updateSmartPanel(route) {
        this.currentRoute = route;
        const content = document.getElementById('smartPanelContent');
        
        if (!route) {
            content.innerHTML = `
                <div class="no-route-message">
                    <div class="empty-state-icon">🗺️</div>
                    <p>Search for a destination to see route details</p>
                </div>
            `;
            return;
        }

        content.innerHTML = `
            <div class="route-info-grid">
                <!-- Route Header -->
                <div class="route-header" style="border-left: 4px solid ${route.color}">
                    <div class="route-title">
                        <span class="route-icon">${route.icon}</span>
                        <span class="route-name">${route.name}</span>
                    </div>
                    <div class="route-type-badge" style="background: ${route.color}20; color: ${route.color}">
                        ${route.type.toUpperCase()}
                    </div>
                </div>

                <!-- Key Metrics -->
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-icon">📏</div>
                        <div class="metric-content">
                            <div class="metric-label">Distance</div>
                            <div class="metric-value">${route.distance.toFixed(2)} km</div>
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-icon">⏱️</div>
                        <div class="metric-content">
                            <div class="metric-label">Est. Time</div>
                            <div class="metric-value">${route.estimatedTime}</div>
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-icon">${route.difficulty.icon}</div>
                        <div class="metric-content">
                            <div class="metric-label">Difficulty</div>
                            <div class="metric-value" style="color: ${route.difficulty.color}">${route.difficulty.level}</div>
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-icon">♿</div>
                        <div class="metric-content">
                            <div class="metric-label">Accessibility</div>
                            <div class="metric-value">${route.accessibilityScore}%</div>
                        </div>
                    </div>
                </div>

                <!-- Accessibility Score Bar -->
                <div class="score-bar-container">
                    <div class="score-bar-label">
                        <span>Accessibility Score</span>
                        <span class="score-value">${route.accessibilityScore}%</span>
                    </div>
                    <div class="score-bar">
                        <div class="score-bar-fill" style="width: ${route.accessibilityScore}%; background: ${this.getScoreColor(route.accessibilityScore)}"></div>
                    </div>
                </div>

                <!-- Route Features -->
                <div class="route-features">
                    <div class="features-header">Route Features</div>
                    <div class="features-grid">
                        ${route.features.ramps ? `
                            <div class="feature-item">
                                <span class="feature-icon">♿</span>
                                <span class="feature-text">${route.features.ramps} Ramps</span>
                            </div>
                        ` : ''}
                        ${route.features.benches ? `
                            <div class="feature-item">
                                <span class="feature-icon">🪑</span>
                                <span class="feature-text">${route.features.benches} Benches</span>
                            </div>
                        ` : ''}
                        ${route.features.lighting ? `
                            <div class="feature-item">
                                <span class="feature-icon">💡</span>
                                <span class="feature-text">${route.features.lighting}</span>
                            </div>
                        ` : ''}
                        ${route.features.surface ? `
                            <div class="feature-item">
                                <span class="feature-icon">🛤️</span>
                                <span class="feature-text">${route.features.surface} surface</span>
                            </div>
                        ` : ''}
                        ${route.features.audio_signals ? `
                            <div class="feature-item">
                                <span class="feature-icon">🔊</span>
                                <span class="feature-text">Audio Signals</span>
                            </div>
                        ` : ''}
                        ${route.features.tactile_paving ? `
                            <div class="feature-item">
                                <span class="feature-icon">👣</span>
                                <span class="feature-text">Tactile Paving</span>
                            </div>
                        ` : ''}
                    </div>
                </div>

                <!-- Obstacles Warning -->
                ${route.features.obstacles && route.features.obstacles.length > 0 ? `
                    <div class="obstacles-warning">
                        <div class="warning-header">
                            <span class="warning-icon">⚠️</span>
                            <span>Obstacles Detected</span>
                        </div>
                        <div class="obstacles-list">
                            ${route.features.obstacles.map(obs => `
                                <div class="obstacle-item">
                                    <span class="obstacle-dot"></span>
                                    <span>${typeof obs === 'object' ? obs.type : obs}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}

                <!-- AI Recommendation -->
                ${this.getAIRecommendation(route)}
            </div>
        `;
    }

    // Get AI-based recommendation
    getAIRecommendation(route) {
        const mode = this.userPreferences.mode;
        let recommendation = '';
        let icon = '🤖';
        let color = '#5b9dff';

        if (mode === 'wheelchair' && route.accessibilityScore >= 95) {
            recommendation = 'Highly recommended for wheelchair users';
            icon = '✅';
            color = '#10e8b8';
        } else if (mode === 'elderly' && route.features.benches >= 3) {
            recommendation = 'Good choice with frequent rest stops';
            icon = '👍';
            color = '#10e8b8';
        } else if (mode === 'visually_impaired' && route.features.audio_signals) {
            recommendation = 'Recommended with audio guidance';
            icon = '🔊';
            color = '#10e8b8';
        } else if (route.type === 'safest') {
            recommendation = 'Safest route with minimal obstacles';
            icon = '🛡️';
            color = '#ffc35a';
        } else {
            recommendation = 'Suitable for your accessibility needs';
            icon = '👌';
            color = '#5b9dff';
        }

        return `
            <div class="ai-recommendation" style="border-left-color: ${color}">
                <div class="ai-header">
                    <span class="ai-icon">${icon}</span>
                    <span class="ai-label">AI Recommendation</span>
                </div>
                <div class="ai-text">${recommendation}</div>
            </div>
        `;
    }

    // Create Nearby Essentials Panel
    createNearbyEssentialsPanel() {
        const panel = document.createElement('div');
        panel.id = 'nearbyEssentialsPanel';
        panel.className = 'smart-panel';
        panel.innerHTML = `
            <div class="smart-panel-header">
                <h3>🏥 Nearby Essentials</h3>
                <button class="panel-toggle" onclick="smartPanel.togglePanel('essentials')">
                    <span class="toggle-icon">−</span>
                </button>
            </div>
            <div class="smart-panel-content" id="nearbyEssentialsContent">
                <div class="loading-message">
                    <div class="spinner"></div>
                    <p>Loading nearby facilities...</p>
                </div>
            </div>
        `;
        
        const smartPanel = document.getElementById('smartInfoPanel');
        if (smartPanel) {
            smartPanel.after(panel);
        }
    }

    // Update Nearby Essentials
    async updateNearbyEssentials(location) {
        const content = document.getElementById('nearbyEssentialsContent');
        
        try {
            // Fetch nearby places
            const response = await fetch(`/api/nearby?lat=${location.lat}&lng=${location.lng}&radius=2`);
            const data = await response.json();
            
            const hospitals = data.places.filter(p => p.type === 'hospital').slice(0, 3);
            const toilets = data.places.filter(p => p.type === 'accessible' && p.name.toLowerCase().includes('toilet')).slice(0, 2);
            const parking = data.places.filter(p => p.type === 'accessible' && p.name.toLowerCase().includes('parking')).slice(0, 2);
            
            content.innerHTML = `
                <div class="essentials-grid">
                    <!-- Hospitals -->
                    ${hospitals.length > 0 ? `
                        <div class="essential-category">
                            <div class="category-header">
                                <span class="category-icon">🏥</span>
                                <span class="category-title">Hospitals</span>
                            </div>
                            <div class="essential-list">
                                ${hospitals.map(h => `
                                    <div class="essential-item" onclick="smartPanel.showOnMap(${h.lat}, ${h.lng}, '${h.name}')">
                                        <div class="essential-info">
                                            <div class="essential-name">${h.name}</div>
                                            <div class="essential-distance">📍 ${h.distance_km.toFixed(2)} km away</div>
                                        </div>
                                        <button class="essential-action" title="Show on map">
                                            <span>→</span>
                                        </button>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}

                    <!-- Accessible Toilets -->
                    ${toilets.length > 0 ? `
                        <div class="essential-category">
                            <div class="category-header">
                                <span class="category-icon">🚻</span>
                                <span class="category-title">Accessible Toilets</span>
                            </div>
                            <div class="essential-list">
                                ${toilets.map(t => `
                                    <div class="essential-item" onclick="smartPanel.showOnMap(${t.lat}, ${t.lng}, '${t.name}')">
                                        <div class="essential-info">
                                            <div class="essential-name">${t.name}</div>
                                            <div class="essential-distance">📍 ${t.distance_km.toFixed(2)} km away</div>
                                        </div>
                                        <button class="essential-action">→</button>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}

                    <!-- Parking -->
                    ${parking.length > 0 ? `
                        <div class="essential-category">
                            <div class="category-header">
                                <span class="category-icon">🅿️</span>
                                <span class="category-title">Accessible Parking</span>
                            </div>
                            <div class="essential-list">
                                ${parking.map(p => `
                                    <div class="essential-item" onclick="smartPanel.showOnMap(${p.lat}, ${p.lng}, '${p.name}')">
                                        <div class="essential-info">
                                            <div class="essential-name">${p.name}</div>
                                            <div class="essential-distance">📍 ${p.distance_km.toFixed(2)} km away</div>
                                        </div>
                                        <button class="essential-action">→</button>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}

                    ${hospitals.length === 0 && toilets.length === 0 && parking.length === 0 ? `
                        <div class="no-essentials">
                            <div class="empty-state-icon">🔍</div>
                            <p>No nearby facilities found</p>
                        </div>
                    ` : ''}
                </div>
            `;
        } catch (error) {
            content.innerHTML = `
                <div class="error-message">
                    <div class="error-icon">⚠️</div>
                    <p>Failed to load nearby facilities</p>
                </div>
            `;
        }
    }

    // Create Route Comparison Panel
    createRouteComparisonPanel() {
        const panel = document.createElement('div');
        panel.id = 'routeComparisonPanel';
        panel.className = 'smart-panel collapsed';
        panel.innerHTML = `
            <div class="smart-panel-header">
                <h3>📊 Route Comparison</h3>
                <button class="panel-toggle" onclick="smartPanel.togglePanel('comparison')">
                    <span class="toggle-icon">+</span>
                </button>
            </div>
            <div class="smart-panel-content" id="routeComparisonContent" style="display: none;">
                <div class="comparison-placeholder">
                    <p>Select routes to compare</p>
                </div>
            </div>
        `;
        
        const nearbyPanel = document.getElementById('nearbyEssentialsPanel');
        if (nearbyPanel) {
            nearbyPanel.after(panel);
        }
    }

    // Update Route Comparison
    updateRouteComparison(routes) {
        const content = document.getElementById('routeComparisonContent');
        
        if (!routes || routes.length === 0) {
            content.innerHTML = `
                <div class="comparison-placeholder">
                    <p>No routes to compare</p>
                </div>
            `;
            return;
        }

        content.innerHTML = `
            <div class="comparison-table">
                <div class="comparison-header">
                    <div class="comparison-cell">Feature</div>
                    ${routes.map(r => `
                        <div class="comparison-cell" style="color: ${r.color}">
                            ${r.icon} ${r.type}
                        </div>
                    `).join('')}
                </div>
                
                <div class="comparison-row">
                    <div class="comparison-cell">Distance</div>
                    ${routes.map(r => `
                        <div class="comparison-cell">${r.distance.toFixed(2)} km</div>
                    `).join('')}
                </div>
                
                <div class="comparison-row">
                    <div class="comparison-cell">Time</div>
                    ${routes.map(r => `
                        <div class="comparison-cell">${r.estimatedTime}</div>
                    `).join('')}
                </div>
                
                <div class="comparison-row">
                    <div class="comparison-cell">Accessibility</div>
                    ${routes.map(r => `
                        <div class="comparison-cell">
                            <span style="color: ${this.getScoreColor(r.accessibilityScore)}">${r.accessibilityScore}%</span>
                        </div>
                    `).join('')}
                </div>
                
                <div class="comparison-row">
                    <div class="comparison-cell">Difficulty</div>
                    ${routes.map(r => `
                        <div class="comparison-cell">
                            <span style="color: ${r.difficulty.color}">${r.difficulty.level}</span>
                        </div>
                    `).join('')}
                </div>
                
                <div class="comparison-row">
                    <div class="comparison-cell">Ramps</div>
                    ${routes.map(r => `
                        <div class="comparison-cell">${r.features.ramps || 0}</div>
                    `).join('')}
                </div>
                
                <div class="comparison-row">
                    <div class="comparison-cell">Obstacles</div>
                    ${routes.map(r => `
                        <div class="comparison-cell">${r.features.obstacles?.length || 0}</div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // Create Accessibility Mode Selector
    createAccessibilityModeSelector() {
        const selector = document.createElement('div');
        selector.id = 'accessibilityModeSelector';
        selector.className = 'mode-selector';
        selector.innerHTML = `
            <div class="mode-selector-header">
                <span class="mode-icon">♿</span>
                <span class="mode-label">Accessibility Mode</span>
            </div>
            <div class="mode-options">
                <button class="mode-btn active" data-mode="wheelchair" onclick="smartPanel.setMode('wheelchair')">
                    <span class="mode-btn-icon">♿</span>
                    <span class="mode-btn-text">Wheelchair</span>
                </button>
                <button class="mode-btn" data-mode="elderly" onclick="smartPanel.setMode('elderly')">
                    <span class="mode-btn-icon">🧓</span>
                    <span class="mode-btn-text">Elderly</span>
                </button>
                <button class="mode-btn" data-mode="visually_impaired" onclick="smartPanel.setMode('visually_impaired')">
                    <span class="mode-btn-icon">👁️</span>
                    <span class="mode-btn-text">Visual</span>
                </button>
            </div>
        `;
        
        const sidebar = document.querySelector('.map-sidebar');
        if (sidebar) {
            const header = sidebar.querySelector('.sidebar-header');
            if (header) {
                header.after(selector);
            }
        }
    }

    // Set accessibility mode
    setMode(mode) {
        this.userPreferences.mode = mode;
        
        // Update button states
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });
        
        // Speak mode change
        if (voiceEnabled) {
            speak(`Accessibility mode changed to ${mode.replace('_', ' ')}`);
        }
        
        // Trigger route recalculation if route exists
        if (this.currentRoute) {
            // Recalculate routes with new mode
            console.log(`Recalculating routes for ${mode} mode`);
        }
    }

    // Create Floating Controls
    createFloatingControls() {
        const controls = document.createElement('div');
        controls.id = 'floatingControls';
        controls.className = 'floating-controls';
        controls.innerHTML = `
            <button class="floating-btn emergency-btn" onclick="smartPanel.triggerEmergency()" title="Emergency">
                <span class="btn-icon">🆘</span>
            </button>
            <button class="floating-btn voice-btn" onclick="smartPanel.toggleVoiceAssistant()" title="Voice Assistant">
                <span class="btn-icon">🎤</span>
            </button>
            <button class="floating-btn alerts-btn active" onclick="smartPanel.toggleAlerts()" title="Safety Alerts">
                <span class="btn-icon">🔔</span>
            </button>
            <button class="floating-btn location-btn" onclick="getUserLocation(true)" title="My Location">
                <span class="btn-icon">📍</span>
            </button>
        `;
        
        document.body.appendChild(controls);
    }

    // Helper methods
    togglePanel(panelType) {
        const panels = {
            'info': 'smartInfoPanel',
            'essentials': 'nearbyEssentialsPanel',
            'comparison': 'routeComparisonPanel'
        };
        
        const panelId = panels[panelType];
        const panel = document.getElementById(panelId);
        const content = panel.querySelector('.smart-panel-content');
        const toggle = panel.querySelector('.toggle-icon');
        
        if (panel.classList.contains('collapsed')) {
            panel.classList.remove('collapsed');
            content.style.display = 'block';
            toggle.textContent = '−';
        } else {
            panel.classList.add('collapsed');
            content.style.display = 'none';
            toggle.textContent = '+';
        }
    }

    getScoreColor(score) {
        if (score >= 90) return '#10e8b8';
        if (score >= 75) return '#ffc35a';
        return '#ff5c7a';
    }

    showOnMap(lat, lng, name) {
        map.setView([lat, lng], 16);
        L.marker([lat, lng]).addTo(map).bindPopup(`<b>${name}</b>`).openPopup();
        if (voiceEnabled) {
            speak(`Showing ${name} on map`);
        }
    }

    triggerEmergency() {
        showEmergencyPanel();
    }

    toggleVoiceAssistant() {
        toggleVoice();
        const btn = document.querySelector('.voice-btn');
        btn.classList.toggle('active');
    }

    toggleAlerts() {
        this.userPreferences.alertsEnabled = !this.userPreferences.alertsEnabled;
        const btn = document.querySelector('.alerts-btn');
        btn.classList.toggle('active');
        
        if (voiceEnabled) {
            speak(`Safety alerts ${this.userPreferences.alertsEnabled ? 'enabled' : 'disabled'}`);
        }
    }

    // Voice Commands Setup
    setupVoiceCommands() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            
            this.recognition.onresult = (event) => {
                const command = event.results[0][0].transcript.toLowerCase();
                this.processVoiceCommand(command);
            };
        }
    }

    processVoiceCommand(command) {
        if (command.includes('search') || command.includes('find')) {
            const query = command.replace('search', '').replace('find', '').trim();
            document.getElementById('routeSearch').value = query;
            speak(`Searching for ${query}`);
        } else if (command.includes('emergency')) {
            this.triggerEmergency();
        } else if (command.includes('navigate') || command.includes('start')) {
            if (this.currentRoute) {
                startRouteVoiceNavigation(this.currentRoute);
            }
        }
    }
}

// Initialize Smart Panel
let smartPanel;
document.addEventListener('DOMContentLoaded', () => {
    smartPanel = new SmartInfoPanel();
});
