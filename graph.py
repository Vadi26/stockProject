import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# Load the CSV file into a DataFrame
df = pd.read_csv('ohlc_data.csv', parse_dates=True, index_col='Date')

# Convert DataFrame to the format required by mplfinance
ohlc_data = df[['Open', 'High', 'Low', 'Close']]

# Generate the buy and sell signals
buy_signals = df[df['signals'] == 1]
sell_signals = df[df['signals'] == -1]

# Create a new column for signals to mark on the plot
df['Buy'] = df['signals'].apply(lambda x: df['Low'] if x == 1 else None)
df['Sell'] = df['signals'].apply(lambda x: df['High'] if x == -1 else None)

# Prepare the additional plots for buy and sell markers
add_plots = [
    mpf.make_addplot(buy_signals['Low'], type='scatter', markersize=100, marker='^', color='g'),
    mpf.make_addplot(sell_signals['High'], type='scatter', markersize=100, marker='v', color='r')
]

# Plot the candlestick chart
mpf.plot(ohlc_data, type='candle', addplot=add_plots, volume=True, style='yahoo')

plt.show()