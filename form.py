import pandas as pd
import bs4 as bs
import urllib.request
from selenium import webdriver

# sauce = urllib.request.urlopen('https://understat.com/league/EPL').read()
# soup = bs.BeautifulSoup(sauce, 'html')
#
# print(soup)

my_url = 'https://understat.com/league/EPL'
driver = webdriver.PhantomJS()
driver.get(my_url)
stuff = driver.find_element_by_tag_name("table")
print(stuff)
driver.close()