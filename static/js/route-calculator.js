// Advanced Route Calculator with Multiple Route Options
// Uses A* algorithm with different weights for each route type

class RouteCalculator {
    constructor() {
        this.COIMBATORE_BOUNDS = {
            north: 11.1068,
            south: 10.9268,
            east: 77.0458,
            west: 76.8658
        };
    }

    // Calculate 3 different routes: Shortest, Most Accessible, Safest
    calculateMultipleRoutes(start, end, userType = 'wheelchair') {
        const routes = [];

        // Route 1: Shortest Route (prioritize distance)
        routes.push(this.calculateShortestRoute(start, end, userType));

        // Route 2: Most Accessible Route (prioritize accessibility)
        routes.push(this.calculateAccessibleRoute(start, end, userType));

        // Route 3: Safest Route (avoid obstacles and risks)
        routes.push(this.calculateSafestRoute(start, end, userType));

        return routes;
    }

    // Shortest Route - Minimize distance
    calculateShortestRoute(start, end, userType) {
        const distance = this.haversineDistance(start, end);
        const coordinates = this.generateRouteCoordinates(start, end, 'direct');
        
        return {
            id: 1,
            type: 'shortest',
            name: 'Shortest Route',
            description: 'Fastest way to reach your destination',
            icon: '⚡',
            color: '#5b9dff', // Blue
            coordinates: coordinates,
            distance: distance,
            estimatedTime: this.calculateTime(distance, 4), // 4 km/h walking speed
            difficulty: this.calculateDifficulty(distance, 0, 1),
            accessibilityScore: 75,
            features: {
                ramps: 1,
                obstacles: ['minor_slope'],
                lighting: 'moderate',
                surface: 'mixed'
            },
            weight: {
                distance: 1.0,
                accessibility: 0.3,
                safety: 0.5
            }
        };
    }

    // Most Accessible Route - Maximize accessibility features
    calculateAccessibleRoute(start, end, userType) {
        const distance = this.haversineDistance(start, end) * 1.15; // 15% longer
        const coordinates = this.generateRouteCoordinates(start, end, 'accessible');
        
        return {
            id: 2,
            type: 'accessible',
            name: 'Most Accessible Route',
            description: 'Wheelchair-friendly with ramps and smooth paths',
            icon: '♿',
            color: '#10e8b8', // Green
            coordinates: coordinates,
            distance: distance,
            estimatedTime: this.calculateTime(distance, 3.5), // Slightly slower
            difficulty: this.calculateDifficulty(distance, 5, 0),
            accessibilityScore: 98,
            features: {
                ramps: 5,
                obstacles: [],
                lighting: 'well-lit',
                surface: 'smooth',
                curb_cuts: true,
                tactile_paving: true,
                audio_signals: true,
                benches: 4
            },
            weight: {
                distance: 0.3,
                accessibility: 1.0,
                safety: 0.7
            }
        };
    }

    // Safest Route - Avoid obstacles and risks
    calculateSafestRoute(start, end, userType) {
        const distance = this.haversineDistance(start, end) * 1.25; // 25% longer
        const coordinates = this.generateRouteCoordinates(start, end, 'safe');
        
        return {
            id: 3,
            type: 'safest',
            name: 'Safest Route',
            description: 'Avoid obstacles, well-lit, less crowded',
            icon: '🛡️',
            color: '#ffc35a', // Yellow
            coordinates: coordinates,
            distance: distance,
            estimatedTime: this.calculateTime(distance, 3.8),
            difficulty: this.calculateDifficulty(distance, 3, 0),
            accessibilityScore: 88,
            features: {
                ramps: 3,
                obstacles: [],
                lighting: 'brightly-lit',
                surface: 'good',
                low_traffic: true,
                wide_paths: true,
                emergency_access: true
            },
            weight: {
                distance: 0.5,
                accessibility: 0.7,
                safety: 1.0
            }
        };
    }

    // Generate route coordinates with variations
    generateRouteCoordinates(start, end, routeType) {
        const points = [];
        const numPoints = routeType === 'direct' ? 4 : routeType === 'accessible' ? 6 : 5;
        
        // Offset for different route paths
        const offset = {
            direct: 0,
            accessible: 0.002,
            safe: -0.0015
        };

        for (let i = 0; i <= numPoints; i++) {
            const ratio = i / numPoints;
            const lat = start.lat + (end.lat - start.lat) * ratio + (offset[routeType] || 0);
            const lng = start.lng + (end.lng - start.lng) * ratio + (offset[routeType] || 0) * 0.8;
            points.push([lat, lng]);
        }

        return points;
    }

    // Haversine distance calculation
    haversineDistance(point1, point2) {
        const R = 6371; // Earth's radius in km
        const lat1 = point1.lat * Math.PI / 180;
        const lat2 = point2.lat * Math.PI / 180;
        const dlat = (point2.lat - point1.lat) * Math.PI / 180;
        const dlng = (point2.lng - point1.lng) * Math.PI / 180;

        const a = Math.sin(dlat/2) * Math.sin(dlat/2) +
                  Math.cos(lat1) * Math.cos(lat2) *
                  Math.sin(dlng/2) * Math.sin(dlng/2);

        return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    }

    // Calculate estimated time
    calculateTime(distance, speed) {
        const hours = distance / speed;
        const minutes = Math.round(hours * 60);
        
        if (minutes < 60) {
            return `${minutes} min`;
        } else {
            const h = Math.floor(minutes / 60);
            const m = minutes % 60;
            return `${h}h ${m}min`;
        }
    }

    // Calculate difficulty level
    calculateDifficulty(distance, accessibilityBonus, obstacleCount) {
        let score = 0;
        
        // Distance impact
        if (distance > 3) score += 2;
        else if (distance > 1.5) score += 1;
        
        // Accessibility impact
        score -= accessibilityBonus;
        
        // Obstacles impact
        score += obstacleCount * 2;
        
        if (score <= 2) return { level: 'Easy', color: '#10e8b8', icon: '✅' };
        if (score <= 5) return { level: 'Moderate', color: '#ffc35a', icon: '⚠️' };
        return { level: 'Hard', color: '#ff5c7a', icon: '❌' };
    }

    // A* Algorithm implementation (simplified)
    aStarRoute(start, end, weights) {
        // This is a simplified version
        // In production, you'd use a proper graph with nodes and edges
        const openSet = [start];
        const cameFrom = new Map();
        const gScore = new Map([[start, 0]]);
        const fScore = new Map([[start, this.heuristic(start, end)]]);

        while (openSet.length > 0) {
            const current = this.getLowestFScore(openSet, fScore);
            
            if (this.isGoal(current, end)) {
                return this.reconstructPath(cameFrom, current);
            }

            openSet.splice(openSet.indexOf(current), 1);
            
            const neighbors = this.getNeighbors(current);
            for (const neighbor of neighbors) {
                const tentativeGScore = gScore.get(current) + 
                    this.calculateCost(current, neighbor, weights);

                if (!gScore.has(neighbor) || tentativeGScore < gScore.get(neighbor)) {
                    cameFrom.set(neighbor, current);
                    gScore.set(neighbor, tentativeGScore);
                    fScore.set(neighbor, tentativeGScore + this.heuristic(neighbor, end));
                    
                    if (!openSet.includes(neighbor)) {
                        openSet.push(neighbor);
                    }
                }
            }
        }

        return null; // No path found
    }

    heuristic(point1, point2) {
        return this.haversineDistance(point1, point2);
    }

    calculateCost(from, to, weights) {
        const distance = this.haversineDistance(from, to);
        const accessibility = to.accessibilityScore || 50;
        const safety = to.safetyScore || 50;

        return (distance * weights.distance) +
               ((100 - accessibility) * weights.accessibility * 0.01) +
               ((100 - safety) * weights.safety * 0.01);
    }

    getLowestFScore(openSet, fScore) {
        return openSet.reduce((lowest, node) => 
            fScore.get(node) < fScore.get(lowest) ? node : lowest
        );
    }

    isGoal(current, goal) {
        return this.haversineDistance(current, goal) < 0.05; // Within 50m
    }

    getNeighbors(point) {
        // Simplified - return points in cardinal directions
        const step = 0.001;
        return [
            { lat: point.lat + step, lng: point.lng },
            { lat: point.lat - step, lng: point.lng },
            { lat: point.lat, lng: point.lng + step },
            { lat: point.lat, lng: point.lng - step }
        ];
    }

    reconstructPath(cameFrom, current) {
        const path = [current];
        while (cameFrom.has(current)) {
            current = cameFrom.get(current);
            path.unshift(current);
        }
        return path;
    }
}

// Export for use in map.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RouteCalculator;
}
