#!/usr/bin/env python3
"""
Main entry point for the trading agent
"""
import argparse
from src.trading_loop import TradingLoop


def main():
    parser = argparse.ArgumentParser(description='Cryptocurrency Trading Agent')
    parser.add_argument(
        '--exchange',
        type=str,
        default='binance',
        help='Exchange name (default: binance)'
    )
    parser.add_argument(
        '--symbol',
        type=str,
        default='BTC/USDT',
        help='Trading pair symbol (default: BTC/USDT)'
    )
    parser.add_argument(
        '--balance',
        type=float,
        default=10000.0,
        help='Initial balance in quote currency (default: 10000)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Check interval in seconds (default: 60)'
    )

    args = parser.parse_args()

    # Create and run trading loop
    trading_loop = TradingLoop(
        exchange=args.exchange,
        symbol=args.symbol,
        initial_balance=args.balance,
        check_interval=args.interval
    )

    trading_loop.run()


if __name__ == '__main__':
    main()
