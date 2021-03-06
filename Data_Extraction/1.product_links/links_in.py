#!/usr/bin/python
from pyvirtualdisplay import Display
from selenium import webdriver
import links_db as my_db
from random import randint
from time import sleep
import sys

#for redirecting output display when on ssh server
display = Display(visible=0, size=(1000, 1200))
display.start()

conn = ""

cmd_arg = sys.argv
database_dir = cmd_arg[1]
database_path_links = database_dir + "/links.db"

# stores all the productIds and their links in the current page with address as $address
#assumpes that database conn has been set up
def store_links_in_page(address, driver):
	# driver = webdriver.Firefox()
	try:
		print address
		sys.stdout.flush()
		driver.get(address)
		print "Got Page Succesfully!!!"
		answer = driver.find_element_by_xpath('//ul[@id="s-results-list-atf"]')
		results = answer.find_elements_by_xpath('./li')

		try:
			next_page = driver.find_element_by_xpath('//a[@id="pagnNextLink"]')
			next_link = next_page.get_attribute('href').encode('ascii','ignore')
		except:
			next_link=0
		# print(len(results))
	
		for result in results:
			# video = result.find_element_by_xpath('./li')
			# video = result
			Prod_id = result.get_attribute('data-asin').encode('ascii','ignore')
			link = result.find_element_by_xpath('.//a[@class="a-link-normal a-text-normal"]')
			url = link.get_attribute('href').encode('ascii','ignore')

			my_db.insert_link(Prod_id, url)

			# print("{} : {} ({})".format(Prod_id, url))
		my_db.save_changes()
		# driver.quit()
		print "Links on Page saved!"
		my_db.get_count()
		sys.stdout.flush()
		return next_link
	except Exception as e:
		my_db.discard_changes()
		print e
	# driver.quit()
	return -1

#creates the connection to the database located at $file 
def initialise_conn(file):
	global conn
	conn = my_db.create_connection(file)

def create_table():
	my_db.create_table()

def testing():
	database_path = "/home/kushagra/Documents/BTP/my_work/tests/pythonsqlite.db"
	initialise_conn(database_path)
	my_db.insert_link("opbfhd", "fdhfjgh")
	my_db.print_all()
	my_db.save_changes()

def spider_all(address):
	crt_page = address
	driver = webdriver.Firefox()
	print "Firefox running!"
	while crt_page:
		sleep(randint(5,15))
		ret_val = store_links_in_page(crt_page,driver)
		if ret_val==-1:
			sleep(5)
			try:
				driver.quit()
			except:
				print "repeat!"
			driver = webdriver.Firefox()
			continue
		crt_page = ret_val
	driver.quit()


def main():
	# database_path = "/home/bt2/14CS10055/BTP_Resources/Data/links.db"
	initialise_conn(database_path_links)
	my_db.set_table_name("IN_LINKS")
	my_db.create_table()
	spider_all("https://www.amazon.in/s/gp/search/ref=sr_nr_p_n_feature_browse-b_4?fst=as%3Aoff&rh=n%3A976419031%2Cn%3A1388977031%2Cn%3A1389175031%2Ck%3Acamera%2Cp_n_feature_browse-bin%3A1484879031%7C1484881031%7C1484882031%7C1484883031%7C1484884031%7C4048478031&keywords=camera&ie=UTF8&qid=1509109690&rnid=1484878031")
	# my_db.create_table()
	my_db.get_count()
	my_db.print_all()

if __name__ == '__main__':
	main()
