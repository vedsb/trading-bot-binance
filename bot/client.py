"""Binance Futures Testnet REST client — HMAC-SHA256 signed."""
from __future__ import annotations
import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode
import requests
from .logging_config import get_logger

logger = get_logger("client")
BASE_URL = "https://testnet.binancefuture.com"

class BinanceAPIError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Binance API error {code}: {message}")

class BinanceClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = BASE_URL):
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        logger.debug("BinanceClient initialised → %s", self.base_url)

    def _sign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        server_time = requests.get(f"{self.base_url}/fapi/v1/time", timeout=5).json()["serverTime"]
        params["timestamp"] = server_time
        params["recvWindow"] = 5000
        query = urlencode(params)
        sig = hmac.new(self.api_secret, query.encode(), hashlib.sha256).hexdigest()
        params["signature"] = sig
        return params

    def _request(self, method: str, endpoint: str,
                 params: Optional[Dict] = None, signed: bool = False) -> Any:
        url = f"{self.base_url}{endpoint}"
        params = params or {}
        if signed:
            params = self._sign(params)

        safe = {k: v for k, v in params.items() if k != "signature"}
        logger.debug("→ %s %s | params: %s", method, endpoint, safe)

        try:
            if method == "GET":
                resp = self.session.get(url, params=params, timeout=10)
            elif method == "POST":
                resp = self.session.post(url, data=params, timeout=10)
            elif method == "DELETE":
                resp = self.session.delete(url, params=params, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
        except requests.exceptions.ConnectionError as e:
            logger.error("Network error: %s", e)
            raise ConnectionError(f"Cannot reach Binance API: {e}") from e
        except requests.exceptions.Timeout:
            logger.error("Request timed out.")
            raise TimeoutError("Binance API request timed out.")

        logger.debug("← %s %s | HTTP %s", method, endpoint, resp.status_code)

        try:
            data = resp.json()
        except Exception:
            resp.raise_for_status()
            raise

        if isinstance(data, dict) and data.get("code", 0) < 0:
            logger.error("API error | code=%s msg=%s", data["code"], data.get("msg"))
            raise BinanceAPIError(data["code"], data.get("msg", "Unknown error"))

        if not resp.ok:
            logger.error("HTTP %s | %s", resp.status_code, data)
            resp.raise_for_status()

        logger.debug("Response: %s", data)
        return data

    def place_order(self, **kwargs) -> Dict[str, Any]:
        params = {k: str(v) for k, v in kwargs.items() if v is not None}
        logger.info("Placing order → %s", params)
        result = self._request("POST", "/fapi/v1/order", params=params, signed=True)
        logger.info("Order accepted → orderId=%s status=%s", result.get("orderId"), result.get("status"))
        return result

    def get_account(self) -> Dict[str, Any]:
        return self._request("GET", "/fapi/v2/account", signed=True)

    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        return self._request("DELETE", "/fapi/v1/order",
                             params={"symbol": symbol, "orderId": order_id}, signed=True)