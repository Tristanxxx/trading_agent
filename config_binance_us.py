"""
Configuration example for Binance.US
For US-based traders
"""

# Exchange Configuration
EXCHANGE = 'binance.us'  # Binance US
SYMBOL = 'BTC/USD'       # Note: Binance.US uses USD, not USDT for many pairs

# Account Configuration
INITIAL_BALANCE = 10000.0  # Starting balance in USD

# Trading Loop Configuration
CHECK_INTERVAL = 60  # Seconds between checks (60 = 1 minute)

# Agent Strategy Parameters
FAST_PERIOD = 9  # Fast moving average period
SLOW_PERIOD = 21  # Slow moving average period
RSI_PERIOD = 14  # RSI calculation period
RSI_OVERSOLD = 30  # RSI oversold threshold
RSI_OVERBOUGHT = 70  # RSI overbought threshold

# Risk Management
RISK_PERCENTAGE = 0.02  # Risk 2% of balance per trade
STOP_LOSS_PERCENTAGE = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENTAGE = 0.04  # 4% take profit (2:1 risk-reward ratio)
