#!/usr/bin/env python3
"""
Test script to verify exchange connectivity
Tests connection to different exchanges and displays available trading pairs
"""
import sys
from src.data_feed import CryptoDataFeed


def test_exchange(exchange_name: str, symbol: str = 'BTC/USDT'):
    """Test connection to an exchange"""
    print(f"\n{'='*60}")
    print(f"Testing {exchange_name} exchange")
    print(f"{'='*60}")

    try:
        # Create data feed
        feed = CryptoDataFeed(exchange_name, symbol)

        # Test fetching current price
        print(f"Fetching current price for {symbol}...")
        price = feed.get_current_price()

        if price:
            print(f"✓ Successfully connected to {exchange_name}")
            print(f"✓ Current price of {symbol}: ${price:,.2f}")

            # Test fetching historical data
            print(f"\nFetching historical data...")
            df = feed.fetch_historical_candles(limit=5)

            if not df.empty:
                print(f"✓ Successfully fetched {len(df)} candles")
                print(f"\nLast 5 candles:")
                print(df[['datetime', 'close', 'volume']].tail())
            else:
                print("⚠ Warning: No historical data returned")

        else:
            print(f"✗ Failed to fetch price from {exchange_name}")

    except Exception as e:
        print(f"✗ Error connecting to {exchange_name}: {e}")


def main():
    """Run exchange connectivity tests"""
    print("\n" + "="*60)
    print("Exchange Connectivity Test")
    print("="*60)

    # Test different exchanges
    test_cases = [
        ('binance', 'BTC/USDT'),
        ('binance.us', 'BTC/USD'),
        ('coinbase', 'BTC/USD'),
        ('kraken', 'BTC/USDT'),
    ]

    for exchange, symbol in test_cases:
        test_exchange(exchange, symbol)

    print("\n" + "="*60)
    print("Tests completed")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
