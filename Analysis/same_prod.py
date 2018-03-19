#!/usr/bin/python
import gensim
import sys
import heapq
from nltk.tokenize import word_tokenize
sys.path.append("../Data_Extraction/2.product_metadata/")
import products_db as my_db
import pickle

domains = ["IN", "UK", "COM", "CA"]

prod_table_name = "PROD"
desc_table_name = "DESC"

def get_features(raw_documents):
	'''Train model on the set of bow of titles'''
	gen_docs = [[w.lower() for w in word_tokenize(text)] for text in raw_documents]
	dictionary = gensim.corpora.Dictionary(gen_docs)
	corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
	tf_idf = gensim.models.TfidfModel(corpus)
	sims = gensim.similarities.Similarity('./', tf_idf[corpus], num_features=len(dictionary))
	return sims

def get_ids_reviews(dbs_all, domains):
	'''extracts ProductId, Title and Domain from the database'''
	raw_documents = []
	ids = []
	dns = []
	for i in range(0,len(dbs_all)):
		metadata_table = my_db.database_sqlite()
		metadata_table.create_connection(dbs_all[i])
		metadata_table.set_table_name(domains[i])
		#initialise a cursor in db
		metadata_table.initialise_cursor(prod_table_name)
		#get next row in db
		row = metadata_table.get_next_element()

		while row:
			ids.append(row[0])
			raw_documents.append(row[1])
			dns.append(domains[i])
			row = metadata_table.get_next_element()

		print "Retrieval completed for domain", domains[i]
	return ids, raw_documents, dns

def get_index_similarity_matrix(sims, dns):
	'''returns top most similar entries from different domain'''
	top_sim = []
	for crt, sim in enumerate(sims):
		L = [(i[0],i[1]) for i in sorted(enumerate(sim), key=lambda x:x[1], reverse=True)]
		top_sim.append([entry for entry in L if dns[crt]!=dns[entry[0]]][:500])
		# top_sim.append(L[:500])
	return top_sim

def main():
	cmd_arg = sys.argv
	root_dir = cmd_arg[1]
	database_dir = root_dir + "/data/phone_data"
	# database_dir = "/home/kushagra/Documents/BTP/my_work/data/phone_data"
	us_db = database_dir + "/us/products.db"
	in_db = database_dir + "/in/products.db"
	uk_db = database_dir + "/uk/products.db"
	ca_db = database_dir + "/ca/products.db"
	dbs = [in_db, uk_db, us_db, ca_db]

	ids, raw_documents, dns = get_ids_reviews(dbs, domains)
	print("Number of documents:",len(raw_documents))

	print "Getting Bag of Words -> tf-idf"
	sims = get_features(raw_documents)
	print "Tf-Idf Retrieved..."

	print "Getting similarities matrix...	"
	ans = get_index_similarity_matrix(sims, dns)
	print "Got Similarity Matrix"

	print "Getting top matches..."
	matches_f = [ (ids[crt],dns[crt],ids[elem[0][0]],dns[elem[0][0]], elem[0][1]) for crt, elem in enumerate(ans)]
	matches_sorted = sorted(matches_f, key=lambda x:x[4], reverse=True) 

	pickle.dump(matches_sorted, open("output_prod_matches","w"))
	print matches_sorted[:20]
	print "======================="
	print matches_sorted[5000:5020]
	print "======================="
	print matches_sorted[10000:10020]
	print "======================="
	print matches_sorted[15000:15020]
	print "======================="
	print matches_sorted[21000:21020]
	
	print len(matches_sorted)	

if __name__ == '__main__':
	main()