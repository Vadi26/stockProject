import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('data.csv')

# Parameters
initial_capital = 100000  # Starting with 100,000 units of currency
position_size = 100       # Number of shares per trade
capital = initial_capital
shares = 0
portfolio_value = []

# Simulate trades
for i in range(len(df)):
    signal = df.loc[i, 'signals']
    close_price = df.loc[i, 'Close']
    
    if signal == 'buy':
        shares += position_size
        capital -= position_size * close_price
    elif signal == 'sell' and shares > 0:
        capital += shares * close_price
        shares = 0
    
    # Calculate the current portfolio value
    current_portfolio_value = capital + shares * close_price
    portfolio_value.append(current_portfolio_value)

# Add portfolio value to the dataframe
df['Portfolio_Value'] = portfolio_value

# Calculate performance metrics
df['Returns'] = df['Portfolio_Value'].pct_change()
total_return = (df['Portfolio_Value'].iloc[-1] / initial_capital) - 1
max_drawdown = (df['Portfolio_Value'].cummax() - df['Portfolio_Value']).max()
sharpe_ratio = df['Returns'].mean() / df['Returns'].std() * np.sqrt(252)  # Assuming daily returns

print(f'Total Return: {total_return * 100:.2f}%')
print(f'Maximum Drawdown: {max_drawdown:.2f}')
print(f'Sharpe Ratio: {sharpe_ratio:.2f}')

# Save the backtest results
df.to_csv('backtest_results.csv', index=False)