#!/usr/bin/env python3
"""Trading Assistant - Main Entry Point"""

import os
import sys
import threading
from flask import Flask
from app.config import Config
from app.dashboard import create_dashboard
from api.routes import api_bp

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')

# Load configuration
config = Config()

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Trading Assistant</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                h1 { text-align: center; }
                .container {
                    background: rgba(255,255,255,0.1);
                    border-radius: 10px;
                    padding: 30px;
                    backdrop-filter: blur(10px);
                }
                .button {
                    display: inline-block;
                    padding: 12px 24px;
                    margin: 10px;
                    background: white;
                    color: #667eea;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                }
                .endpoints {
                    background: rgba(0,0,0,0.2);
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }
                code {
                    background: rgba(0,0,0,0.3);
                    padding: 2px 6px;
                    border-radius: 3px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Trading Assistant Bot</h1>
                <p style="text-align: center;">AI-Powered Market Analysis & Trading Signals</p>
                
                <div style="text-align: center;">
                    <a href="/dashboard" class="button">📊 Open Dashboard</a>
                    <a href="/api/brief" class="button">📈 Market Brief</a>
                    <a href="/api/scan" class="button">🔍 Scanner</a>
                </div>
                
                <div class="endpoints">
                    <h3>API Endpoints:</h3>
                    <ul>
                        <li><code>GET /api/brief</code> - Get market brief</li>
                        <li><code>GET /api/scan</code> - Run market scanner</li>
                        <li><code>GET /api/status</code> - System status</li>
                        <li><code>POST /api/webhook</code> - Webhook for automation</li>
                    </ul>
                </div>
                
                <p style="text-align: center; opacity: 0.8;">
                    Status: <span style="color: #4ade80;">● Running</span> | 
                    Version: 1.0.0 | 
                    <a href="https://github.com/yourusername/trading-assistant-replit" style="color: white;">GitHub</a>
                </p>
            </div>
        </body>
    </html>
    """

@app.route('/dashboard')
def dashboard():
    return """
    <html>
        <head>
            <meta http-equiv="refresh" content="0; url=/streamlit">
            <script>window.location.href = '/streamlit';</script>
        </head>
        <body>
            <p>Redirecting to dashboard...</p>
        </body>
    </html>
    """

def run_flask():
    """Run Flask server"""
    app.run(host='0.0.0.0', port=5000, debug=False)

def run_streamlit():
    """Run Streamlit dashboard"""
    os.system('streamlit run app/dashboard.py --server.port=8501 --server.headless=true')

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════╗
║          TRADING ASSISTANT BOT - STARTING UP           ║
╚════════════════════════════════════════════════════════╝

🚀 Initializing services...
📡 API Server: http://0.0.0.0:5000
📊 Dashboard: http://0.0.0.0:8501

Ready for trading! 📈
    """)
    
    # Start Flask in a thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Run Streamlit in main thread
    run_streamlit()