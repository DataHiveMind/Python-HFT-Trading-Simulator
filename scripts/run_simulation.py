# run_simulation.py
from hft_simulator.core.market_data import MarketDataSimulator
from hft_simulator.core.order_book import OrderBook
from hft_simulator.core.strategy import Strategy
from hft_simulator.core.execution import ExecutionEngine
from hft_simulator.core.backtest import Backtester
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    
    # Initialize components
    order_book = OrderBook()
    market_data = MarketDataSimulator(data_source="data/historical_ticks.csv")
    strategy = Strategy(order_book)
    engine = ExecutionEngine()
    backtester = Backtester(engine)

    # Simulation loop: feed market ticks and apply strategy
    for tick in market_data.tick_generator():
        order_book.process_tick(tick)
        decision = strategy.on_new_tick(tick['price'])
        if decision:
            side, price, volume = decision
            if engine.risk_check():
                fill = engine.send_order(side, price, volume)
                backtester.record_trade(fill)

    metrics = backtester.performance_metrics()
    logging.info(f"Simulation Metrics: {metrics}")

if __name__ == "__main__":
    main()
