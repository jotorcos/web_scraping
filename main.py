import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import pandas as pd
from datetime import datetime

import platform
if (platform.system() == 'Windows'):
    webdriver_path = r'C:\Users\obardes\Documents\chromedriver_win32\chromedriver'
else:
    webdriver_path = r'/usr/local/bin/chromedriver'


def extract_information(url, movies_df, col_names):
    '''
        :Params:
         url - A film's description link i.e. https://www.filmaffinity.com/es/film996348.html
         movies_df - A pandas dataframe where new movies entries are appended to
         col_names - List of column names in "movies_df"

         :Description:
         Initilizes a Selenium browser for each URL recieved to being extraction process

         :Returns:
         Returns "movies_df" with new appended entries and a consolidated error count
    '''

    # Path to webdriver
    browser = webdriver.Chrome(webdriver_path)

    # URL to scrape
    browser.get(url)
    time.sleep(1)

    # Initialize List
    title, year, duration, country, rating = [], [], [], [], []

    info_elems = browser.find_elements_by_class_name("movie-info")

    # Get title
    title = info_elems[0].find_elements_by_tag_name("dd")[0].text

    # Get year
    year = info_elems[0].find_elements_by_tag_name("dd")[1].text

    # Get duration
    duration = info_elems[0].find_elements_by_tag_name("dd")[2].text

    # Get country
    country = info_elems[0].find_elements_by_tag_name("dd")[3].text

    # Get rating
    rating_elems = browser.find_elements_by_id("movie-rat-avg")

    if len(rating_elems):
        rating = rating_elems[0].text
    else:
        rating = 'None'

    movie_info = {
        'title': title,
        'year': year,
        'duration': duration,
        'country': country,
        'rating': rating
    }

    print(movie_info)

    df_mismatch = 0
    try:
        # Create new entry
        create_new_entry = pd.DataFrame(
            movie_info, columns=col_names, index=[0])

        # Appends new entry to posts_df
        movies_df = movies_df.append(
            create_new_entry, ignore_index=True)
        print('Dataframe')
        print(movies_df)
    except:
        print('mismatch')
        df_mismatch += 1
        pass

    browser.quit()

    return movies_df, df_mismatch


def get_billboard_links(pub_url):
    '''
        :Params:
         pub_url - URL link of the film affinity billboard

        :Description:
         Scrapes all the movies in the billboard

        :Returns:
         Returns a list of the links in the billboard
    '''

    # Path to webdriver
    browser = webdriver.Chrome(webdriver_path)

    # URL to scrape
    browser.get(pub_url)
    time.sleep(1)

    # Let's retrieve all the elements based on CSS selector: movie-title
    elems = browser.find_elements_by_css_selector(".movie-title [href]")
    links = [elem.get_attribute('href') for elem in elems]

    browser.quit()

    return links


############################################################################


url = "https://www.filmaffinity.com/es/cat_new_th_es.html"

# Get profile links
links = get_billboard_links(url)

movies_col = ["title", "year", "duration", "country", "rating"]

# Initalize empty dfs
movies_df = pd.DataFrame(None, columns=movies_col)

# Loop through URL list
t0 = datetime.now()
time_counter = 0
error_count = 0
save_state = 0
for link in links:
    time_counter += 1
    sys.stdout.write("Processed: %s / %s \r" % (time_counter, len(links)))
    sys.stdout.flush()
    movies_df, error_retrieved = extract_information(
        link, movies_df, movies_col)
    error_count += error_retrieved

    # save to csv every 50 urls
    if save_state % 5 == 1:
        # Write to CSVs
        movies_df.to_csv(r'movies_scrape/movies_df.csv')

    save_state += 1

    print("Processed: %s / %s -- Elapse Time: %s" %
          (time_counter, len(links), datetime.now()-t0))
    print(f"Errors due to input mismatch: {error_count}")

# Write to CSVs
movies_df.to_csv('movies_df.csv')
