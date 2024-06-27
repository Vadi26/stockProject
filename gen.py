import pandas as pd
import pandas_ta as ta

def append_indicators(df):
    # Calculate MACD
    macd = ta.macd(df['Close'])
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_Signal'] = macd['MACDs_12_26_9']

    # Calculate Bollinger Bands
    bb = ta.bbands(df['Close'])
    print(bb.columns)  # Print the columns to inspect the correct keys
    df['Upper_Band'] = bb.iloc[:, 0]  # Adjust the columns based on inspection
    df['Lower_Band'] = bb.iloc[:, 2]  # Adjust the columns based on inspection

    # Calculate VWAP
    df['VWAP'] = ta.vwap(df['High'], df['Low'], df['Close'], df['Volume'])

    # Calculate RSI
    df['RSI'] = ta.rsi(df['Close'])

    # Calculate EMA (e.g., 5-period and 20-period)
    df['Short_EMA'] = ta.ema(df['Close'], length=5)
    df['Long_EMA'] = ta.ema(df['Close'], length=20)

    return df

# Load your OHLCV data
df = pd.read_csv('ye.csv', parse_dates=True, index_col='Date')

# Append the indicator values
df = append_indicators(df)

# Save the dataframe with indicators (optional)
df.to_csv('ohlcv_with_indicators.csv')

# Print the dataframe to verify
print(df.head())

# Now you can pass this dataframe to the backtesting code
