from datetime import datetime

from backtest.models import BacktestTrade

trade = BacktestTrade(

    trade_date=datetime.now(),

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

print(trade)