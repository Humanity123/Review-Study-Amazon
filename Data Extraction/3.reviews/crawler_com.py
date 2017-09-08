#!/usr/bin/python
from selenium import webdriver
import SQLite1 as my_db
from random import randint
from time import sleep

conn = ""

database_path_links = "/home/gulab/pythonsqlite.db"
lin_table_name = "COM_LINKS"

# stores all the productIds and their links in the current page with address as $address
#assumpes that database conn has been set up
def store_links_in_page(address, driver):
	# driver = webdriver.Firefox()
	try:
		lin_table = my_db.database_sqlite()
		lin_table.create_connection(database_path_links)
		lin_table.set_table_name(lin_table_name)

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
		    link = result.find_element_by_xpath('.//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]')
		    # print("----------",len(link),"-----------")
		    url = link.get_attribute('href')
		    
		    lin_table.insert_link(Prod_id, url)
		    # lin_table.save_changes()
		    
		    # print("{} : {} ({})".format(Prod_id, url))
		print "Links On Page Saved"
		lin_table.get_count()
		lin_table.save_changes()
		# driver.quit()
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
				print ""
			driver = webdriver.Firefox()
			continue
		crt_page = ret_val
	driver.quit()


def main():
	database_path = "/home/gulab/pythonsqlite.db"
	# initialise_conn(database_path)
	lin_table = my_db.database_sqlite()
	lin_table.create_connection(database_path_links)
	lin_table.set_table_name(lin_table_name)
	lin_table.create_table()
	# spider_all("https://www.amazon.com/s/ref=sr_ex_n_1?rh=n%3A2335752011%2Ck%3Aphones&bbn=2335752011&keywords=phones&ie=UTF8&qid=1503142996")
	lin_table.get_count()
	# my_db.print_all()

if __name__ == '__main__':
	main()
