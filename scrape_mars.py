# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    mars_data_dict = {}

    # Retrieve latest NASA Mars news headline
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    response = requests.get(nasa_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_title = soup.find('div', class_="content_title").text
    news_desc = soup.find('div', class_="rollover_description_inner").text

    # Retrieve Mars Images 
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    click_thru_html = browser.html
    soup = BeautifulSoup(click_thru_html, 'html.parser')
    featured_image_url = "https://www.jpl.nasa.gov/" + soup.find('figure', class_='lede').a['href']

    # Retrieve Twitter data 
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find('p', class_="tweet-text").text

    # Retrieve Mars Facts, convert to a dataframe, and save as an html table
    mars_facts_url = "http://space-facts.com/mars/"
    tables = pd.read_html(mars_facts_url)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ['Fact', 'Value']
    mars_facts_df = mars_facts_df.set_index('Fact')
    mars_facts_df.index.name = None
    mars_facts = mars_facts_df.to_html()

    # Manually retrieve Mars Hemispheres images from https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    hemisphere_image_urls = [{'title': 'Cerberus Hemisphere', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},
          {'title': 'Schiaparelli Hemisphere', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
          {'title': 'Syrtis Major Hemisphere', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},
          {'title': 'Valles Marineris Hemisphere', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}
         ]
         
    # Save all data retrieved to a dictionary
    mars_data_dict = {
        "latest_hdl_title": news_title,
        "latest_hdl_description": news_desc,
        "mars_high_res_img": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts":  mars_facts,
        "mars_imgs": hemisphere_image_urls
    }

    browser.quit()

    return mars_data_dict
