#!/usr/bin/python
import gensim
import pickle
import sys
import heapq
from nltk.tokenize import word_tokenize
sys.path.append("../Data_Extraction/2.product_metadata/")
import products_db as my_db


'''Generates the matching products on amazon India domain matching with the products on 91mobiles.com'''

cmd_arg = sys.argv
root_dir = cmd_arg[1]
database_dir = root_dir + "/data/phone_data"
us_db = database_dir + "/us/products.db"
in_db = database_dir + "/in/products.db"
uk_db = database_dir + "/uk/products.db"

dbs = [in_db]
domains = ["IN"]

prod_table_name = "PROD"
desc_table_name = "DESC"

def get_features(raw_documents):
	'''Train model on the set of bow of titles'''
	gen_docs = [[w.lower() for w in word_tokenize(text)] for text in raw_documents]
	dictionary = gensim.corpora.Dictionary(gen_docs)
	corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
	tf_idf = gensim.models.TfidfModel(corpus)
	sims = gensim.similarities.Similarity('/home/kushagra/Documents/BTP/my_work/Review-Study-Amazon/Analysis/', tf_idf[corpus], num_features=len(dictionary))
	return sims

def get_ids_reviews():
	'''extracts ProductId, Title and Domain from the database'''
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

	ids, raw_documents, dns = get_ids_reviews()
	
	#update raw_documents using products from website
	a = pickle.load(open('features.pickle','r'))
	print len(a)
	prd_id=0
	for item in a:
		raw_documents.append(item['model'])
		ids.append(item['model']+"_91_"+str(prd_id))
		dns.append('91')
		prd_id+=1

	print("Number of documents:",len(raw_documents))
	
	print "Getting Bag of Words -> tf-idf"
	sims = get_features(raw_documents)
	print "Tf-Idf Retrieved..."
	
	print "Getting similarities matrix...	"
	ans = get_index_similarity_matrix(sims, dns)
	print "Got Similarity Matrix"
	
	print "Getting top matches..."
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

	'''Printing the matches obtained for the products on teh website'''
	for match in matches_sorted:
		if '_91_' in match[0]:
			b = match[0].split('_')
			index = int(b[2])
			print index
			a[index]['match'] = match[1]
	pickle.dump(a,open('feature2.pickle','w'))
if __name__ == '__main__':
	main()