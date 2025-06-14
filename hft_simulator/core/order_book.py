import heapq
import uuid
from typing import Optional, Dict, List, Tuple

class Order:
    def __init__(self, side: str, price: float, volume: int):
        self.id = str(uuid.uuid4())
        self.side = side  # "BUY" or "SELL"
        self.price = price
        self.volume = volume

class OrderBook:
    def __init__(self):
        # Max-heap for bids (invert price for heapq)
        self.bids: List[Tuple[float, str, Order]] = []
        # Min-heap for asks
        self.asks: List[Tuple[float, str, Order]] = []
        # Order lookup for cancel/modify
        self.order_map: Dict[str, Tuple[str, float, Order]] = {}

    def add_order(self, side: str, price: float, volume: int) -> str:
        order = Order(side, price, volume)
        if side == "BUY":
            heapq.heappush(self.bids, (-price, order.id, order))
        else:
            heapq.heappush(self.asks, (price, order.id, order))
        self.order_map[order.id] = (side, price, order)
        self.match_orders()
        return order.id

    def cancel_order(self, order_id: str) -> bool:
        if order_id not in self.order_map:
            return False
        side, price, order = self.order_map.pop(order_id)
        # Mark order as cancelled (lazy deletion)
        order.volume = 0
        return True

    def modify_order(self, order_id: str, new_price: float, new_volume: int) -> bool:
        if order_id not in self.order_map:
            return False
        side, _, order = self.order_map[order_id]
        self.cancel_order(order_id)
        self.add_order(side, new_price, new_volume)
        return True

    def get_best_bid(self) -> Optional[Tuple[float, int]]:
        while self.bids:
            price, order_id, order = self.bids[0]
            if order.volume > 0:
                return (-price, order.volume)
            heapq.heappop(self.bids)  # Remove cancelled/filled
        return None

    def get_best_ask(self) -> Optional[Tuple[float, int]]:
        while self.asks:
            price, order_id, order = self.asks[0]
            if order.volume > 0:
                return (price, order.volume)
            heapq.heappop(self.asks)  # Remove cancelled/filled
        return None

    def match_orders(self):
        # Simple price-time priority matching
        while self.bids and self.asks:
            best_bid = self.bids[0][2]
            best_ask = self.asks[0][2]
            if best_bid.volume == 0:
                heapq.heappop(self.bids)
                continue
            if best_ask.volume == 0:
                heapq.heappop(self.asks)
                continue
            if -self.bids[0][0] >= self.asks[0][0]:
                trade_volume = min(best_bid.volume, best_ask.volume)
                best_bid.volume -= trade_volume
                best_ask.volume -= trade_volume
                # Optionally, log or process the trade here
            else:
                break

# Example usage:
# ob = OrderBook()
# ob.add_order("BUY", 100.0, 10)
# ob.add_order("SELL", 99.5, 5)
# print(ob.get_best_bid())
# print(ob.get_best_ask())