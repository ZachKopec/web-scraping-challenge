#Dependency
import pandas as pd
import requests

from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

#initialyzing the browser
def init_browser():
    #load the crome driver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

#scraping   
def scrape():
    #load the crome driver
    browser = init_browser()
    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    #find latest News Title and Paragraph
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
        
    arts = soup.find_all('div', class_='content_title')
    bdys = soup.find_all('div', class_='article_teaser_body')

    art_hdr_list = []
    art_bdy_list = []

    for art in arts:
            
        mains = art.find_all('a')
            
        for main in mains:
            title = main.text.strip()
            art_hdr_list.append(title)
            
    for bdy in bdys:
        body = bdy.text.strip()
        art_bdy_list.append(body)

    article_hdr_1 = art_hdr_list[0]
    article_bdy_1 = art_bdy_list[0]

    #visit the URL for the JPL Featured Space Image by splinter
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    farts = soup2.find_all('a', class_='button fancybox')

    for fart in farts:
        img_url = fart["data-fancybox-href"]
        
        base_url = 'https://www.jpl.nasa.gov'
        
        full_img_url = base_url + img_url
        
    #visit the Mars Facts web url
    url3 = 'https://space-facts.com/mars/'
    browser.visit(url3)
    
    tables = pd.read_html(url3)
    df = tables[0]
    html_table = df.to_html()

    #visit the Mars Hemispheres web url
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    html4 = browser.html
    soup4 = BeautifulSoup(html4, 'html.parser')

    hemisphere_img_urls = []
    base_url = 'https://astrogeology.usgs.gov'

    items = soup4.find_all('div', class_='item')

    for item in items:
        title = item.find("h3").text
        img_url = item.find("a",class_="itemLink product-item")["href"]
        
        browser.visit(base_url + img_url)
        
        image_html = browser.html
        soup5 = BeautifulSoup(image_html, 'html.parser')
        
        final_img_url = base_url + soup5.find("img", class_="wide-image")["src"]
        
        hemisphere_img_urls.append({"title": title, "image_url": final_img_url})
        
    Mars_Hemispheres_data = {
        "Mars_News_Title": article_hdr_1,
        "Mars_News_Paragraph": article_bdy_1,
        "Mars_Featured_Image": full_img_url,
        "Mars_Facts": html_table,
        "Mars_Hemisphere_Images": hemisphere_img_urls
    }
    #browser.quit()
    
    return Mars_Hemispheres_data

