#!/usr/bin/python
from selenium import webdriver
import SQLite2 as my_db
from random import randint
from time import sleep
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains


database_path_links = "/home/gulab/pythonsqlite.db"
database_path_reviews = "/home/gulab/pythonsqlite3.db"
database_path_prod = "/home/gulab/pythonsqlite2.db"

img_table_name = "IMG"
desc_table_name = "DESC"
prod_table_name = "PROD"
lin_table_name = "LINKS"
domain = "UK"

def store_metadata_in_page(ProdId, address, driver):
	# driver = webdriver.Firefox()
	prod_db = my_db.database_sqlite()
	prod_db.create_connection(database_path_prod)
	prod_db.set_table_name(domain)
	driver.get(address)

	results = driver.find_element_by_xpath('.//span[@id="productTitle"]')
	title = results.text

	result = driver.find_element_by_xpath('.//div[@id="averageCustomerReviews"]')
	result = result.find_element_by_xpath('.//span[@id="acrPopover"]')
	stars = result.get_attribute('title').split(" ")[0]

	prod_db.insert_prod(ProdId, title, stars)

	results = driver.find_element_by_xpath('.//div[@id="feature-bullets"]')
	features = results.find_elements_by_xpath('./ul/li')
	i=0
	for feature in features:
		i+=1
		prod_db.insert_desc(ProdId, feature.text, ProdId+"#"+str(i))
		# print feature.text

	results = driver.find_element_by_xpath('.//div[@id="altImages"]')
	altImages = results.find_elements_by_xpath('./ul/li')
	for img in altImages:
		hover = ActionChains(driver).move_to_element(img)
		hover.perform()		
	results = driver.find_element_by_xpath('.//div[@id="main-image-container"]')
	img = results.find_element_by_xpath('./ul')
	images = img.find_elements_by_xpath('.//img')
	i=0
	for image in images:
		i+=1
		img_src = image.get_attribute('src')
		prod_db.insert_img(ProdId, img_src, ProdId+"#"+str(i))
		# print img_src

	prod_db.save_changes()
	prod_db.get_count(prod_table_name)
	return 1
	# driver.quit()



# # stores all the productIds and their links in the current page with address as $address
# #assumpes that database conn has been set up

def testing():
	database_path = "/home/gulab/pythonsqlite.db"
	initialise_conn(database_path)
	my_db.insert_link("opbfhd", "fdhfjgh")
	my_db.print_all()
	my_db.save_changes()

def spider_all(ProdId,address):
	crt_page = address
	retry_cnt = 5
	while retry_cnt:
		try:
			driver = webdriver.Firefox()
			driver.get(crt_page)
			# print("hello")
			answer = driver.find_element_by_xpath('//a[@id="acrCustomerReviewLink"]')
			# print(answer)
			review_link = answer.get_attribute('href')
		except Exception as e:
			print "Error in getting to review page!"
			print e
			try:
				driver.quit()
			except Exception as e:
				print e
			print "Retrying..."
			retry_cnt-=1
			continue
		break;
	if retry_cnt==0:
		return -1
	crt_page = review_link

	driver.quit()

def get_all_metadata():
	links_table = my_db.database_sqlite()
	links_table.create_connection(database_path_links)
	links_table.set_table_name(domain)
	links_table.initialise_cursor(lin_table_name)
	row = links_table.get_next_element()
	retry_cnt = 5
	while retry_cnt:
		try:
			driver = webdriver.Firefox()
			while row:	
				print row[0]
				# ret_val=0
				sleep(randint(5,15))
				store_metadata_in_page(row[0],row[1],driver)
				row = links_table.get_next_element()
		except Exception as e:
			print "Error in getting metadata!"
			print e
			try:
				driver.quit()
			except Exception as e:
				print e
			print "Retrying..."
			retry_cnt-=1
	links_table.get_count(lin_table_name)
def main():
	crt_page = "https://www.amazon.in/Samsung-G-550FY-On5-Pro-Gold/dp/B01FM7GGFI/ref=sr_1_1?s=electronics&ie=UTF8&qid=1504191327&sr=1-1&keywords=phone"
	# driver = webdriver.Firefox()
	# crt_page = "dhgrfhg"
	# initialise_conn(database_path)
	# my_db.set_table_name(rev_table_name)

	prod_table = my_db.database_sqlite()
	prod_table.create_connection(database_path_prod)
	prod_table.set_table_name(domain)


	# prod_table = my_db.database_sqlite()
	# prod_table.create_connection(database_path_links)
	# prod_table.set_table_name(lin_table_name)



	# prod_table.create_table_reviews()
	prod_table.create_table_products()
	prod_table.create_table_img()
	prod_table.create_table_desc()
	# prod_table.initialise_cursor()
	# get_all_metadata()

	# spider_all("kusagra",crt_page)
	# spider_all("https://www.amazon.com/s/ref=sr_ex_n_1?rh=n%3A2335752011%2Ck%3Aphones&bbn=2335752011&keywords=phones&ie=UTF8&qid=1503142996")
	prod_table.get_count(prod_table_name)
	prod_table.print_all(prod_table_name)
	prod_table.print_all(desc_table_name)
	prod_table.print_all(img_table_name)
	prod_table.get_count(prod_table_name)
	prod_table.get_count(desc_table_name)
	prod_table.get_count(img_table_name)
	# prod_table.get_count(prod_table_name)

if __name__ == '__main__':
	main()
