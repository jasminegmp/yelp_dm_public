# This file contains all library functions that pertain to time series data mining
from matplotlib import pyplot as plt
import pandas as pd
import math
import numpy as np
import get_csv

# Download this https://pypi.python.org/pypi/fastdtw
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

# Creates pandas data frame
def create_pandas_df(df_data):
	df = pd.DataFrame(df_data, columns = ['id', 'date', 'stars', 'text'])
	return df

# Preprocesses time series because of challenges we ran into
# First, multiple reviews on same date. Solved it by separating each data point that had same
# timestamp by an hour
# Second, review range was too discrete. Solved it by performing a rolling average
def preprocess_ts(df):

	# https://stackoverflow.com/questions/44128600/how-should-i-handle-duplicate-times-in-time-series-data-with-pandas
	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
	df['date'] = df['date'] + pd.to_timedelta(df.groupby('date').cumcount(), unit='h')
	df =  df.sort_values(by=['date'])
	new_df = df.set_index('date')

	# Perform rolling average
	if len(df) > 100:
		ts = pd.Series.rolling(new_df['stars'], window=100).mean()
	else:
		ts = pd.Series.rolling(new_df['stars'], window=1).mean()

	# Remove any NA datapoints
	ts = ts.dropna()
	#print ts
	#print new_df
	return ts, new_df

# Performs DTW provided two time series
def perform_dtw(ts_1, ts_2):

	# Following is done because DTW requires same length time series
	compare_len = min(len(ts_1),len(ts_2))

	x = ts_1.iloc[-compare_len:].values
	y = ts_2.iloc[-compare_len:].values

	dtw_dist, path = fastdtw(x,y, dist=euclidean)

	print dtw_dist

	return dtw_dist

# Performs DTW provided two time series that are time normalized using quartiles
def perform_quartile_dtw(ts_1, ts_2):

	# Following is done because DTW requires same length time series
	compare_len = min(len(ts_1),len(ts_2))

	x = ts_1[-compare_len:]
	y = ts_2[-compare_len:]

	dtw_dist, path = fastdtw(ts_1, ts_2, dist=euclidean)

	print dtw_dist

	return dtw_dist

# Normalizes time series such that x axis is normalized using quartiles
def normalize_quartile(ts, new_df):
	ts_time = []
	ts_value = []
	for i in range(len(ts)):
		temp_quartile = float(i)/len(new_df)
		ts_time.append(temp_quartile)
		temp_val = ts.ix[i]
		ts_value.append(temp_val)
	return ts_time, ts_value

# Perform z-normalization (from 0 to 1)
def z_normalization(ts_time, ts_val,):
	max = 1
	min = 0
	znorm_ts_val = []
	for i in range(len(ts_val)):
		znorm_ts_val.append((ts_time[i] - min)/(max - min))
	return znorm_ts_val

# Perform DTW
def pattern_finder(bName_1, bName_2):
	bName1_csv = get_csv.alphanumeric_name(bName_1)
	bName2_csv = get_csv.alphanumeric_name(bName_2)
	bName1_csv = bName1_csv + ".csv"
	bName2_csv = bName2_csv + ".csv"

	bData_1 = pd.read_csv(bName1_csv)
	bData_2 = pd.read_csv(bName2_csv)

	# Create pandas data frame from csv
	df_1 = create_pandas_df(bData_1)
	df_2 = create_pandas_df(bData_2)

	# Perform some preprocessing of reviews into a comprehendible time series
	ts_1, newdf1 = preprocess_ts(df_1)
	ts_2, newdf2 = preprocess_ts(df_2)

	dtw_dist = perform_dtw(ts_1, ts_2)

	return dtw_dist

# Perform DTW after Z normalization and time normalization
def pattern_finder_quartile(bName_1, bName_2):
	bName1_csv = get_csv.alphanumeric_name(bName_1)
	bName2_csv = get_csv.alphanumeric_name(bName_2)
	bName1_csv = bName1_csv + ".csv"
	bName2_csv = bName2_csv + ".csv"

	bData_1 = pd.read_csv(bName1_csv)
	bData_2 = pd.read_csv(bName2_csv)

	# Create pandas data frame from csv
	df_1 = create_pandas_df(bData_1)
	df_2 = create_pandas_df(bData_2)

	# Perform some preprocessing of reviews into a comprehendible time series
	ts_1, newdf1 = preprocess_ts(df_1)
	ts_2, newdf2 = preprocess_ts(df_2)

	ts_time_1, ts_value_1 = normalize_quartile(ts_1, newdf1)
	ts_time_2, ts_value_2 = normalize_quartile(ts_2, newdf2)

	z_norm_ts_1 = z_normalization(ts_time_1, ts_value_1)
	z_norm_ts_2 = z_normalization(ts_time_2, ts_value_2)

	dtw_dist = perform_quartile_dtw(z_norm_ts_1, z_norm_ts_2)

	return dtw_dist


