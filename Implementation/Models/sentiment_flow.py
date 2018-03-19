import sys
import csv
sys.path.append("../Features/Sentiment_Flow/")
sys.path.append("../Parser/")

from flow_abstraction import *
from table_dump_parser import *

flow_2class_change_noloops = [abstract_2class, abstract_change, abstract_no_loops]
flow_2class_noloops_change = [abstract_2class, abstract_no_loops, abstract_change]
flow_change_noloops_2class = [abstract_change, abstract_no_loops, abstract_2class]
flow_noloops_2class_change = [abstract_no_loops, abstract_2class, abstract_change]
flow_2class_change         = [abstract_2class, abstract_change]
flow_change_2class_noloops = [abstract_change, abstract_2class, abstract_no_loops]
flow_noloops_change_2class = [abstract_no_loops, abstract_change, abstract_2class]
flow_2class_noloops        = [abstract_2class, abstract_no_loops]
flow_change_2class         = [abstract_change, abstract_2class]
flow_change_noloops		   = [abstract_change, abstract_no_loops]
flow_noloops_2class        = [abstract_no_loops, abstract_2class]
flow_noloops_change 	   = [abstract_no_loops, abstract_change]
flow_change 			   = [abstract_change]
flow_2class 			   = [abstract_2class]
flow_noloops               = [abstract_no_loops]
flow_original              = []

model_variants = [flow_2class_change_noloops, flow_2class_noloops_change, flow_change_noloops_2class, flow_noloops_2class_change, flow_2class_change, flow_change_2class_noloops, \
 				flow_noloops_change_2class, flow_2class_noloops, flow_change_2class, flow_change_noloops, flow_noloops_2class, flow_noloops_change, flow_change, flow_2class, \
 				flow_noloops, flow_original]

def get_sentiment_flow(reviews):
	''' gives the sentiment flow for a list of reviews depending on their star rating'''
	sentiment_flow = []
	for review in reviews:
		if review['star_rating'] is None : print review
		if float(review['star_rating']) >= 4:
			sentiment_flow.append(1)
		elif float(review['star_rating']) <= 2:
			sentiment_flow.append(-1)
		else:
			sentiment_flow.append(0)
	return sentiment_flow

def get_abstract_sentiment_flow(reviews, abstractions):
	''' returns the abstracted sentiment flow for given reviews and abstracted '''
	sentiment_flow = get_sentiment_flow(reviews)
	for abstraction in abstractions:
		sentiment_flow = abstraction(sentiment_flow)

	return sentiment_flow

def main():
	review_list = get_list_from_table_dump('/Users/yash/Downloads/output-2.txt', 6)
	product_reviews = []
	reviews = []
	for index, review in enumerate(review_list):
		if index == 0:
			reviews = [review]
		elif review_list[index]['product_id'] == review_list[index-1]['product_id']:
			reviews.append(review)
		else:
			product_reviews.append(reviews)
			reviews = [review]
	product_reviews.append(reviews)

	for index, variant in enumerate(model_variants):
		if index != 0: continue
		review_set = set()
		for reviews in product_reviews:
			review_set.add(tuple(get_abstract_sentiment_flow(reviews, variant)))
			

		if index == 0: print index, review_set
	

	return 0
if __name__ == "__main__":
	main()

