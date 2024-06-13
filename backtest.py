import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG  # Example data

def compute_macd(series, short_window=12, long_window=26, signal_window=9):
    short_ema = series.ewm(span=short_window, adjust=False).mean()
    long_ema = series.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    hist = macd - signal
    return macd, signal, hist

class MACD_EMA_Strategy(Strategy):
    short_window = 12
    long_window = 26
    signal_window = 9

    def init(self):
        close = self.data.Close
        self.macd, self.signal, self.hist = compute_macd(close, self.short_window, self.long_window, self.signal_window)

    def next(self):
        if crossover(self.macd, self.signal):
            self.buy()
        elif crossover(self.signal, self.macd):
            self.sell()

# Backtest the strategy
bt = Backtest(GOOG, MACD_EMA_Strategy, cash=10_000, commission=.002)
stats = bt.run()
print(stats)

# Optimize the strategy
stats = bt.optimize(
    short_window=range(5, 20, 1),
    long_window=range(20, 50, 1),
    signal_window=range(5, 15, 1),
    maximize='Equity Final [$]'
)
print(stats)

# Visualize the results
bt.plot()