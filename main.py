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
    # Path to webdriver
    browser = webdriver.Chrome(webdriver_path)

    # URL to scrape
    browser.get(url)
    time.sleep(1)

    #############
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
    # try:
    # Create new entry
    create_new_entry = pd.DataFrame(
        movie_info, columns=col_names, index=[0])

    # Appends new entry to posts_df
    movies_df = movies_df.append(
        create_new_entry, ignore_index=True)
    print('Dataframe')
    print(movies_df)
    # except:
    #     print('mismatch')
    #     df_mismatch += 1
    #     pass
    #############

    browser.quit()

    return movies_df, df_mismatch


def get_billboard_links(pub_url):
    '''
        :Params:
         pub_url - URL link of the film affinity billboard

        :Description:
         Scrapes all the movies in the billboard

        :Returns:
         Returns a dictionary: keys -> titles of the movies, value -> Affinity URL of the movie
         e.g. Movies + links: {'Cars 3 ': 'https://www.filmaffinity.com/es/film996348.html', 'Trolls 2: Gira mundial ': 'https://www.filmaffinity.com/es/film382118.html', 'El secreto. Atrévete a soñar ': 'https://www.filmaffinity.com/es/film863533.html', 'El club de los divorciados ': 'https://www.filmaffinity.com/es/film282953.html', 'Regreso a Hope Gap ': 'https://www.filmaffinity.com/es/film956950.html', 'Promare ': 'https://www.filmaffinity.com/es/film502713.html', 'El artista anónimo ': 'https://www.filmaffinity.com/es/film886602.html', 'StarDog y TurboCat ': 'https://www.filmaffinity.com/es/film776143.html', 'Una mujer con unas alas tremendas ': 'https://www.filmaffinity.com/es/film370699.html', 'Antología de un pueblo fantasma ': 'https://www.filmaffinity.com/es/film501387.html', 'Meseta ': 'https://www.filmaffinity.com/es/film309963.html', 'Una vez más ': 'https://www.filmaffinity.com/es/film894894.html', 'La voz humana ': 'https://www.filmaffinity.com/es/film524505.html', 'No Matarás ': 'https://www.filmaffinity.com/es/film294014.html', 'Shin Chan en Australia. Tras las esmeraldas verdes ': 'https://www.filmaffinity.com/es/film319021.html', 'Las hijas del Reich ': 'https://www.filmaffinity.com/es/film212481.html', 'Corpus Christi ': 'https://www.filmaffinity.com/es/film115913.html', 'Ane ': 'https://www.filmaffinity.com/es/film741584.html', 'Rebeca ': 'https://www.filmaffinity.com/es/film187222.html', 'Crescendo ': 'https://www.filmaffinity.com/es/film486749.html', 'Vitalina Varela ': 'https://www.filmaffinity.com/es/film461020.html', 'Cunningham ': 'https://www.filmaffinity.com/es/film349000.html', 'De nuevo otra vez ': 'https://www.filmaffinity.com/es/film175879.html', 'Binti ': 'https://www.filmaffinity.com/es/film823369.html', 'La Española. La de Torres ': 'https://www.filmaffinity.com/es/film312336.html', 'No nacimos refugiados ': 'https://www.filmaffinity.com/es/film261699.html', 'Nación cautiva ': 'https://www.filmaffinity.com/es/film126784.html', 'The Vigil ': 'https://www.filmaffinity.com/es/film175872.html', 'Verano del 85 ': 'https://www.filmaffinity.com/es/film781007.html', 'Como perros y gatos: La patrulla unida ': 'https://www.filmaffinity.com/es/film603802.html', 'El arco mágico ': 'https://www.filmaffinity.com/es/film947577.html', 'Dehesa, el bosque del lince ibérico ': 'https://www.filmaffinity.com/es/film359024.html', 'El rey del barrio ': 'https://www.filmaffinity.com/es/film697728.html', 'Cartas mojadas ': 'https://www.filmaffinity.com/es/film475616.html', 'Sanmao: La novia del desierto ': 'https://www.filmaffinity.com/es/film849184.html', 'Arzak since 1897 ': 'https://www.filmaffinity.com/es/film217803.html', 'Explota Explota ': 'https://www.filmaffinity.com/es/film452718.html', "Rifkin's Festival ": 'https://www.filmaffinity.com/es/film761443.html', 'Falling ': 'https://www.filmaffinity.com/es/film595745.html', 'La habitación (The Room) ': 'https://www.filmaffinity.com/es/film164722.html', 'Akelarre ': 'https://www.filmaffinity.com/es/film823863.html', 'El juicio de los 7 de Chicago ': 'https://www.filmaffinity.com/es/film389985.html', 'Una ventana al mar ': 'https://www.filmaffinity.com/es/film694511.html', 'La isla de las mentiras ': 'https://www.filmaffinity.com/es/film687337.html', 'Eso que tú me das ': 'https://www.filmaffinity.com/es/film128695.html', 'Greenland: El último refugio ': 'https://www.filmaffinity.com/es/film688457.html', 'Black Beach ': 'https://www.filmaffinity.com/es/film303755.html', 'Nunca, casi nunca, a veces, siempre ': 'https://www.filmaffinity.com/es/film666035.html', 'El Drogas ': 'https://www.filmaffinity.com/es/film444814.html', 'Vicky el Vikingo y la espada mágica ': 'https://www.filmaffinity.com/es/film148516.html', 'Pinocho ': 'https://www.filmaffinity.com/es/film955709.html', 'Uno para todos ': 'https://www.filmaffinity.com/es/film866421.html', 'Un diván en Túnez ': 'https://www.filmaffinity.com/es/film233453.html', 'After. En mil pedazos ': 'https://www.filmaffinity.com/es/film873946.html', 'Las niñas ': 'https://www.filmaffinity.com/es/film779034.html', 'Antebellum ': 'https://www.filmaffinity.com/es/film790716.html', '100% Wolf: Pequeño gran lobo ': 'https://www.filmaffinity.com/es/film161461.html', 'Tenet ': 'https://www.filmaffinity.com/es/film257249.html', 'La boda de Rosa ': 'https://www.filmaffinity.com/es/film667484.html', 'Trasto, de la mansión a la calle ': 'https://www.filmaffinity.com/es/film651389.html', 'Jurassic World ': 'https://www.filmaffinity.com/es/film843613.html', 'Parque Jurásico (Jurassic Park) ': 'https://www.filmaffinity.com/es/film152490.html', 'Padre no hay más que uno 2: La llegada de la suegra ': 'https://www.filmaffinity.com/es/film262550.html', 'Jurassic World: El reino caído ': 'https://www.filmaffinity.com/es/film283552.html', 'Voces ': 'https://www.filmaffinity.com/es/film784607.html', 'Superagente Makey ': 'https://www.filmaffinity.com/es/film863064.html', '¡Scooby! ': 'https://www.filmaffinity.com/es/film353339.html', 'Urubú ': 'https://www.filmaffinity.com/es/film193699.html'}


    '''

    # Path to webdriver
    browser = webdriver.Chrome(webdriver_path)

    # URL to scrape
    browser.get(pub_url)
    time.sleep(1)
    # Let's retrieve all the elements based on CSS selector: movie-title
    elems = browser.find_elements_by_css_selector(".movie-title [href]")
    links = [elem.get_attribute('href') for elem in elems]
    # names = [elem.get_attribute('textContent') for elem in elems]
    # For convenience, let's generate a hash dictionary with the results: movie_title:movie_URL
    # billboard = dict(zip(names, links))

    browser.quit()
    # return billboard
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
