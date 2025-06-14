# tests/test_strategy.py
from hft_simulator.core.strategy import Strategy, compute_alpha_signal
from hft_simulator.core.order_book import OrderBook

def test_compute_alpha_signal():
    # Simulate historical prices where moving averages should generate a signal
    prices = [100, 101, 102, 103, 104, 105, 104, 103, 102, 101, 100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90]
    signal = compute_alpha_signal(prices)
    # Assert that the signal is computed (you can set a fixed expected outcome)
    assert signal is not None

def test_strategy_decision():
    # Create a sample order book and strategy instance
    ob = OrderBook()
    # Simulate adding orders to represent current market state
    ob.add_bid(100, 10)
    ob.add_ask(101, 10)
    strategy = Strategy(ob)
    
    # Feed a new tick and verify that strategy produces a decision
    decision = strategy.on_new_tick(100.5)
    # The output is structured as ("BUY"/"SELL", price, volume) or None
    assert decision in [None, ("BUY", 100.5, 10), ("SELL", 100.5, 10)]
