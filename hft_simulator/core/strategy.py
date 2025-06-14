from typing import List, Dict, Optional

class StrategyConfig:
    """Configuration for trading strategy parameters."""
    def __init__(self, short_window: int = 5, long_window: int = 20):
        self.short_window = short_window
        self.long_window = long_window

def moving_average(prices: List[float], window: int) -> Optional[float]:
    """Compute the moving average for the last 'window' prices."""
    if len(prices) < window:
        return None
    return sum(prices[-window:]) / window

def generate_signal(prices: List[float], config: StrategyConfig) -> str:
    """
    Generate trading signal based on moving average crossover.
    Returns: "BUY", "SELL", or "HOLD"
    """
    short_ma = moving_average(prices, config.short_window)
    long_ma = moving_average(prices, config.long_window)
    if short_ma is None or long_ma is None:
        return "HOLD"
    if short_ma > long_ma:
        return "BUY"
    elif short_ma < long_ma:
        return "SELL"
    else:
        return "HOLD"

def decide_order_action(prices: List[float], config: StrategyConfig) -> str:
    """Determine order action based on the generated signal."""
    signal = generate_signal(prices, config)
    return signal

# Example usage:
# config = StrategyConfig(short_window=10, long_window=50)
# prices = [tick['price'] for tick in recent_ticks]
# action = decide_order_action(prices, config)
# if action == "BUY":
#     # send buy order
# elif action == "SELL":
#     # send sell order