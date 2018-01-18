# This file contains all library functions that are data mining tests called by test_script
import json
import dicttoxml
import get_csv
import review_plotter
import re
import string
import numpy as np
import ts_lib

def run_test(test_id, arg1, arg2):
	test_function = { 1: run_test_1,
					2: run_test_2,
					3: run_test_3,
					4: run_test_4,
	}
	test_function[test_id](arg1, arg2)


# This test runs category vs category using DTW
def run_test_1(category_txt, nop):

	found_category_list = []
	output_txt = category_txt + "_output_1.txt"
	category_txt = category_txt + ".txt"

	fileobj = open(category_txt)
	for line in iter(fileobj):
		line = string.replace(line, '\n', '')
		found_category_list.append(line)
	fileobj.close()
	
	print found_category_list

	fileobj = open(output_txt, "w")

	for i in range(len(found_category_list)):
		gen_category_1 = found_category_list[i]
		for j in range(len(found_category_list)):
			gen_category_2 = found_category_list[j]
			print gen_category_1
			print gen_category_2
			dtw_dist = ts_lib.pattern_finder(gen_category_1, gen_category_2)
			comparison = gen_category_1 + "\t" + gen_category_2 + "\t" + str(dtw_dist)
			fileobj.write(comparison + "\n")
	fileobj.close()


# This test runs category vs category using time normalization and DTW
def run_test_2(category_txt, nop):
	found_category_list = []
	output_txt = category_txt + "_output_2.txt"
	category_txt = category_txt + ".txt"

	fileobj = open(category_txt)
	for line in iter(fileobj):
		line = string.replace(line, '\n', '')
		found_category_list.append(line)
	fileobj.close()
	
	print found_category_list

	fileobj = open(output_txt, "w")

	# loop through every 
	for i in range(len(found_category_list)):
		gen_category_1 = found_category_list[i]
		for j in range(len(found_category_list)):
			gen_category_2 = found_category_list[j]
			print gen_category_1
			print gen_category_2
			dtw_dist = ts_lib.pattern_finder_quartile(gen_category_1, gen_category_2)
			comparison = gen_category_1 + "\t" + gen_category_2 + "\t" + str(dtw_dist)
			fileobj.write(comparison + "\n")
	fileobj.close()

# This test runs company vs categories using time normalization, z normalization and DTW
def run_test_3(bName, category_txt):
	found_category_list = []
	output_txt = category_txt + "_output_3.txt"
	category_txt = category_txt + ".txt"

	valid = get_csv.create_csv_company(bName, 0)
	if not valid:
		print "This company doesn't have enough info."
		return 0
	gen_category_1 = bName

	fileobj = open(category_txt)
	for line in iter(fileobj):
		line = string.replace(line, '\n', '')
		found_category_list.append(line)
	fileobj.close()
	fileobj = open(output_txt, "w")
	for j in range(len(found_category_list)):
		gen_category_2 = found_category_list[j]
		print gen_category_1
		print gen_category_2
		dtw_dist = ts_lib.pattern_finder_quartile(gen_category_1, gen_category_2)
		comparison = gen_category_1 + "\t" + gen_category_2 + "\t" + str(dtw_dist)
		fileobj.write(comparison + "\n")
	fileobj.close()
	#review_plotter.review_plotter(bName)

# This test runs company vs company in a specific category using time normalization, z normalization and DTW
def run_test_4(business_1, category_name):
	found_category_list = []
	ran_list = []
	output_name = category_name + "_output_4.txt"

	found_category_list = get_csv.get_category_csv(category_name)
	fileobj = open(output_name, "w")

	for j in range(len(found_category_list)):
		business_2 = found_category_list[j]
		business_2 = business_2.lower()
		if business_2 not in ran_list:
			found_2 = get_csv.create_csv_company(business_2, 10)
			if found_2:
				print business_1
				print business_2
				dtw_dist = ts_lib.pattern_finder_quartile(business_1, business_2)
				comparison = business_1 + "\t" + business_2 + "\t" + str(dtw_dist)
				fileobj.write(comparison + "\n")
			ran_list.append(business_2)
			#print ran_list
	fileobj.close()
	#review_plotter.review_plotter(bName)


