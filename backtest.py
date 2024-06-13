import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load data from CSV
data = pd.read_csv('your_ema_values.csv', parse_dates=True, index_col='Date')

# Ensure the columns are named correctly and match the strategy's requirements
print(data.head())

class MACD_EMA_Strategy(Strategy):
    def init(self):
        # Use precomputed MACD and Signal values from the CSV
        self.macd = self.data.MACD
        self.macd_signal = self.data.MACD_SIGNAL

    def next(self):
        if crossover(self.macd, self.macd_signal):
            self.buy()
        elif crossover(self.macd_signal, self.macd):
            self.sell()

# Backtest the strategy
bt = Backtest(data, MACD_EMA_Strategy, cash=10_000, commission=.002)
stats = bt.run()
print(stats)

# Visualize the results
bt.plot()

# Optimize the strategy
stats = bt.optimize(
    cash=10_000, # Starting cash for optimization
    commission=.002, # Commission for optimization
    maximize='Equity Final [$]'
)
print(stats)