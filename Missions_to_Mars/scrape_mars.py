#Dependencies
import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

#Initialize browser
def init_browser():
    #Load chrome driver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

#scraping   
def scrape():
    #Set browser variable to load chrome driver
    browser = init_browser()
    
    ###First required url to find latest news title and paragraph###
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #Variables to begin scraping
    arts = soup.find_all('div', class_='content_title')
    bdys = soup.find_all('div', class_='article_teaser_body')

    #Empty lists to hold data
    art_hdr_list = []
    art_bdy_list = []

    #Loop through everything found in 'arts'
    for art in arts:
        
        #Variable to find 'a' tags in 'arts'
        mains = art.find_all('a')
            
        #Loop through 'a' tags in 'mains
        for main in mains:
            #Set variable of the found text and append in to title list
            title = main.text.strip()
            art_hdr_list.append(title)
            
    #Loop through everything found in 'bdys'
    for bdy in bdys:
        #Set variable of the found text and append in to body text list
        body = bdy.text.strip()
        art_bdy_list.append(body)

    #Record the first title and body text in variables for usage
    article_hdr_1 = art_hdr_list[0]
    article_bdy_1 = art_bdy_list[0]

    ###End first url###

    ###Second required url to find featured image###
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    #Variable to begin scraping
    imgs = soup2.find_all('a', class_='button fancybox')

    #Loop through everything found in 'imgs'
    for img in imgs:
        #Record image url and combine with base url
        img_url = img["data-fancybox-href"]
        base_url = 'https://www.jpl.nasa.gov'
        full_img_url = base_url + img_url

    ###End second url###
        
    ###Third required url to find mars facts###
    url3 = 'https://space-facts.com/mars/'
    browser.visit(url3)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    
    #Read html into variable, convert to dataframe & then to html table
    tables = pd.read_html(url3)
    df = tables[0]
    html_table = df.to_html()

    ###End third url###

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
    
    browser.quit()
    
    return Mars_Hemispheres_data

