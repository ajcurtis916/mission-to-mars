#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #set executable path/initiate headless driver for deployment
    executable_path={'executable_path':ChromeDriverManager().install()}
    browser=Browser('chrome',**executable_path, headless=True)

    #set variables
    news_title, news_paragraph=mars_news(browser)

    #run all scraping functions and store results in dictionary
    data= {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    
    #stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    #visit the mars nasa news site
    url='https://redplanetscience.com/'
    browser.visit(url)

    #delay for loading page
    #searching for elements with the tag 'div' and attribute 'list_text'
    browser.is_element_present_by_css('div.list_text',wait_time=5)

    #convert the browser html to a soup object and quit the browser
    html=browser.html
    news_soup=soup(html,'html.parser')

    #add try/except for error handling
    try:

        #variable to look for the div tag
        slide_elem=news_soup.select_one('div.list_text')
        #slide_elem.find('div',class_='content_title')

        #use parent element to find the first 'a' tag and save it as 'news_title'
        #returns most recent/first title because page is dynamic
        news_title=slide_elem.find('div',class_='content_title').get_text()

        #use the parent element to find the paragraph text
        news_p=slide_elem.find('div',class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None    

    return news_title, news_p

def featured_image(browser):

    #visit featured image url
    url='https://spaceimages-mars.com/'
    browser.visit(url)

    #find and click the full image button
    full_image_elem=browser.find_by_tag('button')[1]
    full_image_elem.click()

    #parse the resulting html with soup
    html=browser.html
    img_soup=soup(html, 'html.parser')

    #add try/accept for error handling
    try:
        #find the relative image url
        img_url_rel=img_soup.find('img',class_='fancybox-image').get('src')

    except AttributeError:
        return None    

    #use base url to create an absolute url
    img_url=f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():

    #add try/except for error handling w/ Pandas' library
    try:
        # visit Mars Facts and scrape into df
        df=pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None    

    #assign columns and set index of dataframe
    df.columns=['description','Mars','Earth']
    df.set_index('description',inplace=True)

    #return df to html code, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__=="__main__":
    #if running as script, print scraped data
    print(scrape_all())