"""API routes"""
from flask import Blueprint, jsonify, request
from app.config import Config
from app.market_brief import MarketBrief
from app.scanner import Scanner

api_bp = Blueprint('api', __name__)

# Initialize components
config = Config()
market_brief = MarketBrief(config)
scanner = Scanner(config)

@api_bp.route('/brief')
def get_brief():
    """Get market brief"""
    return jsonify(market_brief.generate())

@api_bp.route('/scan')
def get_scan():
    """Run market scanner"""
    signals = scanner.scan()
    return jsonify({
        'signals': signals,
        'count': len(signals),
        'timestamp': datetime.now().isoformat()
    })

@api_bp.route('/status')
def get_status():
    """Get system status"""
    return jsonify({
        'status': 'online',
        'configured': config.is_configured(),
        'capital': config.capital,
        'watchlist': config.watchlist
    })

@api_bp.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint"""
    data = request.json
    action = data.get('action')
    
    if action == 'brief':
        return get_brief()
    elif action == 'scan':
        return get_scan()
    elif action == 'status':
        return get_status()
    else:
        return jsonify({'error': 'Unknown action'}), 400