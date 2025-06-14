# tests/test_execution.py
from hft_simulator.core.execution import ExecutionEngine

def test_order_execution():
    engine = ExecutionEngine()
    
    # Test BUY order execution
    order = engine.send_order("BUY", 100, 10)
    assert engine.position == 10
    
    # Test SELL order execution
    order = engine.send_order("SELL", 101, 5)
    assert engine.position == 5  # 10 - 5

def test_risk_check_execution():
    engine = ExecutionEngine()
    
    # Submit multiple orders until risk limit should be triggered
    for _ in range(11):
        engine.send_order("BUY", 100, 10)
    # Assume risk_check returns False if position > 100 shares
    assert not engine.risk_check()
