import sys
import os
import random
import logging
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import backend modules
from backend.price_feed import get_prices
from backend.news_feed import fetch_news
from backend.whale_tracker import get_fake_whale_tx
from ai.summarize import summarize

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Whale Position Functions (from your whale_position.py)
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT", "BNBUSDT", "DOTUSDT", "MATICUSDT", "LINKUSDT"]

def get_simulated_open_positions(min_usd=10000, count=5):
    """Generate simulated open positions for whale tracking (optimized for dashboard)"""
    positions = []
    current_time = datetime.now()
    
    for i in range(count):
        # Generate random time within last 2 hours
        time_offset = random.randint(0, 7200)
        position_time = current_time - timedelta(seconds=time_offset)
        
        # Generate position amount with realistic distribution
        if random.random() < 0.1:
            amount = random.randint(min_usd * 10, min_usd * 50)
        elif random.random() < 0.3:
            amount = random.randint(min_usd * 3, min_usd * 10)
        else:
            amount = random.randint(min_usd, min_usd * 3)
        
        # Select symbol with weighted probability
        symbol_weights = {
            "BTCUSDT": 0.3, "ETHUSDT": 0.25, "SOLUSDT": 0.15, "ADAUSDT": 0.1,
            "BNBUSDT": 0.08, "DOTUSDT": 0.05, "MATICUSDT": 0.04, "LINKUSDT": 0.03
        }
        
        symbol = random.choices(
            list(symbol_weights.keys()),
            weights=list(symbol_weights.values())
        )[0]
        
        # Generate side with slight bias towards LONG
        side = random.choices(["LONG", "SHORT"], weights=[0.55, 0.45])[0]
        
        # Generate entry price
        base_prices = {
            "BTCUSDT": 104000, "ETHUSDT": 2500, "SOLUSDT": 145, "ADAUSDT": 1.2,
            "BNBUSDT": 690, "DOTUSDT": 7.8, "MATICUSDT": 0.85, "LINKUSDT": 15.5
        }
        
        base_price = base_prices.get(symbol, 100)
        price_variation = random.uniform(-0.05, 0.05)
        entry_price = base_price * (1 + price_variation)
        
        # Calculate position size
        position_size = amount / entry_price
        
        # Generate leverage
        leverage = random.choice([1, 2, 3, 5, 10, 20, 25, 50])
        
        # Generate PnL
        pnl_percentage = random.uniform(-0.15, 0.25)
        unrealized_pnl = amount * pnl_percentage
        
        # Generate margin used
        margin_used = amount / leverage
        
        # Generate current price based on PnL
        if side == "LONG":
            current_price = entry_price * (1 + (unrealized_pnl / amount))
        else:
            current_price = entry_price * (1 - (unrealized_pnl / amount))
        
        # Generate liquidation price
        if side == "LONG":
            liquidation_price = entry_price * (1 - (0.8 / leverage))
        else:
            liquidation_price = entry_price * (1 + (0.8 / leverage))
        
        positions.append({
            "Time": position_time.strftime("%H:%M:%S"),
            "Symbol": symbol.replace("USDT", ""),
            "Side": side,
            "Amount (USD)": f"${amount:,}",
            "Size": f"{position_size:.4f}",
            "Entry Price": f"${entry_price:,.2f}",
            "Current Price": f"${current_price:,.2f}",
            "Leverage": f"{leverage}x",
            "Margin": f"${margin_used:,.0f}",
            "PnL": f"${unrealized_pnl:,.0f}",
            "PnL %": f"{pnl_percentage * 100:+.1f}%",
            "Liq. Price": f"${liquidation_price:,.2f}",
            "Exchange": random.choice(["Binance", "Bybit", "OKX", "Bitget"])
        })
    
    return positions

def format_currency(value):
    """Format currency with proper thousand separators"""
    try:
        if isinstance(value, (int, float)):
            return f"${value:,.2f}"
        return value
    except Exception as e:
        logger.error(f"Error formatting currency: {e}")
        return value

def format_percentage(value):
    """Format percentage with proper sign"""
    try:
        if isinstance(value, (int, float)):
            return f"+{value}%" if value > 0 else f"{value}%"
        return value
    except Exception as e:
        logger.error(f"Error formatting percentage: {e}")
        return value

def get_market_data():
    """Get comprehensive market data"""
    try:
        return {
            'total_market_cap': '$2.45T',
            'volume_24h': '$98.2B',
            'btc_dominance': '52.3%',
            'fear_greed_index': 65
        }
    except Exception as e:
        logger.error(f"Error getting market data: {e}")
        return {}

def clean_html(html_text):
    """Remove HTML tags from text"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_text)

def style_whale_positions_dataframe():
    """Apply custom styling to whale positions dataframe"""
    return """
    <style>
    .whale-positions table {
        font-size: 12px;
    }
    .whale-positions .positive {
        color: #00ff88;
        font-weight: bold;
    }
    .whale-positions .negative {
        color: #ff4444;
        font-weight: bold;
    }
    .whale-positions .long {
        background-color: rgba(0, 255, 136, 0.1);
    }
    .whale-positions .short {
        background-color: rgba(255, 68, 68, 0.1);
    }
    
    /* Fix column alignment and spacing */
    [data-testid="stDataFrame"] {
        width: 100%;
    }
    
    [data-testid="stDataFrame"] > div {
        width: 100%;
        overflow-x: auto;
    }
    
    /* Ensure consistent heights */
    .stContainer {
        height: 100%;
    }
    
    /* Summary box styling */
    .summary-container {
        background-color: rgba(28, 131, 225, 0.1);
        border-radius: 10px;
        padding: 1rem;
        height: 350px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    </style>
    """

def run_dashboard():
    """Main dashboard function"""
    try:
        # Configure page
        st.set_page_config(
            page_title="Bloomberg Crypto Lokal",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Auto-refresh
        st_autorefresh(interval=30000, key="datarefresh")

        # Title and description
        st.title("📈 Bloomberg Crypto Lokal")
        st.markdown("Pantauan pasar crypto dan transaksi besar secara real-time")

        # Market metrics
        col1, col2, col3, col4 = st.columns(4)
        
        prices = get_prices()
        market_data = get_market_data()

        with col1:
            btc_price = prices.get('bitcoin', {}).get('usd', 0)
            st.metric("Bitcoin (BTC)", format_currency(btc_price), "+2.4%")

        with col2:
            eth_price = prices.get('ethereum', {}).get('usd', 0)
            st.metric("Ethereum (ETH)", format_currency(eth_price), "-0.8%")

        with col3:
            st.metric("Total Market Cap", market_data.get('total_market_cap', 'N/A'))

        with col4:
            st.metric("24h Volume", market_data.get('volume_24h', 'N/A'))

        # Whale Transactions
        st.subheader("🐋 Whale Transactions")
        if "whale_tx" not in st.session_state:
            st.session_state["whale_tx"] = []

        tx = get_fake_whale_tx()
        if tx:
            st.session_state["whale_tx"].append(tx)
            # Keep only last 10 transactions
            if len(st.session_state["whale_tx"]) > 10:
                st.session_state["whale_tx"] = st.session_state["whale_tx"][-10:]
            
            tx_df = pd.DataFrame(st.session_state["whale_tx"])
            st.dataframe(tx_df, use_container_width=True)

        # Whale Positions (New Section)
        st.subheader("💼 Whale Open Positions")
        
        # Initialize whale positions in session state
        if "whale_positions" not in st.session_state:
            st.session_state["whale_positions"] = []
        
        # Generate new whale positions periodically
        if len(st.session_state["whale_positions"]) == 0 or random.random() < 0.3:
            new_positions = get_simulated_open_positions(min_usd=50000, count=8)
            st.session_state["whale_positions"] = new_positions
        
        # Display whale positions
        if st.session_state["whale_positions"]:
            positions_df = pd.DataFrame(st.session_state["whale_positions"])
            
            # Add custom styling
            st.markdown(style_whale_positions_dataframe(), unsafe_allow_html=True)
            
            # Create columns with better proportions
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Display the main dataframe with fixed height
                st.dataframe(
                    positions_df,
                    use_container_width=True,
                    height=350
                )
            
            with col2:
                # Create a container with consistent spacing
                with st.container():
                    st.markdown("### 📊 Position Summary")
                    
                    # Calculate summary stats
                    total_positions = len(positions_df)
                    long_positions = len(positions_df[positions_df['Side'] == 'LONG'])
                    short_positions = len(positions_df[positions_df['Side'] == 'SHORT'])
                    
                    # Extract numeric values for calculations
                    amounts = []
                    pnl_values = []
                    for _, row in positions_df.iterrows():
                        # Clean amount string
                        amount_str = row['Amount (USD)'].replace('$', '').replace(',', '')
                        amounts.append(float(amount_str))
                        
                        # Clean PnL string
                        pnl_str = row['PnL'].replace('$', '').replace(',', '')
                        pnl_values.append(float(pnl_str))
                    
                    total_value = sum(amounts)
                    total_pnl = sum(pnl_values)
                    
                    # Display metrics with consistent spacing
                    st.metric("Total Positions", total_positions)
                    st.metric("Long/Short", f"{long_positions}/{short_positions}")
                    st.metric("Total Value", f"${total_value:,.0f}")
                    
                    # PnL metric with color indication
                    pnl_delta = f"{(total_pnl/total_value)*100:+.1f}%" if total_value > 0 else "0%"
                    st.metric(
                        "Total PnL", 
                        f"${total_pnl:,.0f}",
                        pnl_delta
                    )
                    
                    # Add some spacing
                    st.markdown("---")
                    
                    # Refresh button with better styling
                    if st.button("🔄 Refresh Positions", 
                                key="refresh_positions", 
                                use_container_width=True):
                        st.session_state["whale_positions"] = get_simulated_open_positions(min_usd=50000, count=8)
                        st.rerun()

        # News Section with improved formatting
        st.subheader("📰 Berita Crypto Terbaru")
        news = fetch_news()
        
        for item in news:
            with st.expander(item['title']):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Clean and display the summary
                    clean_summary = clean_html(item['summary'])
                    st.markdown(clean_summary)
                    
                with col2:
                    # Add a nice looking "Read More" button
                    st.markdown(
                        f"""
                        <div style='text-align: right; padding: 10px;'>
                        <a href='{item["link"]}' target='_blank'>
                            <button style='
                                background-color: #4CAF50;
                                border: none;
                                color: white;
                                padding: 10px 20px;
                                text-align: center;
                                text-decoration: none;
                                display: inline-block;
                                font-size: 14px;
                                margin: 4px 2px;
                                cursor: pointer;
                                border-radius: 4px;
                            '>
                            🔗 Baca Selengkapnya
                            </button>
                        </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                # Add separator between news items
                st.markdown("---")

    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        st.error("An error occurred while loading the dashboard")

if __name__ == "__main__":
    run_dashboard()