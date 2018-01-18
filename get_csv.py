# This file contains all library functions that relate to CSV interactions
from datetime import datetime
from bs4 import BeautifulSoup as soup
import json
import csv
import re
import dicttoxml
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# handles non-alphanumeric characters
def alphanumeric_name(name):
# Read from here on how to remove all non alphanumeric
# https://stackoverflow.com/questions/22520932/python-remove-all-non-alphabet-chars-from-string
	regex = re.compile('[^a-zA-Z]')
	name = regex.sub('', name)
	return name

# create panads data frame
def create_pandas_df(df_data):
	df = pd.DataFrame(df_data, columns = ['name', 'id', 'date', 'stars', 'text'])
	return df

# create csv for category
def create_category_csv(gen_category, categories, min_reviews):

	idList=[];
	name = [];
	#print "         searching for ids related to "+ gen_category 
	c=0
	#print categories
	for cat in categories:
		with open('business.csv') as bfile:
			reader = csv.reader(bfile);
			for row in reader:
				#print cat
				if (cat in row[2]):
					idList.append(row[0])
					name.append(row[1])

	if len(name) > min_reviews:
		print "         " + gen_category + " " + str(len(name)) + " matches found"
		csv_name = alphanumeric_name(gen_category)
		csvFile=csv.writer(open(csv_name+".csv","wb+"));
		csvFile.writerow(["name", "id", "date", "stars","text"]);

		dates=[]
		stars=[]
		count=0

		with open('reviews.csv') as rfile:
			rreader=csv.reader(rfile)
			for rrow in rreader:
				#print rrow
				if rrow[0] in idList:
					if count < len(name):
						csvFile.writerow([name[count], rrow[0],rrow[1],rrow[2],rrow[3]]);
						dates.append(rrow[1]);
						stars.append(rrow[2]);
						count+=1
					else:
						break
		return 1
	else:
		return 0

# get dataframe given csv
def get_category_csv(gen_category):

	idList=[];
	name = [];
	#print "         searching for ids related to "+ gen_category 
	c=0
	#print categories

	csv_name = alphanumeric_name(gen_category)
	cData = pd.read_csv(csv_name+".csv")

	# Create pandas data frame from csv
	df = create_pandas_df(cData)
	#print df['name']
	return df['name']

# create csv given company
def create_csv_company(bName, min_reviews):
	csv_name = alphanumeric_name(bName)
	csvFile=csv.writer(open(csv_name+".csv","wb+"));
	csvFile.writerow(["name", "id", "date", "stars","text"]);

	idList=[];
	name = [];
	print "         searching for ids related to that name " + bName,
	c=0
	with open('business.csv') as bfile:
		reader = csv.reader(bfile);
		for row in reader:
			#print row[1]
			temp = row[1].lower()
			if temp==bName.lower():
				idList.append(row[0])
				name.append(row[1])
				c+=1
	print c,"ids found."

	dates=[]
	stars=[]
	count=0
	if len(name) > min_reviews:
		with open('reviews.csv') as rfile:
			rreader=csv.reader(rfile)
			for rrow in rreader:
				#print rrow[0]
				if rrow[0] in idList:
					if count < len(name):
						csvFile.writerow([name[count], rrow[0],rrow[1],rrow[2],rrow[3]]);
						dates.append(rrow[1]);
						stars.append(rrow[2]);
						count+=1
					else:
						break
		return 1
	else:
		return 0










