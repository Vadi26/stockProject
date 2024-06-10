import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

csv_file = "RELIANCE.csv"

# Function to plot candlestick chart
def plot_candlestick(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file, parse_dates=True, index_col='Date')
    
    # Create the candlestick chart
    fig = make_subplots(rows=1, cols=1)
    
    candlestick = go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name='Candlesticks')
    
    fig.add_trace(candlestick)
    
    # Update layout for better visuals
    fig.update_layout(title='Reliance Chart',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False)
    
    fig.show()


    
plot_candlestick(csv_file)