# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import urllib2
import time

#Make Browser object for request to page
browser = webdriver.PhantomJS()
browser.implicitly_wait(2) # Wait for page load

#Request to seed page
browser.get("https://section.blog.naver.com/ThemePost.nhn")

#Click the travel subject
menus = browser.find_elements_by_css_selector('div.navigator_category a')
menus[3].click()

subMenus = browser.find_elements_by_css_selector('div.navigator_category_sub[data-set="hobby"] a')
subMenus[5].click()
time.sleep(0.5)
'''
img = browser.find_elements_by_css_selector('div.thumbnail_author > img.img_author')
for i in img:
	print(i.get_attribute('src'))
	print()

'''
'''
nextPage = browser.find_elements_by_css_selector('div.pagination > a.button_next')
print(nextPage[0].text)
nextPage[0].click
time.sleep(0.5)
nextPage = browser.find_elements_by_css_selector('div.pagination > a.button_next')
print(nextPage[0].text)
'''


url = 'http://blog.naver.com/PostView.nhn?blogId=blog0149&logNo=221131679173&redirect=Dlog&widgetTypeCall=true&directAccess=false'

post = BeautifulSoup(urllib2.urlopen(str(url)).read().decode('ms949', 'utf8'), 'html.parser')

meta = post.select('head meta[property]')
'''
for m in meta:
	print(m['content'])
'''

print(meta[8]['content'])
print(meta[9]['content'])
browser.close()
