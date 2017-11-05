#!/usr/bin/python
import reviews_db as my_db


#stores reviews in the current page and returns the link to NEXT page
def store_reviews_in_page(database_dir, domain, file_out):
	database_path_reviews = database_dir + "/reviews.db"
	rev_table_name = domain+"_REV"
	#create connection to the database
	rev_table = my_db.database_sqlite()
	rev_table.create_connection(database_path_reviews)
	rev_table.set_table_name(rev_table_name)
	try:
		print "dumping reviews in ", database_path_reviews
		rev_table.dump(file_out)
	except Exception as e:
		print e

def main():
	store_reviews_in_page(".", "COM", "US_rev")

if __name__ == '__main__':
	main()
