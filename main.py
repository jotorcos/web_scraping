import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

webdriver_path = r'/usr/local/bin/chromedriver'


# Selenium

def get_total_cases(pub_url):
    '''
        :Params:
         pub_url - URL link of a medium publication i.e. https://medium.com/search/users?q=towards%20data%20science

        :Description:
         Scrapes links related to user profiles from a publication page. i.e. https://medium.com/@kozyrkov

        :Returns:
         Returns a list of user names and user profile urls

    '''

    # Path to webdriver
    browser = webdriver.Chrome(webdriver_path)

    # URL to scrape
    browser.get(pub_url)
    time.sleep(1)

    total_cases = browser.find_element_by_class_name(
        "maincounter-number").get_attribute('textContent')

    browser.quit()

    return total_cases


############################################################################


url = "https://www.worldometers.info/coronavirus/"

total_cases = get_total_cases(url)

print(f'No. of total cases: {total_cases}')
