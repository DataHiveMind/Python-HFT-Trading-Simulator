from typing import Dict, Callable

class RiskLimits:
    def __init__(self, max_position: int, max_order_size: int, stop_loss: float):
        self.max_position = max_position
        self.max_order_size = max_order_size
        self.stop_loss = stop_loss  # e.g., -1000.0 for max loss

class RiskManager:
    def __init__(self, limits: RiskLimits, alert_callback: Callable[[str], None]):
        self.limits = limits
        self.positions: Dict[str, int] = {}  # symbol -> position size
        self.pnl: float = 0.0
        self.alert_callback = alert_callback

    def check_order(self, symbol: str, side: str, volume: int) -> bool:
        """Validate order against risk limits."""
        new_position = self.positions.get(symbol, 0) + (volume if side == "BUY" else -volume)
        if abs(new_position) > self.limits.max_position:
            self.alert_callback(f"Position limit breached for {symbol}: {new_position}")
            return False
        if volume > self.limits.max_order_size:
            self.alert_callback(f"Order size limit breached: {volume}")
            return False
        return True

    def update_position(self, symbol: str, side: str, volume: int, price: float):
        """Update position and PnL after order execution."""
        pos = self.positions.get(symbol, 0)
        if side == "BUY":
            self.positions[symbol] = pos + volume
            self.pnl -= price * volume
        else:
            self.positions[symbol] = pos - volume
            self.pnl += price * volume
        self._check_stop_loss()

    def _check_stop_loss(self):
        if self.pnl < self.limits.stop_loss:
            self.alert_callback(f"Stop-loss triggered! PnL: {self.pnl}")

    def get_position(self, symbol: str) -> int:
        return self.positions.get(symbol, 0)

    def get_pnl(self) -> float:
        return self.pnl

# Example usage:
# def alert(msg): print("ALERT:", msg)
# limits = RiskLimits(max_position=100, max_order_size=50, stop_loss=-1000.0)
# risk = RiskManager(limits, alert)
# if risk.check_order("AAPL", "BUY", 60):