#!/usr/bin/python
from pyvirtualdisplay import Display
from selenium import webdriver
import links_db as my_db
from random import randint
from time import sleep
import sys

#for redirecting output display when on ssh server
display = Display(visible=0, size=(800, 600))
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
		driver.get(address)

		answer = driver.find_element_by_xpath('//ul[@id="s-results-list-atf"]')
		results = answer.find_elements_by_xpath('./li')
		try:
			next_page = driver.find_element_by_xpath('//a[@id="pagnNextLink"]')
			next_link = next_page.get_attribute('href')
		except:
			next_link=0
		# print(len(results))
	
		for result in results:
		    # video = result.find_element_by_xpath('./li')
		    # video = result
		    Prod_id = result.get_attribute('data-asin')
		    link = result.find_element_by_xpath('.//a[@class="a-link-normal a-text-normal"]')
		    # print("----------",len(link),"-----------")
		    url = link.get_attribute('href')
		    
		    my_db.insert_link(Prod_id, url)
		    # my_db.save_changes()
		    
		    # print("{} : {} ({})".format(Prod_id, url))
		my_db.save_changes()
		# driver.quit()
		sys.stdout.flush()
		return next_link
	except :
		print "Error"
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
	# database_path = "/home/kushagra/Documents/BTP/my_work/data/pythonsqlite.db"
	initialise_conn(database_path_links)
	my_db.set_table_name("IN_LINKS")
	my_db.create_table()
	spider_all("https://www.amazon.co.uk/s/ref=sr_nr_n_8?fst=as%3Aoff&rh=n%3A560798%2Cn%3A5362060031%2Ck%3Aphone&keywords=phone&ie=UTF8&qid=1503568898&rnid=560800")
	# my_db.create_table()
	my_db.print_all()
	my_db.get_count()

if __name__ == '__main__':
	main()
