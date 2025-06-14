# tests/test_risk_management.py
from hft_simulator.core.risk_management import RiskManager

def test_risk_limits():
    risk_manager = RiskManager(max_position=100)
    
    # Test scenario within acceptable limits
    assert risk_manager.assess_risk(50) is True
    
    # Test scenario exceeding limits
    assert risk_manager.assess_risk(150) is False
