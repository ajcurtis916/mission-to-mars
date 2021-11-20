#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#set executable path
executable_path={'executable_path':ChromeDriverManager().install()}
browser=Browser('chrome',**executable_path, headless=False)

url='https://redplanetscience.com/'
browser.visit(url)

#delay for loading page
#searching for elements with the tag 'div' and attribute 'list_text'
browser.is_element_present_by_css('div.list_text',wait_time=1)

#set up html parser
html=browser.html
news_soup=soup(html,'html.parser')
#variable to look for the div tag
slide_elem=news_soup.select_one('div.list_text')

slide_elem.find('div',class_='content_title')

#use the parent element to find the first 'a' tag and save it as 'news_title'
#returns most recent/first title because page is dynamic
news_title=slide_elem.find('div',class_='content_title').text
news_title

#use the parent element to find the paragraph text
news_p=slide_elem.find('div',class_='article_teaser_body').text
news_p

## Featured Images
#visit url
url='https://spaceimages-mars.com/'
browser.visit(url)

#find and click the full image button
full_image_elem=browser.find_by_tag('button')[1]
full_image_elem.click()

#parse the resulting html with soup
html=browser.html
img_soup=soup(html, 'html.parser')

#find the relative image url
img_url_rel=img_soup.find('img',class_='fancybox-image').get('src')
img_url_rel

#use base url to create an absolute url
img_url=f'https://spaceimages-mars.com/{img_url_rel}'

#print relative/featured image url
img_url

## Mars Facts

df=pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description','Mars','Earth']
df.set_index('description',inplace=True)
df

#return df to html code
df.to_html()

#end session
browser.quit()