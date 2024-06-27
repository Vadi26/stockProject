import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

class MyStrategy(Strategy):
    def init(self):
        # Precompute indicators
        self.macd = self.data.MACD
        self.macd_signal = self.data.MACD_Signal
        self.vwap = self.data.VWAP
        self.rsi = self.data.RSI
        self.close = self.data.Close
        self.upper_band = self.data.Upper_Band
        self.lower_band = self.data.Lower_Band
        self.short_ema = self.data.Short_EMA
        self.long_ema = self.data.Long_EMA

    def next(self):
        # Get the latest values
        macd = self.macd[-1]
        macd_signal = self.macd_signal[-1]
        close_price = self.close[-1]
        vwap = self.vwap[-1]
        rsi = self.rsi[-1]
        upper_band = self.upper_band[-1]
        lower_band = self.lower_band[-1]
        short_ema = self.short_ema[-1]
        long_ema = self.long_ema[-1]

        # Determine MACD bullish/bearish signal
        macd_bullish = macd > macd_signal
        macd_bearish = macd < macd_signal

        # Determine Bollinger Bands confirmation
        bollinger_bullish = close_price > lower_band
        bollinger_bearish = close_price < upper_band

        # Determine VWAP trend confirmation
        vwap_bullish = close_price > vwap
        vwap_bearish = close_price < vwap

        # Determine RSI trend detection
        rsi_bullish = rsi > 50
        rsi_bearish = rsi < 50

        # Determine EMA trend direction
        ema_bullish = short_ema > long_ema
        ema_bearish = short_ema < long_ema

        # Determine buy signal
        if (macd_bullish and bollinger_bullish and vwap_bullish and rsi_bullish and ema_bullish):
            if not self.position:
                self.buy()
        
        # Determine sell signal
        elif (macd_bearish and bollinger_bearish and vwap_bearish and rsi_bearish and ema_bearish):
            if self.position:
                self.sell()

# Load your data
# Assume df is your DataFrame with OHLCV data and all the indicator values
df = pd.read_csv('your_data.csv', parse_dates=True, index_col='Date')

# Backtest the strategy
bt = Backtest(df, MyStrategy, cash=10000, commission=.002, exclusive_orders=True)
stats = bt.run()

# Print the results
print(stats)

# Plot the results
bt.plot()
