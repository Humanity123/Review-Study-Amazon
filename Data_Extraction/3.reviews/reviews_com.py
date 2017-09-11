#!/usr/bin/python
from pyvirtualdisplay import Display
from selenium import webdriver
import reviews_db as my_db
from random import randint
from time import sleep
from datetime import datetime

#redirecting output display when using ssh server
display = Display(visible=0, size=(1000, 800))
display.start()

cmd_arg = sys.argv
database_dir = cmd_arg[1]
database_path_links = database_dir + "/links.db"
database_path_reviews = database_dir + "/reviews.db"
database_path_prod =  database_dir + "/products.db"

rev_table_name = "COM_REV"
lin_table_name = "COM_LINKS"

#stores reviews in the current page and returns the link to NEXT page
def store_reviews_in_page(ProdId, address, driver):
	try:
		#create connection to the database
		rev_table = my_db.database_sqlite()
		rev_table.create_connection(database_path_reviews)
		rev_table.set_table_name(rev_table_name)
		driver.get(address)
		print  "Review Page Accessed!"
		try:
			results = driver.find_elements_by_xpath('.//div[@data-hook="review"]')
		except:
			results = []
		try: #getting link for next page
			answer = driver.find_element_by_xpath('//ul[@class="a-pagination"]')
			answer = answer.find_element_by_xpath('./li[@class="a-last"]')
			answer = answer.find_element_by_xpath('./a')
			next_link = answer.get_attribute('href')
		except:
			next_link=0

		#iterating over the reviews in current page
		for result in results:
			review_id = result.get_attribute('id')
			review = result.find_element_by_xpath('./div')
			
			stars = review.find_element_by_xpath('./div/a')
			stars = stars.get_attribute('title')
			stars = stars.split(" ")[0]
			
			date = review.find_element_by_xpath('.//span[@data-hook="review-date"]')
			date = date.text.split(" ")
			# date = date.split(" ")
			date = " ".join(date[1:])
			date = datetime.strptime(date,"%B %d, %Y").isoformat()

			
			vote = review.find_element_by_xpath('.//span[@data-hook="review-voting-widget"]')
			vote = vote.text.split(" ")[0]
			# type(vote)
			if vote=="Was":
				vote=0
			elif vote=="One":
				vote=1

			rev_data = review.find_element_by_xpath('.//span[@data-hook="review-body"]')
			rev_data = rev_data.text
	    
			rev_table.insert_review(review_id, ProdId, date, vote, rev_data, stars)
		#commit changes in db if no error encountered
		rev_table.save_changes()
		print "REVIEWS On PAGE SAVED"
		rev_table.get_count()
		return next_link
	except Exception as e:
		print e
	# driver.quit()
	return -1

def testing():
	database_path = "/home/gulab/pythonsqlite.db"
	initialise_conn(database_path)
	my_db.insert_link("opbfhd", "fdhfjgh")
	my_db.print_all()
	my_db.save_changes()

#iterates through all the review pages of the given product
def spider_all(ProdId,address):
	crt_page = address
	retry_cnt = 5 #will try maximum 5 times for one page
	while retry_cnt:
		try:
			driver = webdriver.Firefox()
			print "Firefox runnning to crawl ", ProdId
			driver.get(crt_page)
			results = driver.find_elements_by_xpath('.//div[@id="reviewSummary"]')
			result = results[0].find_element_by_xpath('./div/a')
			review_link = result.get_attribute('href')
			print review_link
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

	print "Starting to crawl reviews!"
	while crt_page:
		sleep(randint(5,15))
		ret_val = store_reviews_in_page(ProdId,crt_page,driver)
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

#iterates through all the products in LINKS db
def get_all_reviews():
	links_table = my_db.database_sqlite()
	links_table.create_connection(database_path_links)
	links_table.set_table_name(lin_table_name)
	links_table.initialise_cursor()
	row = links_table.get_next_element()
	while row:	
		print "Crawling for", row[0], " started!"
		ret_val = spider_all(row[0],row[1])
		if ret_val==-1:
			print "Unsuccesfull crawl Attempt! Going to next product"
		row = links_table.get_next_element()

def main():
	rev_table = my_db.database_sqlite()
	rev_table.create_connection(database_path_reviews)
	rev_table.set_table_name(rev_table_name)
	rev_table.create_table_reviews()

	get_all_reviews()

	rev_table.get_count()
	rev_table.print_all()
	rev_table.get_count()

if __name__ == '__main__':
	main()
