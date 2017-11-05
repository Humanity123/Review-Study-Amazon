#!/usr/bin/python
import reviews_com as rv
import sys

cmd_arg = sys.argv
database_dir = cmd_arg[1]
database_path_reviews = database_dir + "/reviews.db"

rev_table_name = "COM_REV_com"

def main():
	rev_table = rv.my_db.database_sqlite()
	rev_table.create_connection(database_path_reviews)
	rev_table.set_table_name(rev_table_name)
	rev_table.create_table_reviews()

	# fp = open("input","r")
	# for line in fp:
	# 	arguments  = line.split()
	# 	rv.spider_all(arguments[0], arguments[1]) 

	# fp = open("output.txt","w")
	# fp.write("review_id\tproduct_id\ttime\thelpfulness\treview\tstar_rating\n")
	# fp.close()
	rev_table.dump("output")
	rev_table.get_count()
	rev_table.print_all()
	rev_table.get_count()

if __name__ == '__main__':
	main()