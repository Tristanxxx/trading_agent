# Binance.US Quick Start Guide

This guide is specifically for US-based traders who want to use the trading agent with Binance.US.

## Why Binance.US?

Binance.US is the US-based version of Binance, compliant with US regulations. If you're located in the United States, you should use Binance.US instead of Binance International.

## Key Differences from Binance International

1. **Different Trading Pairs**: Binance.US uses `USD` instead of `USDT` for many pairs
   - Example: `BTC/USD` instead of `BTC/USDT`

2. **Limited Asset Selection**: Fewer cryptocurrencies available compared to international version

3. **US Regulations**: Compliant with US financial regulations

## Quick Start

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Test Connection

Test your connection to Binance.US:

```bash
python test_exchanges.py
```

This will test connectivity to multiple exchanges including Binance.US.

### 3. Run with Binance.US

#### Option A: Command Line

```bash
# BTC/USD on Binance.US
python main.py --exchange binance.us --symbol BTC/USD --balance 10000

# ETH/USD on Binance.US
python main.py --exchange binance.us --symbol ETH/USD --balance 5000
```

#### Option B: Configuration File

Copy the Binance.US configuration:

```bash
cp config_binance_us.py config.py
```

Then run:

```bash
python main.py
```

### 4. Customize Your Strategy

Edit `config_binance_us.py`:

```python
# Exchange Configuration
EXCHANGE = 'binance.us'
SYMBOL = 'BTC/USD'  # Change to your preferred pair

# Account Configuration
INITIAL_BALANCE = 10000.0

# Strategy Parameters
FAST_PERIOD = 9
SLOW_PERIOD = 21
RSI_PERIOD = 14
```

## Popular Trading Pairs on Binance.US

- `BTC/USD` - Bitcoin
- `ETH/USD` - Ethereum
- `BNB/USD` - Binance Coin
- `ADA/USD` - Cardano
- `SOL/USD` - Solana
- `MATIC/USD` - Polygon
- `AVAX/USD` - Avalanche

## Example Session

```bash
$ python main.py --exchange binance.us --symbol BTC/USD

============================================================
Initializing Trading System
============================================================
Connected to binanceus exchange
Exchange: binance.us
Symbol: BTC/USD
Initial Balance: 10000.00 USD
============================================================

Fetching historical data for indicator initialization...
Loaded 50 historical candles

Initial Indicator Values:
  Fast SMA: 43250.50
  Slow SMA: 43180.25
  RSI: 52.34

Initialization complete. Starting trading loop...
============================================================
```

## Important Notes

1. **Paper Trading**: This system does NOT place real orders. It's for strategy testing only.

2. **API Keys Not Required**: For market data (read-only), you don't need API keys.

3. **For Live Trading**: You would need to:
   - Create Binance.US API keys
   - Implement order execution
   - Add proper error handling and risk management

4. **Rate Limits**: Be mindful of Binance.US API rate limits when running the bot.

## Troubleshooting

### "Exchange not supported" error

Make sure you're using the correct exchange name:
- ✓ Correct: `binance.us` or `binanceus`
- ✗ Wrong: `binance_us`, `binance-us`, `binanceus.com`

### "Symbol not found" error

Verify the trading pair exists on Binance.US:
- Most pairs use `/USD` not `/USDT`
- Visit https://www.binance.us/markets to see available pairs

### Connection errors

- Check your internet connection
- Verify Binance.US is accessible in your region
- Some states in the US have restrictions

## Support

For issues specific to:
- **This trading agent**: Check the main README.md
- **Binance.US platform**: Visit https://support.binance.us/
- **CCXT library**: Visit https://github.com/ccxt/ccxt

## Disclaimer

This is educational software for strategy testing. Cryptocurrency trading carries significant risk. Always test thoroughly with paper trading before considering any real trading. This software is not affiliated with Binance or Binance.US.
