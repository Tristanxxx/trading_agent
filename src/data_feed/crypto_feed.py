"""
Crypto Data Feed Module
Fetches 1-minute cryptocurrency data from exchanges
"""
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import ccxt
import pandas as pd


class CryptoDataFeed:
    """Fetches and provides 1-minute cryptocurrency data"""

    def __init__(self, exchange_name: str = 'binance', symbol: str = 'BTC/USDT'):
        """
        Initialize the data feed

        Args:
            exchange_name: Name of the exchange (default: binance)
            symbol: Trading pair symbol (default: BTC/USDT)
        """
        self.exchange_name = exchange_name
        self.symbol = symbol
        self.exchange = getattr(ccxt, exchange_name)()
        self.last_timestamp = None

    def fetch_latest_candle(self) -> Optional[Dict]:
        """
        Fetch the latest 1-minute candle

        Returns:
            Dictionary containing OHLCV data or None if error
        """
        try:
            # Fetch last 2 candles to ensure we get a complete one
            ohlcv = self.exchange.fetch_ohlcv(
                self.symbol,
                timeframe='1m',
                limit=2
            )

            if not ohlcv:
                return None

            # Use the second-to-last candle (completed candle)
            candle = ohlcv[-2] if len(ohlcv) > 1 else ohlcv[-1]

            # Skip if we've already processed this candle
            if self.last_timestamp == candle[0]:
                return None

            self.last_timestamp = candle[0]

            return {
                'timestamp': candle[0],
                'datetime': datetime.fromtimestamp(candle[0] / 1000),
                'open': candle[1],
                'high': candle[2],
                'low': candle[3],
                'close': candle[4],
                'volume': candle[5],
                'symbol': self.symbol
            }

        except Exception as e:
            print(f"Error fetching candle: {e}")
            return None

    def fetch_historical_candles(self, limit: int = 100) -> pd.DataFrame:
        """
        Fetch historical 1-minute candles for backtesting or analysis

        Args:
            limit: Number of candles to fetch

        Returns:
            DataFrame with OHLCV data
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(
                self.symbol,
                timeframe='1m',
                limit=limit
            )

            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df

        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return pd.DataFrame()

    def get_current_price(self) -> Optional[float]:
        """
        Get the current market price

        Returns:
            Current price or None if error
        """
        try:
            ticker = self.exchange.fetch_ticker(self.symbol)
            return ticker['last']
        except Exception as e:
            print(f"Error fetching current price: {e}")
            return None
