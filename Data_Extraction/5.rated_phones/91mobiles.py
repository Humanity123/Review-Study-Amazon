#!/usr/bin/python
# from pyvirtualdisplay import Display
from selenium import webdriver
# import links_db as my_db
from random import randint
from time import sleep
import sys
import pickle

conn = ""

#for redirecting output display when on ssh server
# display = Display(visible=0, size=(1000, 1200))
# display.start()

# cmd_arg = sys.argv
# database_dir = cmd_arg[1]
# database_path_links = database_dir + "/links.db"

# stores all the productIds and their links in the current page with address as $address
#assumpes that database conn has been set up
def store_links_in_page(address):
	driver = webdriver.Firefox()
	try:
		print address
		sys.stdout.flush()
		driver.get(address)
		aspects = ['performance', 'display', 'camera', 'battery']
		features = []
		while True:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			sleep(randint(4,8))
			phones = driver.find_elements_by_xpath('//div[@class="finder_snipet_wrap "]')
			print len(phones)
			for phone in phones:
				try:
					ls = {}
					name = phone.find_element_by_xpath('.//a[@class="hover_blue_link name gaclick"]')
					model = name.text
					# print model
					ls['model'] = model
					overall = phone.find_element_by_xpath('.//div[@class="rating_box_new_list"]')
					overall = int(overall.text[:-1])
					# print overall
					ls['overall'] = overall
					ratings = phone.find_elements_by_xpath('.//div[@class="mtr_bar_div"]')
					for i,rating in enumerate(ratings):
						rate = rating.find_element_by_xpath('./div').get_attribute('style')[7:9]
						ls[aspects[i]] = int(rate)
					features.append(ls)
				except:
					print "something unavailable for : ", model
				# features.append(answer.text.encode('ascii','ignore').split()[1])
			# print len(features), features[len(features)-1]
			btn = driver.find_element_by_xpath('.//div[@class="listing-btns4"]')
			btn = btn.find_element_by_xpath('./span[@class="list-bttnn"]')
			if btn is not None:
				btn.click()
			else:
				break
	except :
		pickle.dump(features,open('features.pickle','w'))
		print "Completed Retrieval"
	return 1

#creates the connection to the database located at $file 
def initialise_conn(file):
	global conn
	conn = my_db.create_connection(file)

def create_table():
	my_db.create_table()

def spider_all(address):
	crt_page = address
	driver = webdriver.Firefox()
	while crt_page:
		sleep(randint(2,5))
		ret_val = store_links_in_page(crt_page)
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
	# initialise_conn(database_path_links)
	# my_db.set_table_name("CA_LINKS")
	# my_db.create_table()
	# my_db.get_count()

	store_links_in_page("https://www.91mobiles.com/mobile-price-list-in-india")

if __name__ == '__main__':
	main()