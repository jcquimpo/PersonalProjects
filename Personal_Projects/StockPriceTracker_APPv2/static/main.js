/* ============================================================================
   STOCK ANALYSIS DASHBOARD - MAIN JAVASCRIPT
   ============================================================================ */

// API Helper Functions
const API = {
    async get(endpoint) {
        try {
            const response = await fetch(endpoint);
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}`);
            }
            return data;
        } catch (error) {
            console.error(`API GET ${endpoint}:`, error);
            throw error;
        }
    },

    async post(endpoint, data = {}) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const responseData = await response.json();
            if (!response.ok) {
                throw new Error(responseData.error || `HTTP ${response.status}`);
            }
            return responseData;
        } catch (error) {
            console.error(`API POST ${endpoint}:`, error);
            throw error;
        }
    }
};

// UI Helper Functions
const UI = {
    showSpinner(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div class="loading-container">
                    <div class="spinner"></div>
                    <div class="loading-text">Running analysis...</div>
                </div>
            `;
        }
    },

    showAlert(message, type = 'info') {
        const alertHtml = `
            <div class="alert alert-${type}" role="alert">
                <strong>${type.toUpperCase()}:</strong> ${message}
            </div>
        `;
        const container = document.querySelector('.container');
        if (container) {
            container.insertAdjacentHTML('afterbegin', alertHtml);
            setTimeout(() => {
                const alert = container.querySelector('.alert');
                if (alert) alert.remove();
            }, 5000);
        }
    },

    formatNumber(num, decimals = 2) {
        return parseFloat(num).toFixed(decimals);
    },

    formatCurrency(num) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(num);
    },

    formatPercent(num) {
        const formatted = parseFloat(num).toFixed(2);
        return `${formatted > 0 ? '+' : ''}${formatted}%`;
    },

    getPercentageClass(value) {
        if (value > 0) return 'pct-positive';
        if (value < 0) return 'pct-negative';
        return 'pct-neutral';
    },

    getBadgeClass(recommendation) {
        if (recommendation.includes('BUY')) return 'badge-buy';
        if (recommendation.includes('HOLD')) return 'badge-hold';
        if (recommendation.includes('SELL')) return 'badge-sell';
        return 'badge-warning';
    }
};

// Chart Functions
const Charts = {
    moverPerformanceChart: null,
    watchlistPerformanceChart: null,
    moverScoresChart: null,

    async loadMoverPerformanceChart(canvasId) {
        try {
            const data = await API.get('/api/chart-data/mover-performance');
            const ctx = document.getElementById(canvasId);
            if (!ctx) return;

            if (this.moverPerformanceChart) this.moverPerformanceChart.destroy();

            this.moverPerformanceChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels || [],
                    datasets: [{
                        label: 'Daily % Change',
                        data: data.data || [],
                        backgroundColor: (data.data || []).map(v => v >= 0 ? '#2ecc71' : '#e74c3c'),
                        borderRadius: 8,
                        borderSkipped: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            ticks: { callback: v => v.toFixed(2) + '%' }
                        }
                    }
                }
            });
        } catch (error) {
            console.warn('Chart data not available yet:', error.message);
        }
    },

    async loadWatchlistPerformanceChart(canvasId) {
        try {
            const data = await API.get('/api/chart-data/watchlist-performance');
            const ctx = document.getElementById(canvasId);
            if (!ctx) return;

            if (this.watchlistPerformanceChart) this.watchlistPerformanceChart.destroy();

            this.watchlistPerformanceChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels || [],
                    datasets: [{
                        label: 'Daily % Change',
                        data: data.data || [],
                        backgroundColor: (data.data || []).map(v => v >= 0 ? '#2ecc71' : '#e74c3c'),
                        borderRadius: 8,
                        borderSkipped: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            ticks: { callback: v => v.toFixed(2) + '%' }
                        }
                    }
                }
            });
        } catch (error) {
            console.warn('Chart data not available yet:', error.message);
        }
    },

    async loadMoverScoresChart(canvasId) {
        try {
            const data = await API.get('/api/chart-data/mover-scores');
            const ctx = document.getElementById(canvasId);
            if (!ctx) return;

            if (this.moverScoresChart) this.moverScoresChart.destroy();

            this.moverScoresChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.labels || [],
                    datasets: [{
                        data: data.data || [],
                        backgroundColor: [
                            '#667eea', '#764ba2', '#2ecc71', '#f39c12', '#e74c3c'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Failed to load mover scores chart:', error);
        }
    }
};

// Analysis Functions
const Analysis = {
    async startAnalysis() {
        try {
            UI.showSpinner('analysis-status');
            const result = await API.post('/api/run-analysis');
            UI.showAlert('Analysis started! This may take a few minutes...', 'info');
            this.pollAnalysisStatus();
        } catch (error) {
            UI.showAlert('Failed to start analysis: ' + error.message, 'danger');
        }
    },

    async pollAnalysisStatus() {
        try {
            const status = await API.get('/api/status');

            if (status.is_running) {
                const statusDiv = document.getElementById('analysis-status');
                if (statusDiv) {
                    statusDiv.innerHTML = `
                        <div class="loading-container">
                            <div class="spinner"></div>
                            <div class="loading-text">Analysis in progress...</div>
                        </div>
                    `;
                }
                setTimeout(() => this.pollAnalysisStatus(), 2000);
            } else {
                const statusDiv = document.getElementById('analysis-status');
                if (statusDiv) {
                    if (status.error) {
                        statusDiv.innerHTML = `
                            <div class="alert alert-danger">
                                <strong>Error:</strong> ${status.error}
                            </div>
                        `;
                    } else if (status.has_results) {
                        statusDiv.innerHTML = `
                            <div class="alert alert-success">
                                <strong>Success!</strong> Analysis complete.
                            </div>
                        `;
                        // Refresh dashboard data and charts
                        if (typeof Dashboard !== 'undefined') {
                            Dashboard.loadCharts();
                            Dashboard.loadData();
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error polling analysis status:', error);
        }
    }
};

// Document Ready - Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Load charts if they exist on the page
    if (document.getElementById('mover-performance-chart')) {
        Charts.loadMoverPerformanceChart('mover-performance-chart');
    }
    if (document.getElementById('watchlist-performance-chart')) {
        Charts.loadWatchlistPerformanceChart('watchlist-performance-chart');
    }
    if (document.getElementById('mover-scores-chart')) {
        Charts.loadMoverScoresChart('mover-scores-chart');
    }

    // Add event listeners for analysis button
    const analyzeBtn = document.getElementById('analyze-btn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', () => Analysis.startAnalysis());
    }
});
