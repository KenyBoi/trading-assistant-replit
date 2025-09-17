"""Market scanner for trading signals"""
import yfinance as yf
import pandas as pd

class Scanner:
    def __init__(self, config):
        self.config = config
    
    def scan(self):
        """Scan for trading opportunities"""
        signals = []
        
        for symbol in self.config.watchlist:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='5d')
                
                if len(hist) >= 2:
                    # Calculate indicators
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2]
                    price_change = ((current_price - prev_price) / prev_price) * 100
                    
                    current_volume = hist['Volume'].iloc[-1]
                    avg_volume = hist['Volume'].mean()
                    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
                    
                    # Generate signals
                    signal = None
                    confidence = 0
                    
                    if price_change > 1 and volume_ratio > 1.5:
                        signal = 'BUY'
                        confidence = min(80, 50 + (price_change * 5) + (volume_ratio * 10))
                    elif price_change < -1 and volume_ratio > 1.5:
                        signal = 'SELL'
                        confidence = min(80, 50 + (abs(price_change) * 5) + (volume_ratio * 10))
                    
                    if signal:
                        signals.append({
                            'symbol': symbol,
                            'signal': signal,
                            'price': round(current_price, 2),
                            'change': round(price_change, 2),
                            'volume_ratio': round(volume_ratio, 2),
                            'confidence': round(confidence)
                        })
            except Exception as e:
                print(f"Error scanning {symbol}: {e}")
        
        # Sort by confidence
        signals.sort(key=lambda x: x['confidence'], reverse=True)
        return signals[:10]  # Top 10 signals