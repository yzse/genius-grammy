# %%
from selenium.webdriver.common.keys import Keys
# auxiliary functions modified by Luis.
import sys
import calendar
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
import re
from selenium.webdriver.support.ui import Select
import random
import time
from selenium import webdriver
import os
import numpy as np
import importlib
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup

#%%
# get grammy links
# note that the url format changes between the 59th & 60th grammy
# https://www.grammy.com/awards/59th-annual-grammy-awards
# https://www.grammy.com/awards/60th-annual-grammy-awards-2017

grammy_urls = []

for i in range(1, 66):
    if i < 60:
        if i % 10 == 1 and i != 11:
            url = 'https://www.grammy.com/awards/{}st-annual-grammy-awards'.format(i)
        elif i % 10 == 2 and i != 12:
            url = 'https://www.grammy.com/awards/{}nd-annual-grammy-awards'.format(i)
        elif i % 10 == 3 and i != 13:
            url = 'https://www.grammy.com/awards/{}rd-annual-grammy-awards'.format(i)
        else:
            url = 'https://www.grammy.com/awards/{}th-annual-grammy-awards'.format(i)
    else:
        if i % 10 == 1 and i != 11:
            url = 'https://www.grammy.com/awards/{}st-annual-grammy-awards-{}'.format(i, i+1957)
        elif i % 10 == 2 and i != 12:
            url = 'https://www.grammy.com/awards/{}nd-annual-grammy-awards-{}'.format(i, i+1957)
        elif i % 10 == 3 and i != 13:
            url = 'https://www.grammy.com/awards/{}rd-annual-grammy-awards-{}'.format(i, i+1957)
        else:
            url = 'https://www.grammy.com/awards/{}th-annual-grammy-awards-{}'.format(i, i+1957)
    grammy_urls.append(url)


# %%
# Starting code to scrape grammys website
dfolder = 'out'
link = 'https://www.grammy.com/awards/65th-annual-grammy-awards-2022'

executable_path = "/usr/local/bin/chromedriver"
browser = webdriver.Chrome(executable_path)
browser.get(link)

time.sleep(4)
print('clicking...')

records = browser.find_elements_by_xpath('//*[@id="627"]/div[2]/div/div[2]/div')[-1].text

# %% 
# parse

# get grammy iteration
year = browser.find_elements_by_xpath('//*[@id="__next"]/div/main/section/section[1]/div/div[1]/h2')[-1].text

# convert to year
year = int(re.findall("\d+", year)[0]) + 1957

winner, nominee = records.split("\nNOMINEES\n")
winner_record, winner_artist = winner.split('\n')[1:3]

titles = []
artists = []

# Use regex to extract titles and artists and append to corresponding lists
for match in re.findall(r'"(.+?)"\n\+\n(.+?)\n', nominee):
    title, artist = match
    titles.append(title)
    artists.append(artist)

# Create a pandas data frame with the extracted information
winner = {'title': [winner_record.strip('"')], 'artist': [winner_artist], 'winner': 1, 'year': year}
nominees = {'title': titles, 'artist': artists, 'winner': 0, 'year': year}

winner_df = pd.DataFrame(winner)
nominees_df = pd.DataFrame(nominees)
df = winner_df.append(nominees_df)

# Print the dataframe
print(df)

# %%
