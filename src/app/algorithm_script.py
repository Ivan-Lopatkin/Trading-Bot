import os
import numpy as np
import pandas as pd

def preprocessing(file_path: str) -> pd.DataFrame:
	cols = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL']
	data = pd.read_csv(file_path, delimiter=';', header=None, names=cols)
    
	data.drop(['TIME'], axis=1, inplace=True)

	data.columns = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL']
	# 1. MACD
	data['EMA12'] = data['CLOSE'].ewm(span=12, adjust=False).mean()
	data['EMA26'] = data['CLOSE'].ewm(span=26, adjust=False).mean()
	data['MACD'] = data['EMA12'] - data['EMA26']
	data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

	# 2. RSI
	window_length = 14
	delta = data['CLOSE'].diff()
	gain = (delta.where(delta > 0, 0)).rolling(window=window_length).mean()
	loss = (-delta.where(delta < 0, 0)).rolling(window=window_length).mean()
	rs = gain / loss
	data['RSI'] = 100 - (100 / (1 + rs))

	# 3. Полосы Боллинджера
	data['Bollinger_Middle'] = data['CLOSE'].rolling(window=20).mean()
	data['Bollinger_Upper'] = data['Bollinger_Middle'] + 2 * data['CLOSE'].rolling(window=20).std()
	data['Bollinger_Lower'] = data['Bollinger_Middle'] - 2 * data['CLOSE'].rolling(window=20).std()

	return data

dataframes = os.listdir(path='data/')
dataframes  = [preprocessing(f'data/{df}') for df in dataframes]
