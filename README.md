# Binance Futures Testnet Trading Bot

A Python CLI trading bot for placing orders on Binance Futures Testnet (USDT-M).

## Features
- Market, Limit, and Stop-Market orders
- BUY and SELL support
- Structured logging (file + console)
- Input validation and error handling
- Clean CLI via argparse

## Setup

### 1. Clone / unzip the project
```bash
cd trading_bot
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API keys
Create a `.env` file in the root folder:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

---

## How to Run

### Market BUY
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Limit SELL
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 99000
```

### Stop-Market BUY (Bonus)
```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.001 --stop-price 95000
```

---

## Project Structure
```
trading_bot/
  bot/
    __init__.py
    client.py         # Binance REST API wrapper (HMAC-SHA256)
    orders.py         # Order placement logic + output formatting
    validators.py     # Input validation
    logging_config.py # Logging setup
  cli.py              # CLI entry point
  .env                # API credentials (not committed)
  requirements.txt
  README.md
```

## Logs
All logs are saved to `logs/trading_bot.log`.

## Assumptions
- Uses Binance Futures Testnet only (base URL: https://testnet.binancefuture.com)
- Requires valid USDT-M futures testnet API keys
- Quantity precision must match the symbol's rules on Binance
