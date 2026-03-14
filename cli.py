#!/usr/bin/env python3
"""CLI entry point for the Binance Futures Trading Bot."""
import argparse
import os
import sys
from dotenv import load_dotenv

from bot.logging_config import setup_logging, get_logger
from bot.client import BinanceClient, BinanceAPIError
from bot.orders import OrderManager, print_order_summary, print_order_response
from bot.validators import ValidationError, validate_symbol, validate_side, validate_order_type

load_dotenv()
setup_logging()
logger = get_logger("cli")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  Market BUY:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  Limit SELL:
    python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 99000

  Stop-Market BUY:
    python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.001 --stop-price 95000
        """
    )
    parser.add_argument("--symbol",     required=True,  help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",       required=True,  help="BUY or SELL")
    parser.add_argument("--type",       required=True,  dest="order_type", help="MARKET, LIMIT, or STOP_MARKET")
    parser.add_argument("--quantity",   required=True,  help="Order quantity")
    parser.add_argument("--price",      required=False, default=None, help="Limit price (required for LIMIT)")
    parser.add_argument("--stop-price", required=False, default=None, dest="stop_price", help="Stop price (required for STOP_MARKET)")
    parser.add_argument("--tif",        required=False, default="GTC", help="Time in force: GTC, IOC, FOK (default: GTC)")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Validate inputs early
    try:
        symbol     = validate_symbol(args.symbol)
        side       = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
    except ValidationError as e:
        print(f"\n❌ Validation Error: {e}\n")
        logger.error("Validation error: %s", e)
        sys.exit(1)

    # Load API credentials
    api_key    = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        print("\n❌ Missing API credentials. Check your .env file.\n")
        logger.error("Missing BINANCE_API_KEY or BINANCE_API_SECRET in environment.")
        sys.exit(1)

    # Print summary before placing
    print_order_summary(
        order_type=order_type,
        symbol=symbol,
        side=side,
        quantity=args.quantity,
        price=args.price,
        stop_price=args.stop_price,
    )

    # Build client and manager
    client  = BinanceClient(api_key=api_key, api_secret=api_secret)
    manager = OrderManager(client=client)

    try:
        if order_type == "MARKET":
            response = manager.place_market_order(
                symbol=symbol, side=side, quantity=args.quantity
            )
        elif order_type == "LIMIT":
            response = manager.place_limit_order(
                symbol=symbol, side=side, quantity=args.quantity,
                price=args.price, time_in_force=args.tif
            )
        elif order_type == "STOP_MARKET":
            response = manager.place_stop_market_order(
                symbol=symbol, side=side, quantity=args.quantity,
                stop_price=args.stop_price
            )
        else:
            print(f"\n❌ Unsupported order type: {order_type}\n")
            sys.exit(1)

        print_order_response(response)

    except ValidationError as e:
        print(f"\n❌ Validation Error: {e}\n")
        logger.error("Validation error: %s", e)
        sys.exit(1)
    except BinanceAPIError as e:
        print(f"\n❌ Binance API Error {e.code}: {e.message}\n")
        logger.error("BinanceAPIError: %s", e)
        sys.exit(1)
    except (ConnectionError, TimeoutError) as e:
        print(f"\n❌ Network Error: {e}\n")
        logger.error("Network error: %s", e)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}\n")
        logger.exception("Unexpected error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
