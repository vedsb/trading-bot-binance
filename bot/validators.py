from __future__ import annotations
import re
from decimal import Decimal, InvalidOperation
from typing import Optional

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}
SYMBOL_RE = re.compile(r"^[A-Z]{2,20}$")

class ValidationError(ValueError):
    pass

def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not SYMBOL_RE.match(s):
        raise ValidationError(f"Invalid symbol '{symbol}'. Use uppercase letters only, e.g. BTCUSDT.")
    return s

def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be BUY or SELL.")
    return s

def validate_order_type(order_type: str) -> str:
    ot = order_type.strip().upper()
    if ot not in VALID_ORDER_TYPES:
        raise ValidationError(f"Invalid order type '{order_type}'. Choose from: {', '.join(sorted(VALID_ORDER_TYPES))}.")
    return ot

def validate_quantity(quantity) -> Decimal:
    try:
        qty = Decimal(str(quantity))
    except InvalidOperation:
        raise ValidationError(f"Invalid quantity '{quantity}'.")
    if qty <= 0:
        raise ValidationError("Quantity must be > 0.")
    return qty

def validate_price(price: Optional[str], order_type: str) -> Optional[Decimal]:
    if order_type == "MARKET":
        if price is not None:
            raise ValidationError("Do not provide --price for MARKET orders.")
        return None
    if price is None:
        raise ValidationError(f"--price is required for {order_type} orders.")
    try:
        p = Decimal(str(price))
    except InvalidOperation:
        raise ValidationError(f"Invalid price '{price}'.")
    if p <= 0:
        raise ValidationError("Price must be > 0.")
    return p

def validate_stop_price(stop_price: Optional[str], order_type: str) -> Optional[Decimal]:
    if order_type != "STOP_MARKET":
        return None
    if stop_price is None:
        raise ValidationError("--stop-price is required for STOP_MARKET orders.")
    try:
        sp = Decimal(str(stop_price))
    except InvalidOperation:
        raise ValidationError(f"Invalid stop price '{stop_price}'.")
    if sp <= 0:
        raise ValidationError("Stop price must be > 0.")
    return sp
