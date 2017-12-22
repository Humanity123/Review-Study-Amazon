from sklearn.svm import SVR
from sklearn import cross_validation
from sklearn.metrics import mean_squared_error
import os
from random import shuffle
import sys
import pickle as pkl
sys.path.append("../Features/Linguistic")
sys.path.append("../Parser")
sys.path.append("../../Data_Extraction/3.reviews/")

import reviews_db as my_db

from STR import *
from UGR import *
from GALC import *
from LIWC import *
from INQUIRER import *

from DBParser import *

cmd_arg = sys.argv
data_dir = cmd_arg[1]

STR_features_extractor = [get_STR_features]
UGR_features_extractor = [get_UGR_features]
GALC_features_extractor = [get_GALC_features]
LIWC_feature_extractor = [ get_LIWC_features]
INQUIRER_feature_extractor = [get_INQUIRER_features]
SEMANTIC_features_extractor = [get_GALC_features, get_LIWC_features, get_INQUIRER_features]
ALL_features_extractor = [get_STR_features, get_UGR_features, get_GALC_features, get_LIWC_features, get_INQUIRER_features]

crt = os.path.join(os.getcwd(), "../../../LinguisticData/featureDictionaries/")

GALC_dic_loc = os.path.join(crt+"galc.csv")
INQUIRER_dic_loc = os.path.join(crt+"inquirerbasic.csv")
LIWC_dic_loc = os.path.join(crt+"LIWC2007.dic")
Start_Line = 66

def get_features(reviews, feature_extractors):
	''' function to get the feature vector of all the reviews
	according to the features given in the feature extractors, the features are concatenated to make
	a single feature vector for a review'''
	feature_vectors = None
	for feature_extractor in feature_extractors:
		if feature_vectors is None:
			feature_vectors = feature_extractor(reviews)
		else:
			feature_vectors = np.concatenate((feature_vectors, feature_extractor(reviews)), axis = 1)

	return feature_vectors

def main():
	direc_in = data_dir + "/in/reviews.db"
	direc_ca = data_dir + "/ca/reviews.db"
	direc_us = data_dir + "/us/reviews.db"
	direc_uk = data_dir + "/uk/reviews.db"

	dir_list = [direc_in, direc_us, direc_uk, direc_ca]
	domains = ["IN", "COM", "UK", "CA"]
	# test_cases = [STR_features_extractor, UGR_features_extractor, GALC_features_extractor, LIWC_feature_extractor, INQUIRER_feature_extractor, SEMANTIC_features_extractor, ALL_features_extractor]
	test_cases = [STR_features_extractor, UGR_features_extractor, GALC_features_extractor, LIWC_feature_extractor, INQUIRER_feature_extractor]

	get_GALC_dic(GALC_dic_loc)
	get_INQUIRER_dic(INQUIRER_dic_loc)
	get_LIWC_dic(LIWC_dic_loc, Start_Line)
	result_all = [[], [], [], []]

	
	for i in range(0,len(dir_list)):
		c_dir = dir_list[i]
		c_domain = domains[i]
		print c_domain ,"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
		rev_data = get_ids_reviews(c_dir, c_domain)
		for test_case in test_cases:
			result_all[i].append(get_features(rev_data[1][:500],test_case))
	
	pkl.dump(result_all, open("Linguistics.pkl","w"))
if __name__ == "__main__":
	main()