from datetime import datetime
from typing import Any, Optional, List, Union
import numpy as np

def normalize_price(price: Union[float, str]) -> float:
    """
    Normalize price to float. Returns 0.0 if conversion fails.
    """
    try:
        return float(price)
    except (ValueError, TypeError):
        return 0.0

def normalize_volume(volume: Union[int, str]) -> int:
    """
    Normalize volume to int. Returns 0 if conversion fails.
    """
    try:
        return int(volume)
    except (ValueError, TypeError):
        return 0

def convert_timestamp(ts: Optional[str]) -> Optional[datetime]:
    """
    Convert a timestamp string to a datetime object.
    Supports multiple formats. Returns None if parsing fails.
    """
    if not ts:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    return None

def moving_average(arr: List[float], window: int) -> Optional[float]:
    """
    Compute the moving average of the last 'window' elements in arr.
    Returns None if not enough data.
    """
    if len(arr) < window or window <= 0:
        return None
    return float(np.mean(arr[-window:]))

def min_max_scale(arr: List[float]) -> List[float]:
    """
    Min-max scale a list of floats to [0, 1].
    Returns zeros if all values are the same.
    """
    arr_np = np.array(arr, dtype=float)
    min_val = arr_np.min()
    max_val = arr_np.max()
    if max_val == min_val:
        return [0.0 for _ in arr]
    return ((arr_np - min_val) / (max_val - min_val)).tolist()

# Unit tests
def _test_normalize_price():
    assert normalize_price("100.5") == 100.5
    assert normalize_price(42) == 42.0
    assert normalize_price(None) == 0.0

def _test_normalize_volume():
    assert normalize_volume("10") == 10
    assert normalize_volume(5) == 5
    assert normalize_volume(None) == 0

def _test_convert_timestamp():
    assert convert_timestamp("2023-01-01 12:00:00.123456") == datetime(2023, 1, 1, 12, 0, 0, 123456)
    assert convert_timestamp("2023-01-01 12:00:00") == datetime(2023, 1, 1, 12, 0, 0)
    assert convert_timestamp("2023/01/01 12:00:00") == datetime(2023, 1, 1, 12, 0, 0)
    assert convert_timestamp("bad format") is None

def _test_moving_average():
    assert moving_average([1, 2, 3, 4, 5], 3) == 4.0
    assert moving_average([1, 2], 3) is None

def _test_min_max_scale():
    assert min_max_scale([1, 2, 3]) == [0.0, 0.5, 1.0]
    assert min_max_scale([5, 5, 5]) == [0.0, 0.0, 0.0]

def run_tests():
    _test_normalize_price()
    _test_normalize_volume()
    _test_convert_timestamp()
    _test_moving_average()
    _test_min_max_scale()
    print("All utils.py tests passed.")

# Uncomment to run tests directly
# if __name__ == "__main__":