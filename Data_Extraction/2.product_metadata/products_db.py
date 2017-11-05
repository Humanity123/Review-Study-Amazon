#!/usr/bin/python
 
import sqlite3
from sqlite3 import Error

class database_sqlite:
	def __init__(self):
		self.conn = ""
		self.table = "IN"
		self.iter_ = ""
	def __del__(self):
		self.conn.close()
	def close_connection(self):
		self.conn.close()
	def create_connection(self,db_file):
		self.conn = sqlite3.connect(db_file)
		return None

	def insert_link(self,id_p,link):
		cur = self.conn.cursor()
		try:
			cur.execute("INSERT INTO %s_LINKS VALUES (?,?)" % (self.table),(id_p,link,))
			return 1
		except Exception as e:
			print e

		return 0

	def initialise_cursor(self,table_name):
		self.iter_ = self.conn.execute("SELECT * from %s_%s" % (self.table,table_name))

	def initialise_cursor_description(self, table_name, prod_id):
		self.iter_ = self.conn.execute("SELECT * from %s_%s WHERE PROD_ID=\"%s\"" % (self.table,table_name,prod_id))

	def get_next_element(self):
		return self.iter_.fetchone()

	def insert_review(self,RevId, ProductID, Rev_Date, Rev_Votes, Review_Data, Rev_Stars ):
		try:
			self.conn.execute("INSERT INTO %s_REV VALUES (?,?,?,?,?,?)" % (self.table),(RevId, ProductID, Rev_Date, Rev_Votes, Review_Data, Rev_Stars,))
			return 1
		except Exception as e:
			print e
		return 0
	def insert_prod(self, ProdId, Title, stars):
		try:
			self.conn.execute("INSERT INTO %s_PROD VALUES (?,?,?)" % (self.table),(ProdId, Title, stars,))
			return 1
		except Exception as e:
			print e
		return 0
	def insert_img(self,ProdId,Info,Cnt):
		try:
			self.conn.execute("INSERT INTO %s_IMG VALUES (?,?,?)" % (self.table),(ProdId, Info, Cnt,))
			return 1
		except Exception as e:
			print e
		return 0
	def insert_desc(self,ProdId,Info,Cnt):
		try:
			self.conn.execute("INSERT INTO %s_DESC VALUES (?,?,?)" % (self.table),(ProdId, Info, Cnt,))
			return 1
		except Exception as e:
			print e
		return 0

	def create_table(self):
		try:
			self.conn.execute("CREATE TABLE %s_LINKS (Prod_ID TEXT PRIMARY KEY      NOT NULL, LINK TEXT NOT NULL);" % (self.table))
			return 1
		except Exception as e:
			print e

		return 0
	def create_table_reviews(self):
		try:
			self.conn.execute("CREATE TABLE %s_REV (Rev_ID TEXT PRIMARY KEY      NOT NULL, ProductID TEXT NOT NULL, Rev_Date DATE , Rev_Votes INT , Review_Data TEXT, Rev_Stars REAL);" % (self.table))
			return 1
		except Exception as e:
			print e
		return 0
	def create_table_products(self):
		try:
			self.conn.execute("CREATE TABLE %s_PROD (PROD_ID TEXT PRIMARY KEY      NOT NULL, TITLE TEXT , STARS REAL);" % (self.table))
			return 1
		except Exception as e:
			print e
		return 0
	def create_table_img(self):
		try:
			self.conn.execute("CREATE TABLE %s_IMG (PROD_ID TEXT NOT NULL, INFO TEXT ,ID TEXT  PRIMARY KEY  );" % (self.table))
			return 1
		except Exception as e:
			print e
		return 0
	def create_table_desc(self):
		try:
			self.conn.execute("CREATE TABLE %s_DESC (PROD_ID TEXT NOT NULL, INFO TEXT ,ID TEXT  PRIMARY KEY  );" % (self.table))
			return 1
		except Exception as e:
			print e
		return 0
	def set_table_name(self,table_name):
		self.table = table_name
	def is_product_present(self,prod_id):
		return self.conn.execute("SELECT count(PROD_ID) from %s WHERE PROD_ID=\"%s\";" % (self.table,prod_id))
	def get_count(self,table_name):
		# LINKS = "LINKS"
		cursor = self.conn.execute("SELECT count(*) from %s_%s" % (self.table,table_name))
		for row in cursor:
			print "COUNT = ", row[0]

		print "Operation done successfully";

	def get_same_prodId(db_file, table_name1, table_name2):
		self.conn.execute("attach \'%s\' as db2;" % (db_file))
		return self.conn.execute("SELECT count(*) from %s_PROD a inner join db2.%s_PROD b on a.PROD_ID = b.PROD_ID;" % (table_name1, table_name2))

	def print_all(self,table_name):
		cursor = self.conn.execute("SELECT * from %s_%s" % (self.table,table_name))
		for row in cursor:
			for data in row:
				print data
			# print "ID = ", row[0]
			# print "\n"
			# print "ADDRESS = ", row[2]
			# print "SALARY = ", row[3], "\n"

		print "Operation done successfully";


	def save_changes(self):
		try:
			self.conn.commit()
		except Exception as e:
			print e
	def discard_changes(self):
		self.conn.rollback();
def main():
    database = "/home/gulab/pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)
    # with conn:
    #     print("1. Query task by priority:")
    #     select_task_by_priority(conn,1)
 
    #     print("2. Query all tasks")
    #     select_all_tasks(conn)

    with conn:
    	insert_link( "arereaggrea", "kushagra")
    	print_all()
if __name__ == '__main__':
    main()