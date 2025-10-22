# Trading Agent

A Python-based cryptocurrency trading agent that continuously feeds 1-minute market data and makes automated trading decisions using technical indicators.

## Features

- Real-time 1-minute cryptocurrency data feed from multiple exchanges
- Automated trading decisions using technical analysis (SMA crossover + RSI)
- Position management with stop-loss and take-profit
- Risk management and position sizing
- Trading statistics and performance tracking
- Configurable parameters for different trading strategies

## Architecture

The system consists of four main components:

1. **Data Feed** (`src/data_feed/`): Fetches 1-minute cryptocurrency candles from exchanges
2. **Trading Agent** (`src/agent/`): Analyzes market data and generates trading signals
3. **Position Manager** (`src/position/`): Manages open positions, PnL, and risk
4. **Trading Loop** (`src/trading_loop.py`): Orchestrates the entire system in an infinite loop

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd trading_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the trading agent with default settings (Binance BTC/USDT):

```bash
python main.py
```

### Custom Configuration

Run with custom exchange and trading pair:

```bash
python main.py --exchange binance --symbol ETH/USDT --balance 10000 --interval 60
```

Parameters:
- `--exchange`: Exchange name (default: binance)
- `--symbol`: Trading pair (default: BTC/USDT)
- `--balance`: Initial balance in quote currency (default: 10000)
- `--interval`: Check interval in seconds (default: 60)

### Configuration File

Edit `config.py` to customize trading strategy parameters:

```python
# Strategy Parameters
FAST_PERIOD = 9  # Fast moving average period
SLOW_PERIOD = 21  # Slow moving average period
RSI_PERIOD = 14  # RSI period
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

# Risk Management
RISK_PERCENTAGE = 0.02  # Risk 2% per trade
STOP_LOSS_PERCENTAGE = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENTAGE = 0.04  # 4% take profit
```

## Trading Strategy

The agent uses a combination of technical indicators:

1. **Moving Average Crossover**:
   - BUY when fast SMA crosses above slow SMA
   - SELL when fast SMA crosses below slow SMA

2. **RSI Filter**:
   - Only buy when RSI < 70 (not overbought)
   - Sell when RSI > 70 (overbought)

3. **Risk Management**:
   - 2% stop loss on each trade
   - 4% take profit target (2:1 risk-reward ratio)
   - Position sizing based on account balance

## Example Output

```
============================================================
Initializing Trading System
============================================================
Exchange: binance
Symbol: BTC/USDT
Initial Balance: 10000.00 USDT
============================================================

Fetching historical data for indicator initialization...
Loaded 50 historical candles

Initial Indicator Values:
  Fast SMA: 43250.50
  Slow SMA: 43180.25
  RSI: 52.34

Initialization complete. Starting trading loop...
============================================================

[2025-10-22 10:30:00]
Price: 43300.00 | Volume: 125.50
Indicators: Fast SMA: 43260.00 | Slow SMA: 43190.00 | RSI: 54.20
Balance: 10000.00 USDT

[2025-10-22 10:31:00]
Price: 43350.00 | Volume: 145.30
Buy signal: Fast SMA (43280.00) crossed above Slow SMA (43200.00), RSI: 56.40
Opened LONG position: 0.218 @ 43350.00
  Stop Loss: 42483.00 | Take Profit: 45084.00
Balance: 10000.00 USDT
```

## Project Structure

```
trading_agent/
├── src/
│   ├── data_feed/
│   │   ├── __init__.py
│   │   └── crypto_feed.py       # Data fetching logic
│   ├── agent/
│   │   ├── __init__.py
│   │   └── trading_agent.py     # Trading strategy and signals
│   ├── position/
│   │   ├── __init__.py
│   │   └── position_manager.py  # Position management
│   └── trading_loop.py           # Main trading loop
├── main.py                       # Entry point
├── config.py                     # Configuration
├── requirements.txt              # Dependencies
└── README.md
```

## Supported Exchanges

The system uses CCXT library and supports 100+ exchanges including:
- Binance
- Coinbase
- Kraken
- Bitfinex
- And many more...

## Warning

This is a basic trading agent for educational purposes.

**Important Notes:**
- This system trades with real market data but simulated execution
- No actual orders are placed on exchanges
- For live trading, you need to implement order execution and API authentication
- Always test thoroughly before using real funds
- Cryptocurrency trading carries significant risk

## Development

### Adding Custom Strategies

To implement your own trading strategy, modify `src/agent/trading_agent.py`:

```python
def analyze_market(self, candle: Dict, has_position: bool) -> Signal:
    # Your custom strategy logic here
    pass
```

### Adding New Indicators

Add indicator calculation methods in `TradingAgent` class:

```python
def calculate_custom_indicator(self, prices: List[float]) -> float:
    # Your indicator logic
    pass
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
