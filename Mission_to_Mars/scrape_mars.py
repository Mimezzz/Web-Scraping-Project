from typing import Text
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    Mars_News_dict = scrape_title()
    Mars_Featured_Image_dict = scrape_featured_image()
    Mars_Fact_dict = scrape_table()
    Mars_Hemispheres_dict = scrape_hemi_img()

    mars_dict = {**Mars_News_dict, **Mars_Featured_Image_dict, **Mars_Fact_dict, **Mars_Hemispheres_dict}

    return mars_dict


def scrape_title():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    url = "https://redplanetscience.com/"
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find('div',class_='content_title').text
    # print(news_title)
    news_info = soup.find('div',class_='article_teaser_body').text
    # print(news_info)
    browser.quit()
    Mars_News_dict = {}
    Mars_News_dict['news_title'] = news_title
    Mars_News_dict['news_info'] = news_info

    return Mars_News_dict



# Scrape featured img
def scrape_featured_image():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    time.sleep(2)
    html = browser.html
    soup = bs(html, "html.parser")
    image=soup.find('img',class_="headerimage fade-in")['src']
#     print(image)
    img_url=url+str(image)
    # print(img_url)
    browser.quit()
    Mars_Featured_Image_dict={}
    Mars_Featured_Image_dict['featured_image_url']=img_url
    return Mars_Featured_Image_dict


def scrape_table():
    url='https://galaxyfacts-mars.com/'
    tables=pd.read_html(url)
    df=tables[0]
    df.columns=['Mars-Earth', 'Mars','Earth']
    df=df.set_index('Mars-Earth')

    html=df.to_html()
    Mars_Fact_dict= {'table_html': html}
    return Mars_Fact_dict
    



# Scrape hemisphere's images
def scrape_hemi_img():  
    url_list=['https://marshemispheres.com/cerberus.html',
          'https://marshemispheres.com/schiaparelli.html',
           'https://marshemispheres.com/syrtis.html',
           'https://marshemispheres.com/valles.html']

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    
    img_list=[]
    
    base_url='https://marshemispheres.com/'
    for url in url_list:
        img_dict={}
        browser.visit(url)
        time.sleep(2)
        html = browser.html
        soup = bs(html, "html.parser")
        title = soup.find('h2',class_='title').text
        img_dict['title']=title
        new_url=base_url+str(soup.find('img',class_='wide-image')['src'])
        img_dict['img_url']=new_url
        img_list.append(img_dict)
        browser.back()

    browser.quit()
    
    Mars_Hemispheres_dict={}
    Mars_Hemispheres_dict['img_urls']=img_list
    
    return Mars_Hemispheres_dict  
            



