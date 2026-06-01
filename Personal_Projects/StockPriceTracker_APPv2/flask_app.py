"""
Flask Web Application for Stock Analysis Dashboard
Displays results from StockPriceTracker_appv2.py analysis
"""

from flask import Flask, render_template, jsonify, request, session
import os
import sys
import json
from datetime import datetime
from functools import wraps
import threading
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the analysis functions from the main script
import StockPriceTracker_appv2 as analyzer

# Configure Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state for analysis results
analysis_state = {
    'is_running': False,
    'last_results': None,
    'last_run_time': None,
    'error': None
}


def run_analysis_background():
    """Run analysis in background and store results."""
    try:
        analysis_state['is_running'] = True
        analysis_state['error'] = None
        logger.info("Starting analysis...")
        
        # Execute the analysis pipeline
        mover_scores, ohlc_data = analyzer.step_1_scan_movers()
        top5_symbols = list(ohlc_data.keys())
        
        watchlist_performance, watchlist_ohlc_data = analyzer.step_2_fetch_watchlist(top5_symbols)
        score_df, wl_score_df = analyzer.analyze_and_score(
            top5_symbols, ohlc_data, watchlist_ohlc_data, watchlist_performance
        )
        
        # Store results
        analysis_state['last_results'] = {
            'mover_scores': mover_scores,
            'ohlc_data': {sym: df.to_dict() for sym, df in ohlc_data.items()},
            'top5_symbols': top5_symbols,
            'watchlist_performance': watchlist_performance,
            'watchlist_ohlc_data': {sym: df.to_dict() for sym, df in watchlist_ohlc_data.items()},
            'score_df': score_df.to_dict('records'),
            'wl_score_df': wl_score_df.to_dict('records'),
        }
        analysis_state['last_run_time'] = datetime.now().isoformat()
        logger.info("Analysis completed successfully")
        
    except Exception as e:
        analysis_state['error'] = str(e)
        logger.error(f"Analysis failed: {e}")
    finally:
        analysis_state['is_running'] = False


# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Dashboard home page."""
    return render_template('index.html',
                         last_run=analysis_state['last_run_time'],
                         has_results=analysis_state['last_results'] is not None)


@app.route('/api/status')
def api_status():
    """Get current analysis status."""
    return jsonify({
        'is_running': analysis_state['is_running'],
        'has_results': analysis_state['last_results'] is not None,
        'last_run': analysis_state['last_run_time'],
        'error': analysis_state['error']
    })


@app.route('/api/run-analysis', methods=['POST'])
def api_run_analysis():
    """Start analysis in background."""
    if analysis_state['is_running']:
        return jsonify({'error': 'Analysis already running'}), 409
    
    # Reset error state
    analysis_state['error'] = None
    
    # Run analysis in background thread
    thread = threading.Thread(target=run_analysis_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'Analysis started'})


@app.route('/api/results')
def api_results():
    """Get analysis results."""
    if analysis_state['last_results'] is None:
        return jsonify({'error': 'No results available. Run analysis first.'}), 404
    
    return jsonify(analysis_state['last_results'])


@app.route('/dashboard')
def dashboard():
    """Main dashboard with all analysis results."""
    if analysis_state['last_results'] is None:
        return render_template('dashboard.html', error='No results available')
    
    results = analysis_state['last_results']
    return render_template('dashboard.html',
                         movers=results['score_df'],
                         watchlist=results['wl_score_df'],
                         top5_symbols=results['top5_symbols'],
                         mover_scores=results['mover_scores'][:10],
                         last_run=analysis_state['last_run_time'])


@app.route('/movers')
def movers():
    """Display top 5 movers."""
    if analysis_state['last_results'] is None:
        return render_template('movers.html', error='No results available')
    
    results = analysis_state['last_results']
    return render_template('movers.html',
                         movers=results['score_df'],
                         ohlc_data=results['ohlc_data'],
                         top5_symbols=results['top5_symbols'])


@app.route('/watchlist')
def watchlist():
    """Display watchlist analysis."""
    if analysis_state['last_results'] is None:
        return render_template('watchlist.html', error='No results available')
    
    results = analysis_state['last_results']
    return render_template('watchlist.html',
                         watchlist=results['wl_score_df'],
                         watchlist_performance=results['watchlist_performance'],
                         watchlist_ohlc_data=results['watchlist_ohlc_data'])


@app.route('/recommendations')
def recommendations():
    """Display investment recommendations."""
    if analysis_state['last_results'] is None:
        return render_template('recommendations.html', error='No results available')
    
    results = analysis_state['last_results']
    score_df = results['score_df']
    wl_score_df = results['wl_score_df']
    
    # Get best performers
    best_mover = score_df[0] if score_df else None
    best_watchlist = wl_score_df[0] if wl_score_df else None
    
    return render_template('recommendations.html',
                         best_mover=best_mover,
                         best_watchlist=best_watchlist,
                         movers=score_df,
                         watchlist=wl_score_df)


@app.route('/api/chart-data/<chart_type>')
def api_chart_data(chart_type):
    """Get chart data for frontend visualization."""
    if analysis_state['last_results'] is None:
        return jsonify({'error': 'No data'}), 404
    
    results = analysis_state['last_results']
    
    if chart_type == 'mover-performance':
        # Return top movers with percentage changes
        return jsonify({
            'labels': [s for s, _ in results['mover_scores'][:5]],
            'data': [pct for _, pct in results['mover_scores'][:5]]
        })
    
    elif chart_type == 'watchlist-performance':
        # Return watchlist with percentage changes
        return jsonify({
            'labels': [s for s, _ in results['watchlist_performance']],
            'data': [pct for _, pct in results['watchlist_performance']]
        })
    
    elif chart_type == 'mover-scores':
        # Return investment scores for movers
        return jsonify({
            'labels': [m['Symbol'] for m in results['score_df']],
            'data': [m['Score'] for m in results['score_df']]
        })
    
    return jsonify({'error': 'Unknown chart type'}), 400


@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.route('/api/data')
def api_data():
    """Get data for tables and dashboard."""
    if analysis_state['last_results'] is None:
        return jsonify({'error': 'No results available'}), 404
    
    results = analysis_state['last_results']
    
    # Results already contain converted dicts from last_results storage
    movers_data = results.get('score_df', [])
    watchlist_data = results.get('wl_score_df', [])
    
    return jsonify({
        'top_movers': movers_data,
        'watchlist': watchlist_data
    })


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    # Return JSON for API routes, HTML for page routes
    if request.path.startswith('/api'):
        return jsonify({'error': 'Not found'}), 404
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    # Return JSON for API routes, HTML for page routes
    if request.path.startswith('/api'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('error.html', error='Internal server error'), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print(" 🌐 Stock Analysis Flask Dashboard")
    print("=" * 80)
    print("\n  Starting Flask app on http://localhost:5000")
    print("  Press Ctrl+C to stop\n")
    
    app.run(debug=True, port=5000, use_reloader=True)
