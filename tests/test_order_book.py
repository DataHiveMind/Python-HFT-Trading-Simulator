# tests/test_order_book.py
import pytest
from hft_simulator.core.order_book import OrderBook

def test_add_order():
    ob = OrderBook()
    
    # Add bid orders and verify the best bid
    ob.add_bid(100, 10)
    ob.add_bid(101, 5)
    assert ob.best_bid() == 101
    
    # Add ask orders and verify the best ask
    ob.add_ask(102, 8)
    ob.add_ask(103, 12)
    assert ob.best_ask() == 102

def test_order_cancellation():
    ob = OrderBook()
    ob.add_bid(100, 10)
    ob.cancel_order('bid', 100)  # Presume cancel_order is implemented
    assert ob.best_bid() is None
