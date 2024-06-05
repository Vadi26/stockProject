import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Step 1: Load Data
data = pd.read_csv('ohlc_data.csv')

# Step 2: Calculate Technical Indicators

# RSI
def calculate_rsi(data, window):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# MACD
def calculate_macd(data, fast=12, slow=26, signal=9):
    data['ema_fast'] = data['Close'].ewm(span=fast, adjust=False).mean()
    data['ema_slow'] = data['Close'].ewm(span=slow, adjust=False).mean()
    data['macd'] = data['ema_fast'] - data['ema_slow']
    data['macd_signal'] = data['macd'].ewm(span=signal, adjust=False).mean()
    data['macd_diff'] = data['macd'] - data['macd_signal']
    return data

# Bollinger Bands
def calculate_bollinger_bands(data, window=20):
    data['bb_middle'] = data['Close'].rolling(window=window).mean()
    data['bb_std'] = data['Close'].rolling(window=window).std()
    data['bb_upper'] = data['bb_middle'] + (data['bb_std'] * 2)
    data['bb_lower'] = data['bb_middle'] - (data['bb_std'] * 2)
    return data

# EMA
def calculate_ema(data, span):
    data[f'ema_{span}'] = data['Close'].ewm(span=span, adjust=False).mean()
    return data

# Supertrend
def calculate_supertrend(data, period=7, multiplier=3):
    data['hl2'] = (data['High'] + data['Low']) / 2
    data['atr'] = data['hl2'].rolling(window=period).std()
    data['upperband'] = data['hl2'] + (multiplier * data['atr'])
    data['lowerband'] = data['hl2'] - (multiplier * data['atr'])
    data['supertrend'] = np.where(data['Close'] > data['upperband'], data['lowerband'], data['upperband'])
    return data

# VWAP
def calculate_vwap(data):
    data['vwap'] = (data['Volume'] * (data['High'] + data['Low'] + data['Close']) / 3).cumsum() / data['Volume'].cumsum()
    return data

# OBV
def calculate_obv(data):
    obv = [0]
    for i in range(1, len(data)):
        if data['Close'][i] > data['Close'][i-1]:
            obv.append(obv[-1] + data['Volume'][i])
        elif data['Close'][i] < data['Close'][i-1]:
            obv.append(obv[-1] - data['Volume'][i])
        else:
            obv.append(obv[-1])
    data['obv'] = obv
    return data

# Doji Pattern
def identify_doji(data):
    data['doji'] = np.where((abs(data['Open'] - data['Close']) <= 0.1 * (data['High'] - data['Low'])), 1, 0)
    return data

# Hammer Pattern
def identify_hammer(data):
    data['hammer'] = np.where(
        (data['Close'] > data['Open']) &
        ((data['High'] - data['Close']) <= 0.1 * (data['High'] - data['Low'])) &
        ((data['Open'] - data['Low']) >= 2 * (data['High'] - data['Open'])), 1, 0)
    return data

# Morning Star and Evening Star Patterns (Simplified)
def identify_morning_star(data):
    data['morning_star'] = np.where(
        (data['Close'].shift(2) < data['Open'].shift(2)) &
        (abs(data['Close'].shift(1) - data['Open'].shift(1)) < (data['High'].shift(1) - data['Low'].shift(1)) * 0.1) &
        (data['Close'] > data['Open']), 1, 0)
    return data

def identify_evening_star(data):
    data['evening_star'] = np.where(
        (data['Close'].shift(2) > data['Open'].shift(2)) &
        (abs(data['Close'].shift(1) - data['Open'].shift(1)) < (data['High'].shift(1) - data['Low'].shift(1)) * 0.1) &
        (data['Close'] < data['Open']), 1, 0)
    return data

# Calculate all indicators
data['RSI'] = calculate_rsi(data, window=14)
data = calculate_macd(data)
data = calculate_bollinger_bands(data)
data = calculate_ema(data, span=20)
data = calculate_ema(data, span=50)
data = calculate_supertrend(data)
data = calculate_vwap(data)
data = calculate_obv(data)
data = identify_doji(data)
data = identify_hammer(data)
data = identify_morning_star(data)
data = identify_evening_star(data)

# Step 3: Generate Buy/Sell Signals

def calculate_pattern_score(data):
    patterns = ['doji', 'hammer', 'morning_star', 'evening_star']
    data['pattern_score'] = data[patterns].sum(axis=1)
    return data

def calculate_indicator_volume_strategy(data):
    # Example volume strategy score
    data['indicator_volume_score'] = np.where(data['obv'] > data['obv'].shift(1), 1, -1)
    return data

def calculate_macd_rsi_strategy(data):
    data['macd_rsi_score'] = np.where((data['macd_diff'] > 0) & (data['RSI'] < 30), 1,
                                      np.where((data['macd_diff'] < 0) & (data['RSI'] > 70), -1, 0))
    return data

def calculate_all_indicators_strategy(data):
    indicators = ['RSI', 'macd_diff', 'bb_upper', 'bb_lower', 'ema_20', 'ema_50', 'supertrend', 'vwap']
    data['all_indicators_score'] = data[indicators].apply(lambda row: (row > row.mean()).sum() - (row < row.mean()).sum(), axis=1)
    return data

def calculate_macd_ema_strategy(data):
    data['macd_ema_score'] = np.where((data['macd'] > data[f'ema_20']) & (data['macd'] > data[f'ema_50']), 1, -1)
    return data

data = calculate_pattern_score(data)
data = calculate_indicator_volume_strategy(data)
data = calculate_macd_rsi_strategy(data)
data = calculate_all_indicators_strategy(data)
data = calculate_macd_ema_strategy(data)

def generate_signals(data):
    weights = {
        'pattern_score': 0.4,
        'indicator_volume_score': 0.2,
        'macd_rsi_score': 0.1,
        'all_indicators_score': 0.2,
        'macd_ema_score': 0.1
    }

    data['signal_score'] = (data['pattern_score'] * weights['pattern_score'] +
                            data['indicator_volume_score'] * weights['indicator_volume_score'] +
                            data['macd_rsi_score'] * weights['macd_rsi_score'] +
                            data['all_indicators_score'] * weights['all_indicators_score'] +
                            data['macd_ema_score'] * weights['macd_ema_score'])

    data['Signal'] = np.where(data['signal_score'] > 0, 1, np.where(data['signal_score'] < 0, -1, 0))
    return data

data = generate_signals(data)

# Step 4: Prepare Features and Labels
features = ['RSI', 'macd', 'macd_signal', 'macd_diff', 'bb_upper', 'bb_lower', 'bb_middle', 'ema_20', 'ema_50', 'supertrend', 'vwap', 'obv', 'doji', 'hammer', 'morning_star', 'evening_star', 'pattern_score', 'indicator_volume_score', 'macd_rsi_score', 'all_indicators_score', 'macd_ema_score']
X = data[features].dropna()
y = data['Signal'].dropna()

# Ensure alignment
X, y = X.align(y, join='inner', axis=0)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size

















6
# Load the trained model
model = joblib.load('trading_signal_model.pkl')

# Make predictions on new data
new_data = pd.read_csv('new_ohlc_data.csv')

# Ensure the new data has the same features
# Recalculate indicators for new data as needed (you can define functions again or refactor them into a separate module)
new_data['RSI'] = calculate_rsi(new_data, window=14)
new_data = calculate_macd(new_data)
new_data = calculate_bollinger_bands(new_data)
new_data = calculate_ema(new_data, span=20)
new_data = calculate_ema(new_data, span=50)
new_data = calculate_supertrend(new_data)
new_data = calculate_vwap(new_data)
new_data = calculate_obv(new_data)
new_data = identify_doji(new_data)
new_data = identify_hammer(new_data)
new_data = identify_morning_star(new_data)
new_data = identify_evening_star(new_data)

new_data = calculate_pattern_score(new_data)
new_data = calculate_indicator_volume_strategy(new_data)
new_data = calculate_macd_rsi_strategy(new_data)
new_data = calculate_all_indicators_strategy(new_data)
new_data = calculate_macd_ema_strategy(new_data)

# Prepare new features
new_X = new_data[features].dropna()

# Make predictions
new_data['Predicted_Signal'] = model.predict(new_X)

# Save the predictions
new_data.to_csv('new_ohlc_data_with_signals.csv', index=False)