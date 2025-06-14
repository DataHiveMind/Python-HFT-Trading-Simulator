import asyncio
import random
from typing import Callable, Any, Coroutine

class LatencySimulator:
    def __init__(self, base_delay: float = 0.001, jitter: float = 0.0005):
        """
        base_delay: base network or processing delay in seconds (e.g., 0.001 for 1ms)
        jitter: max random jitter to add/subtract from base_delay (in seconds)
        """
        self.base_delay = base_delay
        self.jitter = jitter

    async def inject_latency(self):
        """Simulate network/exchange latency with jitter."""
        delay = self.base_delay + random.uniform(-self.jitter, self.jitter)
        delay = max(0, delay)
        await asyncio.sleep(delay)

    async def wrap_async(self, coro_func: Callable[..., Coroutine], *args, **kwargs) -> Any:
        """Wrap an async function, injecting latency before execution."""
        await self.inject_latency()
        return await coro_func(*args, **kwargs)

    async def wrap_sync(self, func: Callable, *args, **kwargs) -> Any:
        """Wrap a sync function, injecting latency before execution."""
        await self.inject_latency()
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)

# Example integration for market data/event streaming:
async def async_market_event_stream(event_generator, latency_sim: LatencySimulator):
    """Yield events asynchronously with simulated latency."""
    for event in event_generator:
        await latency_sim.inject_latency()
        yield event

# Example usage:
# import asyncio
# latency_sim = LatencySimulator(base_delay=0.001, jitter=0.0005)
#
# async def main():
#     async for event in async_market_event_stream(market_event_stream(data), latency_sim):
#         print(event)
#