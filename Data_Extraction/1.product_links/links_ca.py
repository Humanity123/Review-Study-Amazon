#!/usr/bin/python
from pyvirtualdisplay import Display
from selenium import webdriver
import links_db as my_db
from random import randint
from time import sleep
import sys

conn = ""

#for redirecting output display when on ssh server
display = Display(visible=0, size=(1000, 1200))
display.start()

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
			link = result.find_element_by_xpath('.//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]')
			# print("----------",len(link),"-----------")
			url = link.get_attribute('href').encode('ascii','ignore')

			my_db.insert_link(Prod_id, url)
			# my_db.save_changes()

			# print("{} : {} ({})".format(Prod_id, url))
		my_db.save_changes()
		# driver.quit()		
		print "Links on Page saved!"
		my_db.get_count()
		sys.stdout.flush()
		return next_link
	except :
		my_db.discard_changes()
		print "Error"
	# driver.quit()
	return -1

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
	# database_path = "/home/kushagra/Documents/BTP/my_work/tests/pythonsqlite.db"
	initialise_conn(database_path_links)
	my_db.set_table_name("CA_LINKS")
	my_db.create_table()
	my_db.get_count()
	# my_db.print_all()
	# spider_all("https://www.amazon.ca/s/ref=sr_pg_303?fst=as%3Aoff&rh=n%3A667823011%2Cn%3A3379552011%2Cn%3A3379583011%2Ck%3Aphones&page=303&keywords=phones&ie=UTF8&qid=1507458489&spIA=B00YD5400Y,B0725WTZ5F,B0749NMVVY,B0172EEAQQ,B074PQTPMF,B01DTTVSJU,B06XK6WFB7,B075GBWGR3,B074J5V8K3,B00UH9AMKM,B074Z35146,B01JAWXOO2,B017CRMIV2,B06XBYQ4XD,B00WMMVPEE,B06XH4396B,B01MU73LLA,B074DR3QNM,B01M9EE5LE,B0745C1Y4Z,B01NB9KZZ8,B071H9K237,B0752TQ86Y,B074MNPSHV,B01DZW39UM,B0713PJ8MQ,B01EBTKSLG,B01JK402T0,B01LXGOR54,B0732QXFBZ,B01N2O6FG7,B01JFN06GU,B01EJDOPBI,B01DZOFW1E,B01KLMNOFE,B01M7X7WBH,B06Y68C63W,B01NBWS96T,B016ICTR9I,B00ZW8ZYOM,B013HVRTMK,B00EY2Q1AS,B0714NB918,B01NCBEW4D,B01ICZ8CJ0,B074C9LXM7,B01EBTKUBY,B06XDLN11T,B00UAF52RQ,B015HD7W9Q,B01LZG8DY4,B01GYE95JW,B00CSJ50HY,B01F78SWUO,B01NA83DNF,B074XW4YBN,B01M3VPQS6,B01FEXJ8U0,B00SA81UGC,B073PVY8TR,B01M31KHRW,B00B4JQPP0,B01L1B5DC6,B00PJSIIES,B01N23NFCM,B0084AHMD6,B0084ALIJ0,B01ANERDRU,B01AOV4UXC,B074J6ZD2N,B075G9L2YC,B01MRU7PXN,B074PLKV71,B075KZ8XPM,B014KSXPTK,B0052DHEIG,B06XKNWQGW,B0083F4WX0")
	spider_all("https://www.amazon.ca/s/gp/search/ref=sr_nr_p_n_feature_two_brow_4?fst=as%3Aoff&rh=n%3A667823011%2Cn%3A677230011%2Cn%3A677235011%2Ck%3Acamera%2Cp_n_feature_two_browse-bin%3A1233088011%7C1233089011%7C1233090011%7C1233091011%7C1233092011&keywords=camera&ie=UTF8&qid=1509109935&rnid=1233087011")

if __name__ == '__main__':
	main()