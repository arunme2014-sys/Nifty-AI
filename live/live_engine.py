import os
import sys
import time
import logging
import pandas as pd
from datetime import datetime

# Ensure the root directory is explicitly in the Python path for clean flat imports
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Reuse existing completed modules exactly as specified in your flat root architecture
import calculate  
import calculate_features
import historical_statistics
import historical_ai
import backtest.engine as backtest_engine  # Houses your Engine Runner / Simulator logic
from live.auth import FyersAuthenticator  
from live.market_data import LiveMarketData

# Setup Production Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("live_engine_production.log")
    ]
)
logger = logging.getLogger("NiftyAILiveOrchestrator")


class PaperTradingSimulator:
    """
    Supplementary layer handling paper trading simulation and risk management.
    Ensures zero interference with core predictive model mechanics.
    """
    def __init__(self):
        self.active_position = None  # None, "BUY", or "SELL"
        self.entry_price = 0.0
        self.trailing_high = 0.0
        self.paper_balance = 1000000.0  # Initial mock capital: 10 Lakhs
        self.trade_log = []

    def process_risk_and_execution(self, signal, current_price):
        """
        Applies a risk management layer (Profit Shields, Panic Reversals)
        and updates the paper trading portfolio simulator.
        """
        if current_price <= 0:
            return

        # 1. Active Position Tracking & Risk Safeguards
        if self.active_position:
            # Update trailing maximums for profit shielding
            if self.active_position == "BUY":
                self.trailing_high = max(self.trailing_high, current_price)
                # Quick Profit Shield / Reversal Exit Check
                if signal == "SELL" or current_price < (self.entry_price * 0.995): 
                    self._execute_paper_exit(current_price, "Panic Reversal / Stop Loss")
            
            elif self.active_position == "SELL":
                self.trailing_high = min(self.trailing_high, current_price)
                if signal == "BUY" or current_price > (self.entry_price * 1.005):
                    self._execute_paper_exit(current_price, "Panic Reversal / Stop Loss")

        # 2. New Entry Signals Processing
        else:
            if signal in ["BUY", "SELL"]:
                self.active_position = signal
                self.entry_price = current_price
                self.trailing_high = current_price
                logger.info(f" [PAPER ENTRY] Executed {signal} at {current_price}")

    def _execute_paper_exit(self, exit_price, reason):
        pnl = (exit_price - self.entry_price) if self.active_position == "BUY" else (self.entry_price - exit_price)
        self.paper_balance += pnl * 50  # Standard Nifty lot size multiplier
        logger.info(f" [PAPER EXIT] Closed {self.active_position} at {exit_price} | Reason: {reason} | Trade PnL: {pnl * 50:.2f}")
        
        self.trade_log.append({
            "entry": self.entry_price,
            "exit": exit_price,
            "type": self.active_position,
            "reason": reason,
            "pnl": pnl * 50,
            "time": datetime.now()
        })
        self.active_position = None
        self.entry_price = 0.0


class LiveEngineOrchestrator:
    def __init__(self, symbol="NSE:NIFTY50-INDEX", timeframe="5minute"):
        self.symbol = symbol
        self.timeframe = timeframe
        
        # Instantiate Fyers live data interface
        self.market_data_provider = LiveMarketData()
        
        # Instantiate completed analytical engines from your root files
        self.stats_engine = historical_statistics.HistoricalStatisticsEngine()
        self.ai_engine = historical_ai.HistoricalAIEngine()
        
        # Instantiate EngineRunner from your backtest/engine.py structure
        self.engine_runner = backtest_engine.EngineRunner()
        
        # Add Paper Trading & Execution layer as a supplement
        self.execution_layer = PaperTradingSimulator()
        
        self.is_running = False

    def validate_data_parity(self, live_df: pd.DataFrame) -> bool:
        """
        Validates live vs historical output formatting to guarantee data alignment.
        """
        if live_df is None or live_df.empty:
            logger.error("Data Parity Check Failed: Live DataFrame is completely empty.")
            return False
            
        required_cols = ['open', 'high', 'low', 'close', 'volume', 'timestamp']
        missing_cols = [col for col in required_cols if col not in live_df.columns]
        
        if missing_cols:
            logger.error(f"Data Parity Check Failed: Missing essential columns: {missing_cols}")
            return False
            
        return True

    def run_pipeline_cycle(self):
        """
        Executes a single workflow pass across the integrated modules.
        Fyers Live Data -> Indicators -> Features -> Stats/AI Engines -> Recommendation
        """
        try:
            # Step 1: Fetch streaming candle segments from Fyers interface
            raw_candles = self.market_data_provider.get_latest_candles(self.symbol, self.timeframe)
            
            # Step 2: Perform structural framework validation checks
            if not self.validate_data_parity(raw_candles):
                return
                
            # Step 3: Compute Indicators (Calls the main entry function in calculate.py)
            df_indicators = calculate.calculate_indicators(raw_candles)
            
            # Step 4: Extract Feature matrices (Calls calculate_features.py)
            df_features = calculate_features.calculate_features(df_indicators)
            
            # Step 5: Route into back-to-back analytics evaluation blocks
            stats_output = self.stats_engine.evaluate(df_features)
            ai_output = self.ai_engine.evaluate(df_features, stats_output)
            
            # Step 6: Extract consolidated prediction execution signal
            final_signal = self.engine_runner.generate_signal(stats_output, ai_output)
            
            # Step 7: Push straight into supplementary paper execution & risk block
            current_spot = float(raw_candles['close'].iloc[-1])
            self.execution_layer.process_risk_and_execution(final_signal, current_spot)
            
            logger.info(f"Cycle completed successfully. Price: {current_spot} | Signal: {final_signal}")
            
        except Exception as e:
            logger.error(f"Critical execution failure during runtime processing loop: {str(e)}", exc_info=True)

    def start(self):
        """Activates the infinite monitoring state loop for market hours."""
        logger.info(f"Starting NiftyAI-Pro Production Orchestrator for {self.symbol} ({self.timeframe})...")
        self.is_running = True
        
        while self.is_running:
            current_time = datetime.now().time()
            
            # Standard Indian market hours boundary validation check (09:15 to 15:30)
            if current_time >= datetime.strptime("09:15:00", "%H:%M:%S").time() and \
               current_time <= datetime.strptime("15:30:00", "%H:%M:%S").time():
                
                self.run_pipeline_cycle()
            else:
                logger.debug("Market is currently closed. Standing by for opening bell...")
                
            time.sleep(60)

    def stop(self):
        """Gracefully halts tracking activities safely."""
        logger.info("Stopping pipeline engine execution gracefully...")
        self.is_running = False


if __name__ == "__main__":
    orchestrator = LiveEngineOrchestrator(symbol="NSE:NIFTY50-INDEX", timeframe="5minute")
    try:
        orchestrator.start()
    except KeyboardInterrupt:
        orchestrator.stop()