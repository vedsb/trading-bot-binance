"""High-level order placement logic."""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, Optional
from .client import BinanceClient
from .logging_config import get_logger
from .validators import validate_symbol, validate_side, validate_quantity, validate_price, validate_stop_price

logger = get_logger("orders")

class OrderManager:
    def __init__(self, client: BinanceClient):
        self.client = client

    def place_market_order(self, symbol: str, side: str, quantity) -> Dict[str, Any]:
        sym = validate_symbol(symbol)
        sd = validate_side(side)
        qty = validate_quantity(quantity)
        logger.info("MARKET | symbol=%s side=%s qty=%s", sym, sd, qty)
        return self.client.place_order(symbol=sym, side=sd, type="MARKET", quantity=qty)

    def place_limit_order(self, symbol: str, side: str, quantity,
                          price, time_in_force: str = "GTC") -> Dict[str, Any]:
        sym = validate_symbol(symbol)
        sd = validate_side(side)
        qty = validate_quantity(quantity)
        prc = validate_price(price, "LIMIT")
        logger.info("LIMIT | symbol=%s side=%s qty=%s price=%s tif=%s", sym, sd, qty, prc, time_in_force)
        return self.client.place_order(
            symbol=sym, side=sd, type="LIMIT",
            quantity=qty, price=prc, timeInForce=time_in_force
        )

    def place_stop_market_order(self, symbol: str, side: str,
                                quantity, stop_price) -> Dict[str, Any]:
        sym = validate_symbol(symbol)
        sd = validate_side(side)
        qty = validate_quantity(quantity)
        sp = validate_stop_price(stop_price, "STOP_MARKET")
        logger.info("STOP_MARKET | symbol=%s side=%s qty=%s stopPrice=%s", sym, sd, qty, sp)
        return self.client.place_order(
            symbol=sym, side=sd, type="STOP_MARKET",
            quantity=qty, stopPrice=sp
        )

def print_order_summary(order_type: str, symbol: str, side: str,
                        quantity, price=None, stop_price=None):
    print("\n" + "="*50)
    print("       ORDER REQUEST SUMMARY")
    print("="*50)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")
    if stop_price:
        print(f"  Stop Price : {stop_price}")
    print("="*50)

def print_order_response(response: Dict[str, Any]):
    print("\n" + "="*50)
    print("       ORDER RESPONSE")
    print("="*50)
    print(f"  Order ID   : {response.get('orderId', 'N/A')}")
    print(f"  Symbol     : {response.get('symbol', 'N/A')}")
    print(f"  Status     : {response.get('status', 'N/A')}")
    print(f"  Side       : {response.get('side', 'N/A')}")
    print(f"  Type       : {response.get('type', 'N/A')}")
    print(f"  Qty        : {response.get('origQty', 'N/A')}")
    print(f"  Executed   : {response.get('executedQty', 'N/A')}")
    avg = response.get('avgPrice') or response.get('price', 'N/A')
    print(f"  Avg Price  : {avg}")
    print("="*50)
    print("  ✅ ORDER PLACED SUCCESSFULLY")
    print("="*50 + "\n")
