import pandas as pd
import plotly.graph_objects as go

# Load the CSV file into a DataFrame
df = pd.read_csv('ohlc_data.csv', parse_dates=['Date'])
df.set_index('Date', inplace=True)

# Rename 'vlue' column to 'Volume' if necessary
if 'vlue' in df.columns:
    df.rename(columns={'vlue': 'Volume'}, inplace=True)

# Create the candlestick chart
fig = go.Figure(data=[go.Candlestick(x=df.index,
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'],
                                     name='OHLC')])

# Generate the buy and sell signals
buy_signals = df[df['signals'] == 1]
sell_signals = df[df['signals'] == -1]

# Add buy markers
fig.add_trace(go.Scatter(x=buy_signals.index, 
                         y=buy_signals['Low'], 
                         mode='markers',
                         marker=dict(symbol='triangle-up', size=10, color='green'),
                         name='Buy Signal'))

# Add sell markers
fig.add_trace(go.Scatter(x=sell_signals.index, 
                         y=sell_signals['High'], 
                         mode='markers',
                         marker=dict(symbol='triangle-down', size=10, color='red'),
                         name='Sell Signal'))

# Update layout
fig.update_layout(title='Candlestick Chart with Buy and Sell Signals',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  template='plotly_dark')

# Show the plot
fig.show()