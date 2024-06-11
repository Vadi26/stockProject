import pandas as pd
import backtrader as bt
import backtrader.feeds as btfeeds

# Load the data
data = pd.read_csv('path_to_your_data.csv', parse_dates=True, index_col='Date')

class SignalStrategy(bt.Strategy):
    def __init__(self):
        self.signal = self.data.signal

    def next(self):
        if not self.position:  # Not in the market
            if self.signal[0] == 1:  # Buy signal
                self.buy()
            elif self.signal[0] == -1:  # Sell signal
                self.sell()
        else:  # In the market
            if self.position.size > 0 and self.signal[0] == -1:  # Long position and sell signal
                self.sell()
            elif self.position.size < 0 and self.signal[0] == 1:  # Short position and buy signal
                self.buy()

# Prepare the data feed
data_feed = btfeeds.PandasData(dataname=data)

# Create a cerebro entity
cerebro = bt.Cerebro()

# Add the custom strategy
cerebro.addstrategy(SignalStrategy)

# Add the data feed
cerebro.adddata(data_feed)

# Set the initial cash
cerebro.broker.set_cash(10000.0)

# Set the commission (optional)
cerebro.broker.setcommission(commission=0.001)

# Run the backtest
results = cerebro.run()

# Plot the results
cerebro.plot()