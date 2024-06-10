import requests
import pandas as pd
import plotly.graph_objects as go

# Function to fetch OHLC data from Alpha Vantage
def fetch_ohlc_data(symbol, api_key, output_size='compact'):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize={output_size}&apikey={api_key}&datatype=csv'
    response = requests.get(url)
    file_name = f'{symbol}_ohlc.csv'
    with open(file_name, 'w') as file:
        file.write(response.text)
    print(f'Data for {symbol} saved to {file_name}')
    return file_name

# Function to plot candlestick chart
def plot_candlestick(csv_file):
    df = pd.read_csv(csv_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close'])])

    fig.update_layout(
        title='Candlestick Chart',
        yaxis_title='Stock Price',
        xaxis_title='Date',
        xaxis_rangeslider_visible=True
    )

    fig.show()

# Main function
def main():
    api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'
    symbol = 'AAPL'  # Example symbol for Apple Inc.
    
    csv_file = fetch_ohlc_data(symbol, api_key)
    plot_candlestick(csv_file)

if __name__ == '__main__':
    main()
