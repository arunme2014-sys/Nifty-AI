"""
NIFTY AI PRO
Sprint 14

Backtest Models
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BacktestTrade:

    trade_date: datetime

    current_price: float

    recommendation: str

    confidence: str

    market_context: str

    trade_grade: str

    entry: float

    stop_loss: float

    target1: float

    target2: float

    result: str = "PENDING"

    exit_price: Optional[float] = None

    pnl_points: float = 0.0

    risk_reward: float = 0.0

    holding_days: int = 0


@dataclass
class BacktestSummary:

    total_trades: int = 0

    buy_trades: int = 0

    sell_trades: int = 0

    wait_trades: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    win_rate: float = 0.0

    average_rr: float = 0.0

    average_profit: float = 0.0

    average_loss: float = 0.0

    profit_factor: float = 0.0

    expectancy: float = 0.0

    max_drawdown: float = 0.0


@dataclass
class WalkForwardResult:

    trade: BacktestTrade

    summary: Optional[BacktestSummary] = None