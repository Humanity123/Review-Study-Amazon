#!/usr/bin/python

import sqlite3
import json
from sqlite3 import Error


#class to handle table in a database
class database_sqlite:
	def __init__(self):
		self.conn = ""
		self.table = "LINKS"
		self.iter_ = ""
	def __del__(self):
		self.conn.close()
	def create_connection(self,db_file):
	    try:
	        self.conn = sqlite3.connect(db_file)
	    except Exception as e:
	        print "Error in Database Creation!", e
	 
	    return None

	def insert_link(self,id_p,link):
		cur = self.conn.cursor()
		try:
			cur.execute("INSERT INTO %s VALUES (?,?)" % (self.table),(id_p,link,))
			return 1
		except Exception as e:
			print e

		return 0

	def initialise_cursor(self):
		self.iter_ = self.conn.execute("SELECT * from %s" % (self.table))

	def get_next_element(self):
		return self.iter_.fetchone()

	def insert_review(self,RevId, ProductID, Rev_Date, Rev_Votes, Review_Data, Rev_Stars ):
		try:
			self.conn.execute("INSERT INTO %s VALUES (?,?,?,?,?,?)" % (self.table),(RevId, ProductID, Rev_Date, Rev_Votes, Review_Data, Rev_Stars,))
			return 1
		except Exception as e:
			print e

		return 0

	def create_table(self):
		try:
			self.conn.execute("CREATE TABLE %s (Prod_ID TEXT PRIMARY KEY      NOT NULL, LINK TEXT NOT NULL);" % (self.table))
			return 1
		except Exception as e:
			print e

		return 0
	def create_table_reviews(self):
		try:
			self.conn.execute("CREATE TABLE %s (Rev_ID TEXT PRIMARY KEY      NOT NULL, ProductID TEXT NOT NULL, Rev_Date DATE , Rev_Votes INT , Review_Data TEXT, Rev_Stars REAL);" % (self.table))
			return 1
		except Exception as e:
			print e
		return 0
		
	def set_table_name(self,table_name):
		self.table = table_name

	def is_review_present(self,prod_id):
		return self.conn.execute("SELECT count(ProductID) from %s WHERE ProductID=\"%s\";" % (self.table,prod_id))

	def get_count(self):
		# LINKS = "LINKS"
		cursor = self.conn.execute("SELECT count(*) from %s" % (self.table))
		for row in cursor:
			print row[0]
			return row[0]

	def print_all(self):
		cursor = self.conn.execute("SELECT * from %s" % (self.table))
		for row in cursor:
			for data in row:
				print data

		print "Operation done successfully";


	def save_changes(self):
		try:
			self.conn.commit()
		except Exception as e:
			print e
	def discard_changes(self):
		self.conn.rollback();
	def dump(self, file):
		fp = open(file+".txt", "a")
		output_dict = []
		cursor = self.conn.execute("SELECT * from %s" % (self.table))
		for row in cursor:
			fp.write(str(row[0])+"\t" + str(row[1])+"\t"+str(row[2])+"\t"+str(row[3])+"\t"+str(row[4])+"\t"+str(row[5])+"\t")
			output_dict.append({'review_id':row[0], 'product_id':row[1], 'time':row[2], 'helpfulness':row[3], 'review':row[4], 'star_rating':row[5]})
		fp.close()
		with open(file+'_dict.txt', 'w') as file:
			file.write(json.dumps(output_dict))
		print "Operation done successfully";

def main():
    database = "/review.db"

    conn = create_connection(database)

    with conn:
    	insert_link( "arereaggrea", "kushagra")
    	print_all()
if __name__ == '__main__':
    main()