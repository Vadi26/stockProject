import pandas as pd

def backtest_signals(csv_file):
    # Load the data
    data = pd.read_csv(csv_file)
    
    # Add columns to keep track of correct signals
    data['correct_signal'] = 0

    for i in range(len(data)):
        if data['signal'].iloc[i] == 1:  # Buy signal
            buy_price = data['close'].iloc[i]
            for j in range(1, 31):
                if i + j >= len(data):
                    break
                if data['signal'].iloc[i + j] == -1:  # Sell signal within 30 candles
                    sell_price = data['close'].iloc[i + j]
                    if sell_price > buy_price:
                        data.at[i, 'correct_signal'] = 1
                        data.at[i + j, 'correct_signal'] = 1
                    break
                if j == 30:  # Reached the end of the 30-candle window
                    future_price = data['close'].iloc[i + j - 1]
                    if future_price > buy_price:
                        data.at[i, 'correct_signal'] = 1

        elif data['signal'].iloc[i] == -1:  # Sell signal
            sell_price = data['close'].iloc[i]
            for j in range(1, 31):
                if i + j >= len(data):
                    break
                if data['signal'].iloc[i + j] == 1:  # Buy signal within 30 candles
                    buy_price = data['close'].iloc[i + j]
                    if sell_price > buy_price:
                        data.at[i, 'correct_signal'] = 1
                        data.at[i + j, 'correct_signal'] = 1
                    break

    # Save the results to a new CSV file
    data.to_csv('backtest_results.csv', index=False)
    print('Backtesting completed. Results saved to backtest_results.csv')

# Example usage
backtest_signals('ohlc_data.csv')