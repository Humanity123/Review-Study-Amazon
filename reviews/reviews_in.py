#!/usr/bin/python
from selenium import webdriver
import SQLite1 as my_db
from random import randint
from time import sleep
from datetime import datetime

database_path_links = "/home/gulab/pythonsqlite.db"
database_path_reviews = "/home/gulab/pythonsqlite3.db"

rev_table_name = "IN_REV"
lin_table_name = "IN_LINKS"

def store_reviews_in_page(ProdId, address, driver):
	# driver = webdriver.Firefox()
	try:
		rev_table = my_db.database_sqlite()
		rev_table.create_connection(database_path_reviews)
		rev_table.set_table_name(rev_table_name)
		driver.get(address)

		# driver.get(review_link)
		answer = driver.find_element_by_xpath('//div[@id="cm_cr-review_list"]')
		# print(answer)
		results = answer.find_elements_by_xpath('./div[@data-hook="review"]')
		# print(len(results))

		try:
			answer = driver.find_element_by_xpath('//ul[@class="a-pagination"]')
			# print(answer)
			answer = answer.find_element_by_xpath('./li[@class="a-last"]')
			answer = answer.find_element_by_xpath('./a')
			next_link = answer.get_attribute('href')
		except:
			next_link=0
		# print(len(results))
	
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
			date = datetime.strptime(date,"%d %B %Y").isoformat()

			
			vote = review.find_element_by_xpath('.//span[@data-hook="review-voting-widget"]')
			vote = vote.text.split(" ")[0]
			# type(vote)
			if vote=="Was":
				vote=0
			elif vote=="One":
				vote=1

			rev_data = review.find_element_by_xpath('.//span[@data-hook="review-body"]')
			rev_data = rev_data.text

			# print ProdId
			# print review_id
			# print vote
			# print date
			# print rev_data
			# print stars
			# print "------------"		    
			rev_table.insert_review(review_id, ProdId, date, vote, rev_data, stars)
		rev_table.save_changes()
		print "REVIEWS On PAGE SAVED"
		rev_table.get_count()
		return next_link
	except Exception as e:
		print e
	# driver.quit()
	return -1



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

def get_all_reviews():
	links_table = my_db.database_sqlite()
	links_table.create_connection(database_path_links)
	links_table.set_table_name(lin_table_name)
	links_table.initialise_cursor()
	row = links_table.get_next_element()
	while row:	
		print row[0]
		ret_val = spider_all(row[0],row[1])
		if ret_val==-1
			print "Unsuccesfull crawl Attempt! Going to next product"
		row = links_table.get_next_element()

def main():
	crt_page = "https://www.amazon.in/Samsung-G-550FY-On5-Pro-Gold/dp/B01FM7GGFI/ref=sr_1_1?s=electronics&ie=UTF8&qid=1504191327&sr=1-1&keywords=phone"
	# driver = webdriver.Firefox()
	# crt_page = "dhgrfhg"
	# initialise_conn(database_path)
	# my_db.set_table_name(rev_table_name)

	rev_table = my_db.database_sqlite()
	rev_table.create_connection(database_path_reviews)
	rev_table.set_table_name(rev_table_name)


	# rev_table = my_db.database_sqlite()
	# rev_table.create_connection(database_path_links)
	# rev_table.set_table_name(lin_table_name)



	rev_table.create_table_reviews()
	# rev_table.initialise_cursor()
	get_all_reviews()

	# spider_all("kusagra",crt_page)
	# spider_all("https://www.amazon.com/s/ref=sr_ex_n_1?rh=n%3A2335752011%2Ck%3Aphones&bbn=2335752011&keywords=phones&ie=UTF8&qid=1503142996")
	rev_table.get_count()
	rev_table.print_all()
	rev_table.get_count()

if __name__ == '__main__':
	main()
