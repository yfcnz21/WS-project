from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd
import argparse
import re

PAGE_LIMIT = True

if PAGE_LIMIT:
    pages = 3

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
url = 'http://www.films101.com/years.htm'
driver.get(url)
years_list= [year.get_attribute("href") for year 
                in driver.find_elements(By.XPATH, '//div[@id="yearbx"]//a')]
driver.close()

movie_dataframe = pd.DataFrame(columns=['title', 'year', "director", "country","media"])

pages = len(years_list)
if PAGE_LIMIT:
    pages = 100

movie_info =[]
for year in years_list[:pages]:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(year)
    table = driver.find_elements(By.XPATH, '//table[@class="lstdta"]//tr')
    for row in table:
        title    = row.find_elements(By.TAG_NAME, "td")[1].text
        year     = row.find_elements(By.TAG_NAME, "td")[2].text
        director = row.find_elements(By.TAG_NAME, "td")[3].text
        country  = row.find_elements(By.TAG_NAME, "td")[4].text
        media    = row.find_elements(By.TAG_NAME, "td")[5].text
        movie = {
              'title'    : title,    
              'year'     : year  ,   
              "director" : director, 
              "country"  : country  ,
              "media"    : media    ,
          }
        movie_dataframe = movie_dataframe.append(movie, ignore_index=True)
    driver.close()
movie_dataframe.to_csv('movies_sel.csv')
