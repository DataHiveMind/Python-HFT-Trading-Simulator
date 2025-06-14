from typing import Dict, List, Optional, Callable, Any
import heapq
import numpy as np

class Venue:
    """Simulated exchange or liquidity pool."""
    def __init__(self, name: str, fee: float = 0.0):
        self.name = name
        self.fee = fee
        self.order_book = []  # Simple list for demonstration

    def add_order(self, side: str, price: float, volume: int, order_type: str = "LIMIT") -> Dict[str, Any]:
        # In a real system, this would interact with an OrderBook instance
        order = {"side": side, "price": price, "volume": volume, "type": order_type, "venue": self.name}
        self.order_book.append(order)
        return {"status": "ACCEPTED", "order": order}

    def get_best_price(self, side: str) -> Optional[float]:
        filtered = [o for o in self.order_book if o["side"] == side and o["volume"] > 0]
        if not filtered:
            return None
        if side == "BUY":
            return max(o["price"] for o in filtered)
        else:
            return min(o["price"] for o in filtered)

class SmartOrderRouter:
    def __init__(self, venues: List[Venue]):
        self.venues = venues

    def route_order(self, side: str, price: float, volume: int, order_type: str = "LIMIT", smart: bool = True) -> List[Dict[str, Any]]:
        """
        Route order across venues.
        If smart=True, split order for best price/venue.
        """
        results = []
        remaining = volume

        # Gather best prices from all venues
        venue_prices = []
        for venue in self.venues:
            best = venue.get_best_price("SELL" if side == "BUY" else "BUY")
            if best is not None:
                venue_prices.append((best, venue))

        # Sort venues for best execution
        if side == "BUY":
            venue_prices.sort(key=lambda x: x[0])  # Lowest ask first
        else:
            venue_prices.sort(key=lambda x: -x[0])  # Highest bid first

        # Smart routing: split order across venues for best price
        for best_price, venue in venue_prices:
            if (side == "BUY" and price >= best_price) or (side == "SELL" and price <= best_price):
                # Simulate full fill at best price for simplicity
                fill_volume = min(remaining, volume)  # In real life, use venue's available liquidity
                result = venue.add_order(side, best_price, fill_volume, order_type)
                results.append(result)
                remaining -= fill_volume
                if remaining <= 0:
                    break

        # If not fully filled, send remainder to first venue as passive order
        if remaining > 0 and self.venues:
            result = self.venues[0].add_order(side, price, remaining, order_type)
            results.append(result)

        return results

    def iceberg_order(self, side: str, price: float, total_volume: int, display_size: int, order_type: str = "LIMIT") -> List[Dict[str, Any]]:
        """
        Simulate iceberg order: only display a portion of the total volume at a time.
        """
        results = []
        remaining = total_volume
        while remaining > 0:
            chunk = min(display_size, remaining)
            chunk_results = self.route_order(side, price, chunk, order_type)
            results.extend(chunk_results)
            remaining -= chunk
            # In real HFT, would wait for fills before posting next chunk
        return results

# Optional: Performance optimization hooks
try:
    from numba import njit
    @njit
    def fast_min(arr):
        return np.min(arr)
except ImportError:
    def fast_min(arr):
        return min(arr)

# Example usage: