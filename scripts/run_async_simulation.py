# run_async_simulation.py
import asyncio
import logging
from hft_simulator.core.order_book import OrderBook
from hft_simulator.core.strategy import Strategy
from hft_simulator.core.execution import ExecutionEngine
from hft_simulator.enhancements.latency import async_market_data_generator

async def run_async_simulation():
    logging.basicConfig(level=logging.INFO)
    
    order_book = OrderBook()
    strategy = Strategy(order_book)
    engine = ExecutionEngine()
    
    # Asynchronously process market data ticks
    async for tick in async_market_data_generator("data/historical_ticks.csv"):
        order_book.process_tick(tick)
        decision = strategy.on_new_tick(tick['price'])
        if decision and engine.risk_check():
            side, price, volume = decision
            fill = engine.send_order(side, price, volume)
            logging.info(f"Order executed: {fill}")
        await asyncio.sleep(0)  # Yield control to the event loop

if __name__ == "__main__":
    asyncio.run(run_async_simulation())
