# 🤖 Binance Futures Trading Bot

A lightweight Python CLI trading bot for placing orders on **Binance Futures Testnet (USDT-M)**.  
Built with clean, layered architecture — separate API client, order logic, validation, and CLI layers.

---

## ✨ Features

- ✅ Place **Market** and **Limit** orders
- ✅ Place **Stop-Market** orders (bonus)
- ✅ Support for both **BUY** and **SELL** sides
- ✅ Full **input validation** with clear error messages
- ✅ **Structured logging** to file and console
- ✅ Clean **CLI** via `argparse`
- ✅ Proper **exception handling** (API errors, network failures, bad input)

---

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance REST API wrapper (HMAC-SHA256)
│   ├── orders.py          # Order placement logic + output formatting
│   ├── validators.py      # Input validation
│   └── logging_config.py  # File + console logging setup
├── cli.py                 # CLI entry point
├── .env                   # API credentials (not committed)
├── requirements.txt
└── README.md
```

---
## 📸 Screenshots

### Market Order
![Market Order](Screenshot%202026-03-14%20150319.png)

### Limit Order
![Limit Order](Screenshot%202026-03-14%20150536.png)
## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/binance-futures-trading-bot.git
cd binance-futures-trading-bot
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API credentials
Create a `.env` file in the root folder:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

> 🔑 Get your free API keys from [Binance Futures Testnet](https://testnet.binancefuture.com) — login with GitHub, then click **API Key** tab.

---

## 🚀 How to Run

### Market Order
```bash
# BUY
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002

# SELL
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.002
```

### Limit Order
```bash
# BUY
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.002 --price 80000

# SELL
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 99000
```

### Stop-Market Order (Bonus)
```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.002 --stop-price 95000
```

---

## 📤 Sample Output

```
==================================================
       ORDER REQUEST SUMMARY
==================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.002
==================================================
2026-03-14 14:47:51 | INFO | Placing order → BTCUSDT BUY MARKET
2026-03-14 14:47:52 | INFO | Order accepted → orderId=12805987786 status=NEW
==================================================
       ORDER RESPONSE
==================================================
  Order ID   : 12805987786
  Symbol     : BTCUSDT
  Status     : NEW
  Side       : BUY
  Type       : MARKET
  Qty        : 0.002
  Executed   : 0.002
  Avg Price  : 83,241.50
==================================================
  ✅ ORDER PLACED SUCCESSFULLY
==================================================
```

---

## 📋 CLI Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--symbol` | ✅ | Trading pair e.g. `BTCUSDT` |
| `--side` | ✅ | `BUY` or `SELL` |
| `--type` | ✅ | `MARKET`, `LIMIT`, or `STOP_MARKET` |
| `--quantity` | ✅ | Order quantity e.g. `0.002` |
| `--price` | ⚠️ LIMIT only | Limit price e.g. `99000` |
| `--stop-price` | ⚠️ STOP_MARKET only | Stop trigger price |
| `--tif` | ❌ optional | Time in force: `GTC`, `IOC`, `FOK` (default: `GTC`) |

---

## 📝 Logs

All logs are saved to `logs/trading_bot.log`.

- **Console** → INFO level and above
- **File** → Full DEBUG detail including raw API requests and responses

---

## 🔒 Assumptions

- Uses **Binance Futures Testnet only** — no real money involved
- Base URL: `https://testnet.binancefuture.com`
- Minimum order notional value is **$100** (Binance requirement)
- API keys must be from the **Futures Testnet** specifically, not binance.com
- Uses server time sync to avoid timestamp errors

---

## 🛠️ Tech Stack

- Python 3.x
- `requests` — HTTP client
- `python-dotenv` — environment variable management
- `argparse` — CLI parsing
- `hmac` + `hashlib` — HMAC-SHA256 request signing
