"""Market brief generator"""
import yfinance as yf
from datetime import datetime

class MarketBrief:
    def __init__(self, config):
        self.config = config
    
    def generate(self):
        """Generate market brief"""
        timestamp = datetime.now(self.config.timezone)
        
        brief = {
            'timestamp': timestamp.isoformat(),
            'indices': {},
            'watchlist': [],
            'summary': ''
        }
        
        # Get indices data
        indices = {'SPY': 'S&P 500', 'QQQ': 'NASDAQ', 'DIA': 'DOW'}
        for symbol, name in indices.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='1d')
                if len(hist) > 0:
                    price = hist['Close'].iloc[-1]
                    change = ((hist['Close'].iloc[-1] - hist['Open'].iloc[0]) / hist['Open'].iloc[0]) * 100
                    brief['indices'][name] = {
                        'symbol': symbol,
                        'price': round(price, 2),
                        'change': round(change, 2),
                        'status': '🟢' if change > 0 else '🔴' if change < 0 else '⚪'
                    }
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
        
        # Get watchlist data
        for symbol in self.config.watchlist[:5]:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                price = info.get('regularMarketPrice', 0)
                prev_close = info.get('regularMarketPreviousClose', price)
                change = ((price - prev_close) / prev_close * 100) if prev_close else 0
                
                brief['watchlist'].append({
                    'symbol': symbol,
                    'price': round(price, 2),
                    'change': round(change, 2),
                    'volume': info.get('regularMarketVolume', 0)
                })
            except:
                pass
        
        # Generate summary
        market_trend = "BULLISH" if sum(1 for i in brief['indices'].values() if i['change'] > 0) >= 2 else "BEARISH"
        brief['summary'] = f"Market trend: {market_trend}"
        
        return brief