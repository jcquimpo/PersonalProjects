// Global chart instances
let topMoversChart = null;
let watchlistChart = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    if (!stockData) {
        console.error('No stock data available');
        return;
    }

    // Set up tab switching
    setupTabs();

    // Set up symbol button listeners
    setupSymbolButtons();

    // Initialize charts and tables for both sections
    updateTopMoversDisplay(stockData.topMovers.symbols[0]);
    updateWatchlistDisplay(stockData.watchlist.symbols[0]);

    // Set up refresh button
    setupRefreshButton();

    // Format timestamp
    if (document.getElementById('timestamp')) {
        const date = new Date(stockData.timestamp);
        document.getElementById('timestamp').textContent = date.toLocaleString();
    }
});

/**
 * Set up tab switching functionality
 */
function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.dataset.tab;

            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Add active class to clicked button and corresponding pane
            this.classList.add('active');
            document.getElementById(tabName).classList.add('active');

            // Redraw charts when switching tabs
            setTimeout(() => {
                if (tabName === 'top-movers' && topMoversChart) {
                    topMoversChart.resize();
                } else if (tabName === 'watchlist' && watchlistChart) {
                    watchlistChart.resize();
                }
            }, 100);
        });
    });
}

/**
 * Set up symbol button listeners
 */
function setupSymbolButtons() {
    const symbolButtons = document.querySelectorAll('.symbol-btn');

    symbolButtons.forEach(button => {
        button.addEventListener('click', function() {
            const symbol = this.dataset.symbol;
            const section = this.dataset.section;

            // Update active button within the same section
            const sectionButtons = document.querySelectorAll(
                `.symbol-btn[data-section="${section}"]`
            );
            sectionButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Update display
            if (section === 'top-movers') {
                updateTopMoversDisplay(symbol);
            } else if (section === 'watchlist') {
                updateWatchlistDisplay(symbol);
            }
        });
    });
}

/**
 * Update Top Movers chart and table for selected symbol
 */
function updateTopMoversDisplay(symbol) {
    const ohlcData = stockData.topMovers.ohlc[symbol];
    if (!ohlcData) {
        console.error(`No OHLC data for ${symbol}`);
        return;
    }

    // Update chart
    updateChart('topMoversChart', symbol, ohlcData);

    // Update table
    updateTable('topMoversTable', symbol, ohlcData);
}

/**
 * Update Watchlist chart and table for selected symbol
 */
function updateWatchlistDisplay(symbol) {
    const ohlcData = stockData.watchlist.ohlc[symbol];
    if (!ohlcData) {
        console.error(`No OHLC data for ${symbol}`);
        return;
    }

    // Update chart
    updateChart('watchlistChart', symbol, ohlcData);

    // Update table
    updateTable('watchlistTable', symbol, ohlcData);

    // Update statistics
    updatePriceStats(symbol, ohlcData);
}

/**
 * Update chart with OHLC data
 */
function updateChart(canvasId, symbol, ohlcData) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const companyName = stockData.symbolNames[symbol] || symbol;

    const chartData = {
        labels: ohlcData.dates.map(date => {
            const d = new Date(date + 'T00:00:00');
            return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        }),
        datasets: [
            {
                label: 'Open',
                data: ohlcData.opens,
                borderColor: '#60a5fa',
                backgroundColor: 'rgba(96, 165, 250, 0.1)',
                tension: 0.3,
                fill: false,
                pointRadius: 4,
                pointHoverRadius: 6,
                borderWidth: 2,
            },
            {
                label: 'High',
                data: ohlcData.highs,
                borderColor: '#22c55e',
                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                tension: 0.3,
                fill: false,
                pointRadius: 4,
                pointHoverRadius: 6,
                borderWidth: 2,
            },
            {
                label: 'Low',
                data: ohlcData.lows,
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                tension: 0.3,
                fill: false,
                pointRadius: 4,
                pointHoverRadius: 6,
                borderWidth: 2,
            },
            {
                label: 'Close',
                data: ohlcData.closes,
                borderColor: '#f59e0b',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                tension: 0.3,
                fill: false,
                pointRadius: 4,
                pointHoverRadius: 6,
                borderWidth: 3,
            },
        ],
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                labels: {
                    color: '#cbd5e1',
                    padding: 15,
                    font: {
                        size: 12,
                        weight: 'bold',
                    },
                },
            },
            title: {
                display: true,
                text: `${symbol} - ${companyName}`,
                color: '#60a5fa',
                font: {
                    size: 16,
                    weight: 'bold',
                },
            },
        },
        scales: {
            y: {
                ticks: {
                    color: '#94a3b8',
                    callback: function(value) {
                        return '$' + value.toFixed(2);
                    },
                },
                grid: {
                    color: 'rgba(148, 163, 184, 0.1)',
                },
            },
            x: {
                ticks: {
                    color: '#94a3b8',
                },
                grid: {
                    color: 'rgba(148, 163, 184, 0.1)',
                },
            },
        },
    };

    // Destroy existing chart if it exists
    const chartId = canvasId === 'topMoversChart' ? 'topMovers' : 'watchlist';
    if (chartId === 'topMovers' && topMoversChart) {
        topMoversChart.destroy();
    } else if (chartId === 'watchlist' && watchlistChart) {
        watchlistChart.destroy();
    }

    // Create new chart
    const newChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: chartOptions,
    });

    // Store reference
    if (chartId === 'topMovers') {
        topMoversChart = newChart;
    } else {
        watchlistChart = newChart;
    }
}

/**
 * Update price table with OHLC data
 */
function updateTable(tableId, symbol, ohlcData) {
    const tbody = document.querySelector(`#${tableId} tbody`);
    tbody.innerHTML = '';

    ohlcData.dates.forEach((date, index) => {
        const row = document.createElement('tr');

        const dateObj = new Date(date + 'T00:00:00');
        const dateStr = dateObj.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
        });

        row.innerHTML = `
            <td>${dateStr}</td>
            <td>$${parseFloat(ohlcData.opens[index]).toFixed(2)}</td>
            <td class="high">$${parseFloat(ohlcData.highs[index]).toFixed(2)}</td>
            <td class="low">$${parseFloat(ohlcData.lows[index]).toFixed(2)}</td>
            <td class="close">$${parseFloat(ohlcData.closes[index]).toFixed(2)}</td>
        `;

        tbody.appendChild(row);
    });
}

/**
 * Update price statistics for watchlist
 */
function updatePriceStats(symbol, ohlcData) {
    const closes = ohlcData.closes;
    const highs = ohlcData.highs;
    const lows = ohlcData.lows;

    const current = closes[closes.length - 1];
    const high = Math.max(...highs);
    const low = Math.min(...lows);
    const avg = closes.reduce((a, b) => a + b, 0) / closes.length;

    document.getElementById('currentValue').textContent = `$${current.toFixed(2)}`;
    document.getElementById('highValue').textContent = `$${high.toFixed(2)}`;
    document.getElementById('lowValue').textContent = `$${low.toFixed(2)}`;
    document.getElementById('avgValue').textContent = `$${avg.toFixed(2)}`;
}

/**
 * Set up refresh button
 */
function setupRefreshButton() {
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', async function() {
            const originalText = this.textContent;
            this.textContent = '⏳ Refreshing...';
            this.disabled = true;

            try {
                const response = await fetch('/api/refresh');
                const data = await response.json();

                if (response.ok) {
                    this.textContent = '✓ Refreshed!';
                    // Update timestamp
                    const date = new Date(data.timestamp);
                    document.getElementById('timestamp').textContent = date.toLocaleString();

                    // Reset button after 2 seconds
                    setTimeout(() => {
                        this.textContent = originalText;
                        this.disabled = false;
                    }, 2000);
                } else {
                    this.textContent = '✗ Error';
                    setTimeout(() => {
                        this.textContent = originalText;
                        this.disabled = false;
                    }, 2000);
                }
            } catch (error) {
                console.error('Refresh error:', error);
                this.textContent = '✗ Error';
                setTimeout(() => {
                    this.textContent = originalText;
                    this.disabled = false;
                }, 2000);
            }
        });
    }
}

/**
 * Format currency
 */
function formatCurrency(value) {
    return `$${parseFloat(value).toFixed(2)}`;
}
