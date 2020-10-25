from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


import platform
if (platform.system() == 'Windows'):
    webdriver_path = r'C:\Users\obardes\Documents\chromedriver_win32\chromedriver'
else:
    webdriver_path = r'/usr/local/bin/chromedriver'


url = "https://www.filmaffinity.com/es/film996348.html"

# Path to webdriver
browser = webdriver.Chrome(webdriver_path)
# URL to scrape
browser.get(url)

time.sleep(1)

elems = browser.find_elements_by_class_name("movie-info")

year = elems[0].find_elements_by_tag_name("dd")[1].text

duration = elems[0].find_elements_by_tag_name("dd")[2].text

country = elems[0].find_elements_by_tag_name("dd")[3].text

rating_elems = browser.find_elements_by_id("movie-rat-avg")

rating = rating_elems[0].text

print(year)

print(duration)

print(country)

print(rating)


browser.quit()
