# verify_parity.py
import sys
import os
import pandas as pd

# Add root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("🔄 Step 1: Initializing Live Market Data Connection...")
    from NiftyAI.live.market_data import LiveMarketData
    market_data = LiveMarketData()
    
    # Fetch a small sample of recent candles
    print("📥 Step 2: Fetching live sample candles from Fyers...")
    raw_df = market_data.get_latest_candles("NSE:NIFTY50-INDEX", "5minute")
    
    print("\n📊 --- LIVE DATA STREAM SNAPSHOT ---")
    print(f"Shape: {raw_df.shape}")
    print(f"Columns found: {list(raw_df.columns)}")
    print(raw_df.tail(2))
    print("------------------------------------\n")
    
    print("🧠 Step 3: Testing Pipeline Transmission...")
    from NiftyAI.indicators.calculate import calculate_indicators
    from NiftyAI.features.calculate_features import calculate_features
    
    df_ind = calculate_indicators(raw_df)
    df_feat = calculate_features(df_ind)
    print(f"✅ Success! Feature matrix generated with shape: {df_feat.shape}")
    print("Ready for live deployment.")

except Exception as e:
    print(f"❌ Alignment Gap Detected: {str(e)}")
    print("Review if column casing (e.g., 'Close' vs 'close') or timestamp formats differ from historical data structures.")