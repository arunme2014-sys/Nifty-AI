from backtest.simulator import TradeSimulator
from backtest.models import BacktestTrade
from datetime import datetime

trade = BacktestTrade(
    trade_date=datetime(2026, 6, 30),
    current_price=23865.75,
    recommendation="SELL",
    confidence="HIGH",
    market_context="RANGE",
    trade_grade="A",
    entry=23890,
    stop_loss=24060,
    target1=23820,
    target2=23660
)

simulator = TradeSimulator()

result = simulator.simulate(trade)

print(result)