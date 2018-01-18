# This is the main script used to data mine
import test_lib
import ts_lib
import preprocessing
import textMining
import review_plotter
print ""
print "Data Mining Project: 'YTrend: Why did you review me like that?'" 
print "Jasmine Kim, Shirin Haji Amin Shirazi, Bailey Herms"
print "Fall 2017 Quarter" 
print "CS 235"
print ""

print "Performing data pre-processing..." 

# Set this flag if this if the first time you're running through the script
first_time_flag = 0

if first_time_flag:
	print ""
	# JSON -> CSV and business ID mapping data pre-processing
	preprocessing.jsn_to_csv_cleanup('../yelp_ds/business.json', '../yelp_ds/review.json')

	print ""
	# Specify parent category you're interested in
	# In this case, restaurants
	preprocessing.find_relevant_categories('restaurants', "restaurants_category")

# Note, third arg is NOP

# First test runs comparison for all restaurant categories against each other
# Uses rolling window mean and DTW
test_lib.run_test(1, "restaurants_category", 0)

# Second test runs comparison for all restaurant categories against each other
# Uses rolling window mean, DTW, time normalization using quartiles, and Z normalization
test_lib.run_test(2, "restaurants_category", 0)

# Third test runs comparison for Chipotle against all other restaurant categories
test_lib.run_test(3, "Chipotle Mexican Grill", "restaurants_category")

# Fourth test runs comparison for Chipotle against all other restaurant that are of Mexican category
test_lib.run_test(4, "Chipotle Mexican Grill", "Mexican")

# Plot for Chipotle
#review_plotter.review_plotter("Chipotle Mexican Grill")
