import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('ohlc_data.csv', parse_dates=['Date'])
df.set_index('Date', inplace=True)

# Ensure signals column is present
if 'signals' not in df.columns:
    raise ValueError("The CSV file must contain a 'signals' column")

# Initialize the backtest parameters
initial_cash = 100000  # Initial cash in USD
cash = initial_cash
positions = 0
portfolio_value = []

# Iterate over the DataFrame rows
for date, row in df.iterrows():
    signal = row['signals']
    close_price = row['Close']
    
    # Buy signal
    if signal == 1 and cash > 0:
        positions = cash / close_price
        cash = 0
        print(f"Buy on {date.date()} at {close_price:.2f}")
    
    # Sell signal
    elif signal == -1 and positions > 0:
        cash = positions * close_price
        positions = 0
        print(f"Sell on {date.date()} at {close_price:.2f}")
    
    # Calculate portfolio value
    portfolio_value.append(cash + positions * close_price)

# Convert portfolio value to a DataFrame for analysis
df['portfolio_value'] = portfolio_value

# Calculate performance metrics
total_return = (df['portfolio_value'].iloc[-1] - initial_cash) / initial_cash * 100
annualized_return = ((df['portfolio_value'].iloc[-1] / initial_cash) ** (252 / len(df)) - 1) * 100
max_drawdown = ((df['portfolio_value'].max() - df['portfolio_value'].min()) / df['portfolio_value'].max()) * 100

print(f"Total Return: {total_return:.2f}%")
print(f"Annualized Return: {annualized_return:.2f}%")
print(f"Max Drawdown: {max_drawdown:.2f}%")

# Plot the portfolio value over time
df['portfolio_value'].plot(title='Portfolio Value Over Time', figsize=(12, 8))
plt.xlabel('Date')
plt.ylabel('Portfolio Value (USD)')
plt.show()