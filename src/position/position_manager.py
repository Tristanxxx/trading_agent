"""
Position Management Module
Handles opening, closing, and tracking trading positions
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class PositionSide(Enum):
    LONG = "LONG"
    SHORT = "SHORT"


@dataclass
class Position:
    """Represents a trading position"""
    symbol: str
    side: PositionSide
    entry_price: float
    size: float
    entry_time: datetime
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    exit_price: Optional[float] = None
    exit_time: Optional[datetime] = None
    pnl: Optional[float] = None

    def calculate_pnl(self, current_price: float) -> float:
        """Calculate current PnL"""
        if self.side == PositionSide.LONG:
            return (current_price - self.entry_price) * self.size
        else:
            return (self.entry_price - current_price) * self.size

    def calculate_pnl_percentage(self, current_price: float) -> float:
        """Calculate current PnL as percentage"""
        if self.side == PositionSide.LONG:
            return ((current_price - self.entry_price) / self.entry_price) * 100
        else:
            return ((self.entry_price - current_price) / self.entry_price) * 100


class PositionManager:
    """Manages trading positions"""

    def __init__(self, initial_balance: float = 10000.0):
        """
        Initialize position manager

        Args:
            initial_balance: Starting balance in quote currency (e.g., USDT)
        """
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.current_position: Optional[Position] = None
        self.position_history: List[Position] = []
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0

    def has_open_position(self) -> bool:
        """Check if there's an open position"""
        return self.current_position is not None

    def open_position(
        self,
        symbol: str,
        side: PositionSide,
        entry_price: float,
        size: float,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None
    ) -> bool:
        """
        Open a new position

        Args:
            symbol: Trading pair symbol
            side: LONG or SHORT
            entry_price: Entry price
            size: Position size in base currency
            stop_loss: Optional stop loss price
            take_profit: Optional take profit price

        Returns:
            True if position opened successfully
        """
        if self.has_open_position():
            print("Cannot open position: already have an open position")
            return False

        cost = entry_price * size
        if cost > self.balance:
            print(f"Insufficient balance: need {cost}, have {self.balance}")
            return False

        self.current_position = Position(
            symbol=symbol,
            side=side,
            entry_price=entry_price,
            size=size,
            entry_time=datetime.now(),
            stop_loss=stop_loss,
            take_profit=take_profit
        )

        print(f"Opened {side.value} position: {size} @ {entry_price}")
        return True

    def close_position(self, exit_price: float, reason: str = "") -> Optional[Position]:
        """
        Close the current position

        Args:
            exit_price: Exit price
            reason: Reason for closing (for logging)

        Returns:
            Closed position or None
        """
        if not self.has_open_position():
            print("No open position to close")
            return None

        self.current_position.exit_price = exit_price
        self.current_position.exit_time = datetime.now()
        self.current_position.pnl = self.current_position.calculate_pnl(exit_price)

        self.balance += self.current_position.pnl
        self.total_trades += 1

        if self.current_position.pnl > 0:
            self.winning_trades += 1
        else:
            self.losing_trades += 1

        print(f"Closed {self.current_position.side.value} position @ {exit_price}")
        print(f"PnL: {self.current_position.pnl:.2f} ({self.current_position.calculate_pnl_percentage(exit_price):.2f}%)")
        if reason:
            print(f"Reason: {reason}")

        self.position_history.append(self.current_position)
        closed_position = self.current_position
        self.current_position = None

        return closed_position

    def check_stop_loss_take_profit(self, current_price: float) -> bool:
        """
        Check if stop loss or take profit has been hit

        Args:
            current_price: Current market price

        Returns:
            True if position was closed
        """
        if not self.has_open_position():
            return False

        pos = self.current_position

        if pos.side == PositionSide.LONG:
            if pos.stop_loss and current_price <= pos.stop_loss:
                self.close_position(current_price, "Stop loss hit")
                return True
            if pos.take_profit and current_price >= pos.take_profit:
                self.close_position(current_price, "Take profit hit")
                return True
        else:  # SHORT
            if pos.stop_loss and current_price >= pos.stop_loss:
                self.close_position(current_price, "Stop loss hit")
                return True
            if pos.take_profit and current_price <= pos.take_profit:
                self.close_position(current_price, "Take profit hit")
                return True

        return False

    def get_current_pnl(self, current_price: float) -> Optional[float]:
        """Get current PnL for open position"""
        if not self.has_open_position():
            return None
        return self.current_position.calculate_pnl(current_price)

    def get_statistics(self) -> dict:
        """Get trading statistics"""
        win_rate = (self.winning_trades / self.total_trades * 100) if self.total_trades > 0 else 0
        total_pnl = self.balance - self.initial_balance
        return_pct = (total_pnl / self.initial_balance) * 100

        return {
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'return_percentage': return_pct,
            'current_balance': self.balance
        }
