#!/usr/bin/python
from pyvirtualdisplay import Display
from selenium import webdriver
from random import randint
from time import sleep
import sys
import copy

sys.path.append("../Data_Extraction/1.product_links")
import links_db as my_db
'''input1 destination dir where joined db is stored'''
'''input2 source dir containing crawled data'''
cmd_arg = sys.argv
destination_database_dir = cmd_arg[1]
source_database_dir = cmd_arg[2]

def save_common_products(destination_database_dir, source_database_dir):
	'''generates dbs with id,link for each domain for products with same id across all three domains'''
	database_path_ca_links = destination_database_dir + "/ca/ca_links.db"
	database_path_uk_links = destination_database_dir + "/uk/uk_links.db"
	database_path_us_links = destination_database_dir + "/us/us_links.db"

	source_database_dir_ca = source_database_dir + "/ca/links.db"
	source_database_dir_us = source_database_dir + "/us/links.db"
	source_database_dir_uk = source_database_dir + "/uk/links.db"

	conn = my_db.create_connection(source_database_dir_uk)
	conn.execute("attach '%s' as db1" % (source_database_dir_us) )
	conn.execute("attach '%s' as db2" % (source_database_dir_ca) )
	print source_database_dir_ca
	cursor = conn.execute("select * from UK_LINKS a inner join db2.CA_LINKS b inner join db1.COM_LINKS c on a.PROD_ID = b.Prod_ID and a.Prod_ID  = c.Prod_ID;")

	my_db.create_connection(database_path_uk_links)
	my_db.set_table_name("UK_LINKS_com")
	my_db.create_table()
	# my_db.get_count()

	for row in cursor:
		# print "-------------------------------"
		# print row[0]
		my_db.insert_link(row[0],row[1])

	my_db.save_changes()
	my_db.get_count()

	conn = my_db.create_connection(source_database_dir_uk)
	conn.execute("attach '%s' as db1" % (source_database_dir_us) )
	conn.execute("attach '%s' as db2" % (source_database_dir_ca) )
	print source_database_dir_ca
	cursor = conn.execute("select * from UK_LINKS a inner join db2.CA_LINKS b inner join db1.COM_LINKS c on a.PROD_ID = b.Prod_ID and a.Prod_ID  = c.Prod_ID;")

	my_db.create_connection(database_path_ca_links)
	my_db.set_table_name("CA_LINKS_com")
	my_db.create_table()
	# my_db.get_count()

	for row in cursor:
		# print "-------------------------------"
		# print row[0]
		my_db.insert_link(row[2],row[3])

	my_db.save_changes()
	my_db.get_count()

	conn = my_db.create_connection(source_database_dir_uk)
	conn.execute("attach '%s' as db1" % (source_database_dir_us) )
	conn.execute("attach '%s' as db2" % (source_database_dir_ca) )
	print source_database_dir_ca
	cursor = conn.execute("select * from UK_LINKS a inner join db2.CA_LINKS b inner join db1.COM_LINKS c on a.PROD_ID = b.Prod_ID and a.Prod_ID  = c.Prod_ID;")

	my_db.create_connection(database_path_us_links)
	my_db.set_table_name("US_LINKS_com")
	my_db.create_table()
	# my_db.get_count()

	for row in cursor:
		# print "-------------------------------"
		# print row[0]
		my_db.insert_link(row[4],row[5])

	my_db.save_changes()
	my_db.get_count()

save_common_products(destination_database_dir, source_database_dir)


