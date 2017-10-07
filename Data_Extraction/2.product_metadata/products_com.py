#!/usr/bin/python
from pyvirtualdisplay import Display
from selenium import webdriver
import products_db as my_db
from random import randint
from time import sleep
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import sys
import psutil

#redirecting output display when using ssh server
display = Display(visible=0, size=(1000, 1000))
display.start()

cmd_arg = sys.argv
database_dir = cmd_arg[1]

database_path_links = database_dir + "/links.db"
database_path_reviews = database_dir + "/reviews.db"
database_path_prod =  database_dir + "/products.db"

img_table_name = "IMG"
desc_table_name = "DESC"
prod_table_name = "PROD"
lin_table_name = "LINKS"
domain = "COM"

#stores reviews in the current page and returns the link to NEXT page
def store_metadata_in_page(ProdId, address, driver):
	# driver = webdriver.Firefox()
	prod_db = my_db.database_sqlite()
	prod_db.create_connection(database_path_prod)
	prod_db.set_table_name(domain)
	driver.get(address)
	print "Retrieved Product Page successfully!!!"
	print address
	sys.stdout.flush()
	results = driver.find_element_by_xpath('.//span[@id="productTitle"]')
	#getting title of product
	title = results.text
	print title
	sys.stdout.flush()
	#getting star of product
	try:
		result = driver.find_element_by_xpath('.//div[@id="averageCustomerReviews"]')
		result = result.find_element_by_xpath('.//span[@id="acrPopover"]')
		stars = result.get_attribute('title').split(" ")[0]
	except:
		stars = "0"
	#insert into product table
	prod_db.insert_prod(ProdId, title, stars)

	#getting features of the product
	results = driver.find_element_by_xpath('.//div[@id="feature-bullets"]')
	features = results.find_elements_by_xpath('./ul/li')
	i=0
	for feature in features:
		i+=1
		prod_db.insert_desc(ProdId, feature.text, ProdId+"#"+str(i))
		# print feature.text

	#getting images of product
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

	#save changes
	prod_db.save_changes()
	print ProdId,  "Retrived successfully!!!"
	prod_db.get_count(prod_table_name)
	sys.stdout.flush()
	return 1

#getting metadata for all products in LINK table
def get_all_metadata():
	links_table = my_db.database_sqlite()
	links_table.create_connection(database_path_links)
	links_table.set_table_name(domain)
	#initialise a cursor in db
	links_table.initialise_cursor(lin_table_name)
	#get next row in db
	row = links_table.get_next_element()
	retry_cnt = 2
	while retry_cnt:
		try:
			driver = webdriver.Firefox()
			driver_process = psutil.Process(driver.service.process.pid)
			print "Firefox Running!!"
			sys.stdout.flush()
			while row:	
				prod_table = my_db.database_sqlite()
				prod_table.create_connection(database_path_prod)
				prod_table.set_table_name(domain+"_"+prod_table_name)
				val = prod_table.is_product_present(row[0])
				va = val.fetchone()
				cnt = va[0]
				prod_table.close_connection()
				if cnt!=0:
					print "Already Crawled Some MetaData for", row[0]
					sys.stdout.flush()
				else:
					print "Getting metadata for : ", row[0]
					sys.stdout.flush()
					sleep(randint(2,5))
					store_metadata_in_page(row[0],row[1],driver)
				row = links_table.get_next_element()
			break
		except Exception as e:
			print "Error in getting metadata!"
			print e
			
			if driver_process.is_running():
				print ("driver is running")

				firefox_process = driver_process.children()
				if firefox_process:
					firefox_process = firefox_process[0]

					if firefox_process.is_running():
						print("Firefox is still running, we can quit")
						driver.quit()
					else:
						print("Firefox is dead, can't quit. Let's kill the driver")
						firefox_process.kill()
				else:
					print("driver has died")
				sys.stdout.flush()
			print "Retrying..."
			retry_cnt-=1
		if retry_cnt==0:
			print "Crawling FAILED! Going to next Product!"
			row = links_table.get_next_element()
			retry_cnt=2
		sys.stdout.flush()
	links_table.get_count(lin_table_name)
	
def main():
	prod_table = my_db.database_sqlite()
	prod_table.create_connection(database_path_prod)
	prod_table.set_table_name(domain)
	prod_table.create_table_products()
	prod_table.create_table_img()
	prod_table.create_table_desc()

	get_all_metadata()

	# prod_table.get_count(prod_table_name)
	# prod_table.print_all(prod_table_name)
	# prod_table.print_all(desc_table_name)
	# prod_table.print_all(img_table_name)
	# prod_table.get_count(prod_table_name)
	# prod_table.get_count(desc_table_name)
	# prod_table.get_count(img_table_name)

if __name__ == '__main__':
	main()
