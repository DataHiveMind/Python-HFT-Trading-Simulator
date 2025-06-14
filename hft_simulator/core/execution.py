import time
import uuid
from typing import Dict, Callable, Optional

class OrderStatus:
    NEW = "NEW"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"

class Order:
    def __init__(self, symbol: str, side: str, price: float, volume: int):
        self.id = str(uuid.uuid4())
        self.symbol = symbol
        self.side = side  # "BUY" or "SELL"
        self.price = price
        self.volume = volume
        self.status = OrderStatus.NEW

class ExecutionEngine:
    def __init__(self, order_book_callback: Callable[[Order], Dict], latency: float = 0.01):
        self.orders: Dict[str, Order] = {}
        self.order_book_callback = order_book_callback
        self.latency = latency  # Simulated latency in seconds

    def send_order(self, symbol: str, side: str, price: float, volume: int) -> str:
        order = Order(symbol, side, price, volume)
        self.orders[order.id] = order
        time.sleep(self.latency)  # Simulate execution latency
        response = self.order_book_callback(order)
        self._handle_response(order, response)
        return order.id

    def _handle_response(self, order: Order, response: Dict):
        if response.get("status") == OrderStatus.FILLED:
            order.status = OrderStatus.FILLED
        elif response.get("status") == OrderStatus.REJECTED:
            order.status = OrderStatus.REJECTED
        elif response.get("status") == OrderStatus.PARTIALLY_FILLED:
            order.status = OrderStatus.PARTIALLY_FILLED
        elif response.get("status") == OrderStatus.CANCELLED:
            order.status = OrderStatus.CANCELLED

    def cancel_order(self, order_id: str):
        order = self.orders.get(order_id)
        if order and order.status == OrderStatus.NEW:
            order.status = OrderStatus.CANCELLED

    def get_order_status(self, order_id: str) -> Optional[str]:
        order = self.orders.get(order_id)
        return order.status if order else None

    def update_position(self, order_id: str, position_tracker: Callable[[Order], None]):
        order = self.orders.get(order_id)
        if order and order.status == OrderStatus.FILLED:
            position_tracker(order)

# Example usage:
# def mock_order_book(order: Order) -> Dict:
#     # Simulate always filled
#     return {"status": OrderStatus.FILLED}
#
# engine = ExecutionEngine(order_book_callback=mock_order_book)
# order_id = engine.send_order("AAPL", "BUY", 150.0, 10)
#