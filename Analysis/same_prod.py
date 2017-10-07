#!/usr/bin/python
import gensim
import sys
import heapq
from nltk.tokenize import word_tokenize
sys.path.append("../Data_Extraction/2.product_metadata/")
import products_db as my_db

# cmd_arg = sys.argv
# database_dir = cmd_arg[1]
database_dir = "/home/kushagra/Documents/BTP/my_work/data"
us_db = database_dir + "/us/products.db"
in_db = database_dir + "/in/products.db"
uk_db = database_dir + "/uk/products.db"

dbs = [in_db, us_db]
domains = ["IN", "COM"]

prod_table_name = "PROD"
desc_table_name = "DESC"

def get_features(raw_documents):
	gen_docs = [[w.lower() for w in word_tokenize(text)] for text in raw_documents]
	dictionary = gensim.corpora.Dictionary(gen_docs)
	corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
	tf_idf = gensim.models.TfidfModel(corpus)
	sims = gensim.similarities.Similarity('/home/kushagra/Documents/BTP/my_work/Review-Study-Amazon/Analysis/', tf_idf[corpus], num_features=len(dictionary))
	return sims
def get_ids_reviews():
	raw_documents = []
	ids = []
	dns = []
	for i in range(0,len(dbs)):
		metadata_table = my_db.database_sqlite()
		metadata_table.create_connection(dbs[i])
		metadata_table.set_table_name(domains[i])
		#initialise a cursor in db
		metadata_table.initialise_cursor(prod_table_name)
		#get next row in db
		row = metadata_table.get_next_element()

		while row:
			ids.append(row[0])
			# desc_table = my_db.database_sqlite()
			# desc_table.create_connection(dbs[i])
			# desc_table.set_table_name(domains[i])
			# #initialise a cursor in db
			# desc_table.initialise_cursor_description(desc_table_name,row[0])

			# descs = ""
			# row_i = desc_table.get_next_element()
			# while row_i:
			# 	descs = descs + " " + row_i[1]
			# 	row_i = desc_table.get_next_element()

			raw_documents.append(row[1])
			
			dns.append(domains[i])
			row = metadata_table.get_next_element()

		print "Retrieval completed for domain", domains[i]
	return ids, raw_documents, dns

def get_index_similarity_matrix(sims, dns):
	top_sim = []
	for crt, sim in enumerate(sims):
		L = [(i[0],i[1]) for i in sorted(enumerate(sim), key=lambda x:x[1], reverse=True)]
		top_sim.append([entry for entry in L if dns[crt]!=dns[entry[0]]][:500])
		# top_sim.append(L[:500])
	return top_sim


def main():
	ids, raw_documents, dns = get_ids_reviews()
	print("Number of documents:",len(raw_documents))
	print "Getting Bag of Words -> tf-idf"
	sims = get_features(raw_documents)
	print "Tf-Idf Retrieved..."
	print "Getting similarities matrix...	"
	ans = get_index_similarity_matrix(sims, dns)
	print "Got Similarity Matrix"
	print "Getting top matches..."
	# Matches = [(ids[crt],[(ids[index_sim[0]], index_sim[1]) for index_sim in sims if dns[crt]!=dns[index_sim[0]]][:1]) for crt ,sims in enumerate(ans[0:])]
	# print ids[sim[0][0]], sim[0][1],"--", ids[sim[1][0]], sim[1][1], "--", ids[sim[2][0]], sim[2][1],"--", ids[sim[3][0]], sim[3][1]
	matches_f = [ (ids[crt],ids[elem[0][0]], elem[0][1])  for crt, elem in enumerate(ans)]
	matches_sorted = sorted(matches_f, key=lambda x:x[2], reverse=True) 
	print matches_sorted[:20]
	print "======================="
	print matches_sorted[200:220]
	print "===============0========"
	print matches_sorted[400:420]
	print "======================="
	print matches_sorted[600:620]
	print "======================="
	print matches_sorted[800:820]
	print len(matches_sorted)

if __name__ == '__main__':
	main()