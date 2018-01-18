# This file contains all library functions that relate to plotting
from matplotlib import pyplot as plt
import pandas as pd
import math
import numpy as np
import csv
import get_csv
# Download this https://pypi.python.org/pypi/fastdtw
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

# This function plots for the business name provided
def review_plotter(bName):

	# Read in csv file for Pandas
	bName = get_csv.alphanumeric_name(bName)
	bName_csv = bName + ".csv"
	print bName_csv
	bData = pd.read_csv(bName_csv)

	# Create pandas data frame from csv
	df = pd.DataFrame(bData, columns = ['id', 'date', 'stars', 'text'])

	# The following does some time series clean up
	# https://stackoverflow.com/questions/44128600/how-should-i-handle-duplicate-times-in-time-series-data-with-pandas
	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
	df['date'] = df['date'] + pd.to_timedelta(df.groupby('date').cumcount(), unit='h')
	df =  df.sort_values(by=['date'])
	new_df = df.set_index('date')

	# Perform rolling average
	if len(new_df) > 100:
		ts = pd.Series.rolling(new_df['stars'], window=100).mean()
	else:
		ts = pd.Series.rolling(new_df['stars'], window=1).mean()

	# Plot
	ts.plot(style='b-', x_compat=True)

	f1 = plt.figure(1)
	plt.title(bName + " (Smoothing)")
	f1.show()
	plt.savefig(bName+"1.png")

	# Scatter Plot
	f2 = plt.figure(2)
	ts.plot(style='bo', x_compat=True)
	plt.title(bName + "(Scatter, Smoothing)")
	f2.show()
	plt.savefig(bName+"2.png")


