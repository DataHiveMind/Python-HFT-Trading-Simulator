import os
import csv
from datetime import datetime
from typing import Dict, Generator, Any, Optional

DATA_DIR = "data"

def load_market_data(filename: str) -> list[Dict[str, Any]]:
    """Load tick data from a CSV file in the data/ directory."""
    path = os.path.join(DATA_DIR, filename)
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [normalize_tick(row) for row in reader]
    return data

def normalize_tick(tick: Dict[str, str]) -> Dict[str, Any]:
    """Normalize and format a raw tick dictionary."""
    return {
        "timestamp": convert_timestamp(tick.get("timestamp")),
        "symbol": tick.get("symbol"),
        "price": float(tick.get("price", 0)),
        "volume": int(tick.get("volume", 0)),
        "side": tick.get("side", "unknown")
    }

def convert_timestamp(ts: Optional[str]) -> Optional[datetime]:
    """Convert a timestamp string to a datetime object."""
    if not ts:
        return None
    # Try common timestamp formats
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    return None

def market_event_stream(data: list[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
    """Yield market events one by one, simulating a data stream."""
    for tick in data:
        yield tick

# Example utility to feed events into an order book (stub)
def feed_events_to_order_book(event_stream, order_book_callback):
    """Feed events into the order book via a callback."""
    for event in event_stream:
        order_book_callback(event)

# Example usage:
# data = load_market_data("sample_ticks.csv")
# stream = market_event_stream(data)
# for event in stream:
#     print(event)