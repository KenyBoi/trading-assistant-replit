"""Configuration management"""
import os
import pytz

class Config:
    def __init__(self):
        # API Keys from environment/secrets
        self.openai_api_key = os.environ.get('OPENAI_API_KEY', '')
        
        # Trading settings
        self.capital = float(os.environ.get('CAPITAL', '25000'))
        self.risk_per_trade = float(os.environ.get('RISK_PER_TRADE', '0.01'))
        
        # System settings
        self.timezone = pytz.timezone('US/Eastern')
        
        # Default watchlist
        self.watchlist = [
            'SPY', 'QQQ', 'AAPL', 'MSFT', 'TSLA', 
            'NVDA', 'AMD', 'META', 'GOOGL', 'AMZN'
        ]
        
    def is_configured(self):
        """Check if system is properly configured"""
        return bool(self.openai_api_key)