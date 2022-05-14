import requests
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

#setting the limit of pages

PAGE_LIMIT = True


titles = []
years = []
directors = []
country = []
media = []


def get_years_list():
    years_list = []
    url_movie_years = 'http://www.films101.com/years.htm'
    page = requests.get(url_movie_years)
    soup = BeautifulSoup(page.text, 'html.parser')
    year_tags = soup.find('div', id="yearbx")
    years_list = [tag.getText() for tag in year_tags.find_all('a')]
    if PAGE_LIMIT:
        years_list = years_list[0:100]
    return years_list

def parse_page(year=2022):
    movie_params_to_movie = {}
    url = f"http://www.films101.com/y{year}r.htm"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    a = soup.find('table', class_='lstdta')
    for movie in a.find_all('tr'):
        titles.append(movie.find('td', class_='zt1').getText())
        years.append(movie.find('td', class_='zy1').getText())
        directors.append(movie.find('td', class_='zd1').getText())
        country.append(movie.find('td', class_='zc1').getText())
        media.append(movie.find('td', class_='z').getText())


def write_to_csv():
    movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'director': directors,
    'country': country,
    'media': media,
    })
    return movies


def main():
    years_list = get_years_list()
    #print(years_list)
    for year in years_list:
        parse_page(year)
    movies = write_to_csv()
    movies.to_csv('movies.csv')
    
    
if __name__ =="__main__":
    main()