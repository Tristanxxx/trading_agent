"""
Trading Agent Module
Makes trading decisions based on market data
"""
from enum import Enum
from typing import Dict, Optional, List
import pandas as pd
import numpy as np


class Signal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class TradingAgent:
    """
    Trading agent that makes decisions based on market data
    Uses a simple moving average crossover strategy as a baseline
    """

    def __init__(
        self,
        fast_period: int = 9,
        slow_period: int = 21,
        rsi_period: int = 14,
        rsi_oversold: float = 30,
        rsi_overbought: float = 70
    ):
        """
        Initialize trading agent with strategy parameters

        Args:
            fast_period: Fast moving average period
            slow_period: Slow moving average period
            rsi_period: RSI calculation period
            rsi_oversold: RSI oversold threshold
            rsi_overbought: RSI overbought threshold
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.price_history: List[float] = []

    def calculate_sma(self, prices: List[float], period: int) -> Optional[float]:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period

    def calculate_rsi(self, prices: List[float], period: int = 14) -> Optional[float]:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return None

        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas[-period:]]
        losses = [-d if d < 0 else 0 for d in deltas[-period:]]

        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def update_price_history(self, candle: Dict):
        """Update price history with new candle data"""
        self.price_history.append(candle['close'])

        # Keep only what we need (slow_period + rsi_period + buffer)
        max_history = max(self.slow_period, self.rsi_period) + 50
        if len(self.price_history) > max_history:
            self.price_history = self.price_history[-max_history:]

    def analyze_market(self, candle: Dict, has_position: bool) -> Signal:
        """
        Analyze market and generate trading signal

        Args:
            candle: Latest candle data
            has_position: Whether we currently have an open position

        Returns:
            Trading signal (BUY, SELL, or HOLD)
        """
        self.update_price_history(candle)

        # Need enough history for indicators
        if len(self.price_history) < self.slow_period:
            return Signal.HOLD

        # Calculate indicators
        fast_sma = self.calculate_sma(self.price_history, self.fast_period)
        slow_sma = self.calculate_sma(self.price_history, self.slow_period)
        rsi = self.calculate_rsi(self.price_history, self.rsi_period)

        if fast_sma is None or slow_sma is None or rsi is None:
            return Signal.HOLD

        current_price = candle['close']

        # Buy signal: fast MA crosses above slow MA and RSI not overbought
        if not has_position:
            if fast_sma > slow_sma and rsi < self.rsi_overbought:
                # Check if this is a recent crossover (additional confirmation)
                if len(self.price_history) >= self.slow_period + 1:
                    prev_fast_sma = self.calculate_sma(
                        self.price_history[:-1],
                        self.fast_period
                    )
                    prev_slow_sma = self.calculate_sma(
                        self.price_history[:-1],
                        self.slow_period
                    )

                    if prev_fast_sma and prev_slow_sma:
                        if prev_fast_sma <= prev_slow_sma:
                            print(f"Buy signal: Fast SMA ({fast_sma:.2f}) crossed above Slow SMA ({slow_sma:.2f}), RSI: {rsi:.2f}")
                            return Signal.BUY

        # Sell signal: fast MA crosses below slow MA or RSI overbought
        if has_position:
            if fast_sma < slow_sma or rsi > self.rsi_overbought:
                print(f"Sell signal: Fast SMA ({fast_sma:.2f}) / Slow SMA ({slow_sma:.2f}), RSI: {rsi:.2f}")
                return Signal.SELL

        return Signal.HOLD

    def calculate_position_size(
        self,
        balance: float,
        current_price: float,
        risk_percentage: float = 0.02
    ) -> float:
        """
        Calculate position size based on available balance and risk

        Args:
            balance: Available balance
            current_price: Current price
            risk_percentage: Percentage of balance to risk (default 2%)

        Returns:
            Position size in base currency
        """
        risk_amount = balance * risk_percentage
        position_value = balance * 0.95  # Use 95% of balance max
        position_size = position_value / current_price
        return round(position_size, 6)

    def calculate_stop_loss_take_profit(
        self,
        entry_price: float,
        side: str,
        stop_loss_pct: float = 0.02,
        take_profit_pct: float = 0.04
    ) -> tuple:
        """
        Calculate stop loss and take profit levels

        Args:
            entry_price: Entry price
            side: Position side (LONG or SHORT)
            stop_loss_pct: Stop loss percentage (default 2%)
            take_profit_pct: Take profit percentage (default 4%)

        Returns:
            Tuple of (stop_loss, take_profit)
        """
        if side == "LONG":
            stop_loss = entry_price * (1 - stop_loss_pct)
            take_profit = entry_price * (1 + take_profit_pct)
        else:  # SHORT
            stop_loss = entry_price * (1 + stop_loss_pct)
            take_profit = entry_price * (1 - take_profit_pct)

        return stop_loss, take_profit

    def get_indicator_values(self) -> Dict:
        """Get current indicator values for display"""
        if len(self.price_history) < self.slow_period:
            return {}

        fast_sma = self.calculate_sma(self.price_history, self.fast_period)
        slow_sma = self.calculate_sma(self.price_history, self.slow_period)
        rsi = self.calculate_rsi(self.price_history, self.rsi_period)

        return {
            'fast_sma': fast_sma,
            'slow_sma': slow_sma,
            'rsi': rsi,
            'current_price': self.price_history[-1] if self.price_history else None
        }
