import sys
sys.path.append("../../Data_Extraction/3.reviews/")
import reviews_db as my_db
def get_ids_reviews(dbPath, domain):
	'''extracts ProductId, Title and Domain from the database'''
	raw_documents = []
	ids = []
	metadata_table = my_db.database_sqlite()
	metadata_table.create_connection(dbPath)
	metadata_table.set_table_name(domain+"_REV_com")
	#initialise a cursor in db
	metadata_table.initialise_cursor()
	#get next row in db
	row = metadata_table.get_next_element()

	while row:
		ids.append(row[0])
		raw_documents.append(row[4])
		row = metadata_table.get_next_element()

	print "Retrieval completed for domain", domain
	return ids, raw_documents
