"""Streamlit dashboard"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf
from app.config import Config
from app.market_brief import MarketBrief
from app.scanner import Scanner

def create_dashboard():
    st.set_page_config(
        page_title="Trading Assistant",
        page_icon="📈",
        layout="wide"
    )
    
    # Initialize components
    config = Config()
    market_brief = MarketBrief(config)
    scanner = Scanner(config)
    
    # Header
    st.title("📈 Trading Assistant Dashboard")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        if config.is_configured():
            st.success("✅ AI Enabled")
        else:
            st.warning("⚠️ Add OPENAI_API_KEY in Secrets")
        
        st.metric("Capital", f"${config.capital:,.0f}")
        st.metric("Risk/Trade", f"{config.risk_per_trade*100:.1f}%")
        
        with st.expander("Watchlist"):
            for symbol in config.watchlist:
                st.write(f"• {symbol}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Scanner", "📈 Charts", "📰 News"])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        # Get market data
        brief_data = market_brief.generate()
        
        # Display indices
        for i, (name, data) in enumerate(brief_data['indices'].items()):
            col = [col1, col2, col3, col4][i % 4]
            with col:
                st.metric(
                    name,
                    f"${data['price']}",
                    f"{data['change']:+.2f}%"
                )
        
        # Market brief
        st.subheader("📊 Market Brief")
        st.info(brief_data['summary'])
        
        # Watchlist table
        if brief_data['watchlist']:
            st.subheader("📋 Watchlist")
            df = pd.DataFrame(brief_data['watchlist'])
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("🔍 Market Scanner")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            scan_type = st.selectbox(
                "Scan Type",
                ["All Signals", "Buy Only", "Sell Only"]
            )
            
            min_confidence = st.slider(
                "Min Confidence",
                0, 100, 50
            )
        
        if st.button("🔍 Run Scan", type="primary"):
            with st.spinner("Scanning..."):
                signals = scanner.scan()
                
                # Filter based on settings
                if scan_type == "Buy Only":
                    signals = [s for s in signals if s['signal'] == 'BUY']
                elif scan_type == "Sell Only":
                    signals = [s for s in signals if s['signal'] == 'SELL']
                
                signals = [s for s in signals if s['confidence'] >= min_confidence]
                
                if signals:
                    st.success(f"Found {len(signals)} signals!")
                    df = pd.DataFrame(signals)
                    
                    # Color code signals
                    def color_signal(val):
                        color = 'green' if val == 'BUY' else 'red'
                        return f'color: {color}'
                    
                    styled_df = df.style.applymap(
                        color_signal, 
                        subset=['signal']
                    )
                    
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No signals found matching criteria")
    
    with tab3:
        st.subheader("📈 Price Charts")
        
        selected = st.selectbox("Select Symbol", config.watchlist)
        period = st.select_slider(
            "Period",
            options=["1d", "5d", "1mo", "3mo", "6mo", "1y"],
            value="1mo"
        )
        
        if st.button("Load Chart", key="chart"):
            ticker = yf.Ticker(selected)
            hist = ticker.history(period=period)
            
            # Create candlestick chart
            fig = go.Figure(data=[go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name=selected
            )])
            
            fig.update_layout(
                title=f"{selected} - {period}",
                yaxis_title="Price ($)",
                xaxis_title="Date",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Volume chart
            st.bar_chart(hist['Volume'])
    
    with tab4:
        st.subheader("📰 Market News")
        st.info("News feed coming soon! Connect to news APIs for real-time updates.")

if __name__ == "__main__":
    create_dashboard()