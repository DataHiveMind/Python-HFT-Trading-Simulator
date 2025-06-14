import pandas as pd
import numpy as np
from typing import Callable, Dict, Any, List

class BacktestResult:
    def __init__(self, trades: List[Dict[str, Any]], equity_curve: pd.Series):
        self.trades = trades
        self.equity_curve = equity_curve
        self.pnl = equity_curve.iloc[-1] - equity_curve.iloc[0]
        self.sharpe = self._compute_sharpe(equity_curve)
        self.max_drawdown = self._compute_max_drawdown(equity_curve)

    def _compute_sharpe(self, equity_curve: pd.Series, risk_free_rate: float = 0.0) -> float:
        returns = equity_curve.pct_change().dropna()
        if returns.std() == 0:
            return 0.0
        return (returns.mean() - risk_free_rate) / returns.std() * np.sqrt(252)

    def _compute_max_drawdown(self, equity_curve: pd.Series) -> float:
        roll_max = equity_curve.cummax()
        drawdown = (equity_curve - roll_max) / roll_max
        return drawdown.min()

class Backtester:
    def __init__(
        self,
        data: pd.DataFrame,
        strategy_func: Callable[[List[float], Any], str],
        execution_func: Callable[[str, float, int], Dict[str, Any]],
        config: Any
    ):
        self.data = data
        self.strategy_func = strategy_func
        self.execution_func = execution_func
        self.config = config
        self.trades = []
        self.equity_curve = []

    def run(self, initial_cash: float = 100000.0) -> BacktestResult:
        cash = initial_cash
        position = 0
        prices = []
        equity = []

        for idx, row in self.data.iterrows():
            price = row['price']
            prices.append(price)
            signal = self.strategy_func(prices, self.config)
            order = None

            if signal == "BUY" and position <= 0:
                order = self.execution_func("BUY", price, 1)
                if order.get("status") == "FILLED":
                    position += 1
                    cash -= price
                    self.trades.append({"side": "BUY", "price": price, "timestamp": row['timestamp']})
            elif signal == "SELL" and position >= 0:
                order = self.execution_func("SELL", price, 1)
                if order.get("status") == "FILLED":
                    position -= 1
                    cash += price
                    self.trades.append({"side": "SELL", "price": price, "timestamp": row['timestamp']})

            equity.append(cash + position * price)

        equity_curve = pd.Series(equity, index=self.data['timestamp'])
        return BacktestResult(self.trades, equity_curve)

# Example usage:
# import pandas as pd
# from strategy import StrategyConfig, generate_signal
#
# data = pd.read_csv("data/sample_ticks.csv", parse_dates=["timestamp"])
# config = StrategyConfig(short_window=5, long_window=20)
#
# def mock_execution(side, price, volume):
#     return {"status": "FILLED"}
#
# backtester = Backtester(data, generate_signal, mock_execution, config)
# result = backtester.run()
# print("PnL:", result.pnl)
# print("Sharpe:", result.sharpe)
# print("Max Drawdown:", result.max_drawdown)
# # result.equity_curve