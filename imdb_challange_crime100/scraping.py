import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv

# page = requests.get('https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=crime&sort=user_rating,desc&start=51&ref_=adv_nxt')
# print(page)
# soup = BeautifulSoup(page.content, "html.parser")

def get_movies(url, filename):
    page = requests.get(url)
    print(page)
    soup = BeautifulSoup(page.content, "html.parser")
    container = soup.find(id="main")
    movies = container.find_all(class_='lister-item mode-advanced')
    names = []
    descs = []
    rel_dates = []
    dir_names = []
    ratings = []
    durations = []
    genres = []
    stars = []
    stars_temp = []
    descriptions = []
    # filming_dates = []

    #setting variables
    all_movies = soup.find_all('div', class_='lister-item-content')
    detail = all_movies[0].find_all('a')
    
    #scrape simple information out of the details
    for item in range(len(movies)):
        #get movie lenght
        runtime = movies[item].find(class_='runtime').get_text().strip(' min')
        durations.append(runtime)
        #get genre
        genre = movies[item].find(class_='genre').get_text().strip()
        genres.append(genre)
        #get release date
        rel_date = movies[item].find(class_='lister-item-year text-muted unbold').get_text().strip('() I')
        rel_dates.append(rel_date)
        #get imdb rating
        rating = movies[item].find(class_='inline-block ratings-imdb-rating').get_text().strip()
        ratings.append(rating)
        #get movie title
        names.append(all_movies[item].find_all('a')[0].get_text().strip())
        #get director
        dir_names.append(all_movies[item].find_all('a')[12].get_text().strip())
        #get stars
        stars_temp = all_movies[item].find_all('a')[13:17]
        movie_stars = []
        for star in stars_temp:
            movie_stars.append(star.get_text().strip("[]'"))
        stars.append(movie_stars)
        #get descriptions
        

        

    
    df = pd.DataFrame({'title': names, 'release_year': rel_dates, 'director': dir_names, 'rating': ratings, 'duration': durations, 'genre': genre, 'stars': stars})

    return df.to_csv(filename, index=False)



get_movies('https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=crime&sort=user_rating,desc&start=51&ref_=adv_nxt', 'test')
