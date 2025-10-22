"""
Main Trading Loop
Continuously feeds market data and executes trading decisions
"""
import time
from datetime import datetime
from typing import Optional

from src.data_feed import CryptoDataFeed
from src.agent import TradingAgent, Signal
from src.position import PositionManager, PositionSide


class TradingLoop:
    """Main trading loop that orchestrates the trading system"""

    def __init__(
        self,
        exchange: str = 'binance',
        symbol: str = 'BTC/USDT',
        initial_balance: float = 10000.0,
        check_interval: int = 60
    ):
        """
        Initialize trading loop

        Args:
            exchange: Exchange name (default: binance)
            symbol: Trading pair (default: BTC/USDT)
            initial_balance: Starting balance
            check_interval: Seconds between checks (default: 60 for 1-min candles)
        """
        self.data_feed = CryptoDataFeed(exchange, symbol)
        self.agent = TradingAgent()
        self.position_manager = PositionManager(initial_balance)
        self.check_interval = check_interval
        self.symbol = symbol
        self.running = False

    def initialize(self):
        """Initialize the system with historical data"""
        print("=" * 60)
        print("Initializing Trading System")
        print("=" * 60)
        print(f"Exchange: {self.data_feed.exchange_name}")
        print(f"Symbol: {self.symbol}")
        print(f"Initial Balance: {self.position_manager.initial_balance:.2f} USDT")
        print("=" * 60)

        # Fetch historical data to warm up indicators
        print("\nFetching historical data for indicator initialization...")
        historical_df = self.data_feed.fetch_historical_candles(limit=50)

        if not historical_df.empty:
            for _, row in historical_df.iterrows():
                candle = {
                    'timestamp': row['timestamp'],
                    'datetime': row['datetime'],
                    'open': row['open'],
                    'high': row['high'],
                    'low': row['low'],
                    'close': row['close'],
                    'volume': row['volume'],
                    'symbol': self.symbol
                }
                self.agent.update_price_history(candle)

            print(f"Loaded {len(historical_df)} historical candles")

            # Display initial indicator values
            indicators = self.agent.get_indicator_values()
            if indicators:
                print("\nInitial Indicator Values:")
                print(f"  Fast SMA: {indicators['fast_sma']:.2f}")
                print(f"  Slow SMA: {indicators['slow_sma']:.2f}")
                print(f"  RSI: {indicators['rsi']:.2f}")

        print("\nInitialization complete. Starting trading loop...")
        print("=" * 60)

    def process_candle(self, candle: dict):
        """Process a new candle"""
        current_price = candle['close']

        print(f"\n[{candle['datetime']}]")
        print(f"Price: {current_price:.2f} | Volume: {candle['volume']:.2f}")

        # Check stop loss / take profit first
        if self.position_manager.has_open_position():
            if self.position_manager.check_stop_loss_take_profit(current_price):
                return

            # Display current position PnL
            pnl = self.position_manager.get_current_pnl(current_price)
            pnl_pct = self.position_manager.current_position.calculate_pnl_percentage(current_price)
            print(f"Open Position PnL: {pnl:.2f} ({pnl_pct:.2f}%)")

        # Get trading signal from agent
        has_position = self.position_manager.has_open_position()
        signal = self.agent.analyze_market(candle, has_position)

        # Display indicators
        indicators = self.agent.get_indicator_values()
        if indicators:
            print(f"Indicators: Fast SMA: {indicators['fast_sma']:.2f} | "
                  f"Slow SMA: {indicators['slow_sma']:.2f} | "
                  f"RSI: {indicators['rsi']:.2f}")

        # Execute trading decisions
        if signal == Signal.BUY and not has_position:
            position_size = self.agent.calculate_position_size(
                self.position_manager.balance,
                current_price
            )
            stop_loss, take_profit = self.agent.calculate_stop_loss_take_profit(
                current_price,
                "LONG"
            )

            self.position_manager.open_position(
                symbol=self.symbol,
                side=PositionSide.LONG,
                entry_price=current_price,
                size=position_size,
                stop_loss=stop_loss,
                take_profit=take_profit
            )
            print(f"  Stop Loss: {stop_loss:.2f} | Take Profit: {take_profit:.2f}")

        elif signal == Signal.SELL and has_position:
            self.position_manager.close_position(current_price, "Agent signal")

        # Display account status
        print(f"Balance: {self.position_manager.balance:.2f} USDT")

    def run(self):
        """Run the trading loop"""
        self.initialize()
        self.running = True

        try:
            while self.running:
                try:
                    # Fetch latest candle
                    candle = self.data_feed.fetch_latest_candle()

                    if candle:
                        self.process_candle(candle)
                    else:
                        print(".", end="", flush=True)

                    # Wait before next check
                    time.sleep(self.check_interval)

                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"\nError in trading loop: {e}")
                    time.sleep(self.check_interval)

        except KeyboardInterrupt:
            print("\n\nStopping trading loop...")
            self.stop()

    def stop(self):
        """Stop the trading loop and display final statistics"""
        self.running = False

        # Close any open positions
        if self.position_manager.has_open_position():
            current_price = self.data_feed.get_current_price()
            if current_price:
                self.position_manager.close_position(current_price, "Loop stopped")

        # Display final statistics
        print("\n" + "=" * 60)
        print("Trading Session Summary")
        print("=" * 60)

        stats = self.position_manager.get_statistics()
        print(f"Total Trades: {stats['total_trades']}")
        print(f"Winning Trades: {stats['winning_trades']}")
        print(f"Losing Trades: {stats['losing_trades']}")
        print(f"Win Rate: {stats['win_rate']:.2f}%")
        print(f"Total PnL: {stats['total_pnl']:.2f} USDT")
        print(f"Return: {stats['return_percentage']:.2f}%")
        print(f"Final Balance: {stats['current_balance']:.2f} USDT")
        print("=" * 60)
