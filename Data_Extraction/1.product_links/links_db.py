#!/usr/bin/python
 
import sqlite3
from sqlite3 import Error

conn = ""
table = "LINKS"
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    global conn
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except :
        print ""
 
    return None

def insert_link(id_p,link):
	cur = conn.cursor()
	try:
		cur.execute("INSERT INTO %s VALUES (?,?)" % (table),(id_p,link,))
		return 1
	except Exception as e:
		print e

	return 0

def create_table():
	try:
		conn.execute("CREATE TABLE %s (Prod_ID TEXT PRIMARY KEY      NOT NULL, LINK TEXT NOT NULL);" % (table))
		return 1
	except:
		print ""

	return 0
	
def set_table_name(table_name):
	global table 
	table = table_name

def get_count():
	# LINKS = "LINKS"
	cursor = conn.execute("SELECT count(*) from %s" % (table))
	for row in cursor:
		print "COUNT = ", row[0]
		# print "LINK = ", row[1], "\n"
		# print "ADDRESS = ", row[2]
		# print "SALARY = ", row[3], "\n"

	print "Operation done successfully";

def print_all():
	cursor = conn.execute("SELECT * from %s" % (table))
	for row in cursor:
		print "ID = ", row[0]
		print "LINK = ", row[1], "\n"
		# print "ADDRESS = ", row[2]
		# print "SALARY = ", row[3], "\n"

	print "Operation done successfully";

def save_changes():
	conn.commit()
	
def discard_changes():
	conn.rollback();

def main():
    database = "/home/kushagra/Documents/BTP/my_work/tests/pythonsqlite.db"
 
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
