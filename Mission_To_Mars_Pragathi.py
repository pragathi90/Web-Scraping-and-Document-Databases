
import time
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

mars_information = {}

def get_news(browser):
    browser = init_browser()
    
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    html = browser.html
    
    soup = BeautifulSoup(html, 'html.parser')



    news_title = soup.find('div', class_='content_title')

    
    news_p = soup.find('div', class_='article_teaser_body')

    
    mars_information['news_title'] = news_title.text
    mars_information['news_paragraph'] = news_p.text

   
    browser.quit()
   
    return mars_information


def get_featured_image(browser):
    browser = init_browser()
            
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)

    html_images = browser.html
    soup = BeautifulSoup(html_images, 'html.parser')

    featured_url = soup.find("img", class_="thumb")["src"]
    featured_image_url = f'https://www.jpl.nasa.gov{featured_url}'
    featured_image_url

    mars_information['featured_image_url'] = featured_image_url

   
    browser.quit()
   
    return mars_information

def get_latest_weather(browser):
    browser = init_browser()

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    html_weather = browser.html

    soup = BeautifulSoup(html_weather, 'html.parser')

    mars_weather = soup.find('p',class_='TweetTextSize')
    
    mars_information['mars_weather'] = mars_weather
    #print('mars_weather = '+ mars_weather.text)

    browser.quit()
   
    return mars_information




def get_facts(browser):

    browser = init_browser()

    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    mars_data = pd.read_html(facts_url)

    mars_data = pd.DataFrame(mars_data[0])

    mars_facts = mars_data.to_html(header = False, index = False)

    #print(mars_facts)
    mars_information['mars_facts'] = mars_facts

    browser.quit()
   
    return mars_information




def get_hemispheres(browser):

    browser = init_browser()

    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemispheres_url = 'https://astrogeology.usgs.gov'

    browser.visit(astro_url)


    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')
    array_url = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    



    for h in array_url: 
        title = h.find('h3').text
        p_img_url = h.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_url + p_img_url)
        
        p_img_url = browser.html
        soup = BeautifulSoup( p_img_url, 'html.parser')
        
        image_url = hemispheres_url + soup.find('img', class_='thumb')['src']
        #hemisphere_image_urls.append({'title' : title, 'img_url' : image_url})

        
        hem_data=dict({'title':title, 'img_url':image_url})
        hemisphere_image_urls.append(hem_data)
        

    mars_information['hemisphere_image_urls'] = hemisphere_image_urls
    #hemisphere_image_urls

    browser.quit()
            
    return mars_information

