# This file contains all library functions that relate to pre-processing data

from datetime import datetime
from bs4 import BeautifulSoup as soup
import json
import csv
import dicttoxml
from matplotlib import pyplot as plt
import string
import re
import get_csv

# This function converts json files to csv for easier readibility
def jsn_to_csv_cleanup(business_json_path, review_json_path):

	print "     Converting business.json to csv"
	print "         extracting id,name,reviewCount ...",

	csvFile= csv.writer(open("business.csv", "wb+"));
	csvFile.writerow(["id", "name", "category", "reviewCount"]);
	counter=0;
	#xml="";
	#we want to extranct business id,name,review count
	with open(business_json_path) as f:
	    for line in f:
	        counter+=1;
	        content = json.loads(line)
	        #xml+=(dicttoxml.dicttoxml(content));
	        csvFile.writerow([content["business_id"], content["name"].encode('utf-8'), content["categories"], content["review_count"]]);
	        #print counter
	print "done"

	print "     Converting reviews to csv"
	print "         extracting businessId,date,stars,text ...",
	csvFile= csv.writer(open("reviews.csv", "wb+"));
	csvFile.writerow(["id", "name", "date", "stars","text"]);
	counter=0;
	#xml="";
	#we want to extranct business id,date,stars and text
	with open(review_json_path) as f:
	    for line in f:
	        counter+=1;
	        content = json.loads(line)
	        #xml+=(dicttoxml.dicttoxml(content));
	        csvFile.writerow([content["business_id"], content["date"], content["stars"],content["text"].encode('utf-8')]);
	       # print counter
	print "done"

# This function creates a csv for all categories that fall under a parent category
# Such as Restaurant contains Mexican, Italian, Chinese, etc.
def find_relevant_categories(parent_category, category_txt):

	print "     Looking for all " + parent_category + "in categories.json ..."
	category_list = []
	category_list = json.load(open('categories.json'))

	print "     Creating " + category_txt
	category_txt = category_txt + ".txt"
	fileobj  = open(category_txt, "w")

	print "     Creating all relevant CSVs in category " + parent_category
	for i in range(len(category_list)):
		#print category_list[i]["parents"]
		if category_list[i]['parents'] == [parent_category]:
			s = category_list[i]['title']
			title_csv = string.replace(s, '/', '_')
			output = get_csv.create_category_csv(title_csv,[s], 1000)
			if output:
				fileobj.write(s + "\n")
			#print category_list[i]['title']
	fileobj.close()


