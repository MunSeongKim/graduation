#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
#import elasticsearch
import urllib2
import time
import json
from datetime import datetime
import elasticsearch
#from elasticsearch import Elasticsearch

start = time.time()
#Create new file for log
f = open("/home/es/crawl/log/scrap_"+datetime.now().strftime("%Y%m%d%H%M%S")+".log", 'w')
f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Scraping start\n")

#Connect part
es = elasticsearch.Elasticsearch([{'host': '192.168.0.7', 'port': 9200}])
f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Connected Elasticsearch server\n")

#Make Browser object for request to page
browser = webdriver.PhantomJS(executable_path='/home/es/phantomjs/bin/phantomjs')
browser.implicitly_wait(2) # Wait for page load
f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Opened PhantomJS webdriver\n")

#Request to seed page
browser.get("https://section.blog.naver.com/ThemePost.nhn")
f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Complete to bring blogs seed page\n")

#Click the travel subject
menus = browser.find_elements_by_css_selector('div.navigator_category a')
menus[3].click()
time.sleep(0.5) # Wait for page load
f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Complete to move to travel category\n")

#Click the category that is domestic travel
subMenus = browser.find_elements_by_css_selector('div.navigator_category_sub[data-set="hobby"] a')
subMenus[5].click()
time.sleep(0.5)
f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Complete to move to domestic travel page\n")

nextPage = browser.find_elements_by_css_selector('div.pagination > a.button_next')
idx = 1
f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Start to parse each posts\n")
for i in range(0, 2):
	#page has each page elements
	page = browser.find_elements_by_css_selector('div.pagination span a')
	for p in page:
		#Click the page element - move the page
		f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Click the page - " + p.text + "page\n")
		p.click()
		time.sleep(1.5)

		#Save rendered html source
		html = browser.page_source
		#Make the object that is for parsing html source
		blogBS = BeautifulSoup(html, 'html.parser')
		#Scrap each post url
		postLink = blogBS.select('div.list_post_article div.desc a.desc_inner')
		for url in postLink:
			#Transforming to url of real post
			postBS = BeautifulSoup(urllib2.urlopen(str(url['href'])).read(), 'html.parser')
			postUri = "http://blog.naver.com" + postBS.select('frame#mainFrame')[0]['src']

			#Make the object that is for parsing blog post
			contentBS = BeautifulSoup(urllib2.urlopen(str(postUri)).read().decode('ms949', 'utf8'), 'html.parser')

			#Parse to content
			meta = contentBS.select('head meta[property]')
			tmpID = meta[3]['content'].replace("http://blog.naver.com/", "").split("/")
			#Make data object for save
			data = {
				"date"   : datetime.now().strftime("%Y.%m.%d. %H:%M"),
				"author" : meta[8]['content'],
				"title"  : meta[0]['content'],
				"img"    : meta[9]['content'],
				"desc"   : meta[2]['content'],
				"url"    : meta[3]['content'],
				"content": ""
			}
	
			selector = "div#post-view" + tmpID[1] + " p"
			content = contentBS.select(selector)
			for c in content:
				data['content'] += c.getText().strip()+" "
			f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Complate to parse - "+str(tmpID[0]+"_"+tmpID[1])+"\n")
	
			try:
				#Indexing blog post data into elasticsearch
				es.create(index='blogs', doc_type='post', id=str(tmpID[0]+"_"+tmpID[1]), body=data)	
				response = es.transport.perform_request(
								method='GET',
								url='/blogs/queries/_percolate',
								body={ "doc": { "content" : data['content'] } })
	
				for ids in response['matches']:
					es.update(index='areas', doc_type='city', id=ids['_id'],
						body={ "script": "ctx._source.count += 1" })
				f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Complate to percolate - "+str(tmpID[0]+"_"+tmpID[1])+"\n")
				idx += 1
			except elasticsearch.TransportError:
				f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Error - Already exists document\n")
				continue
	nextPage[0].click();
	f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Click the next\n")
browser.quit()
end = time.time()
f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Complate stored which "+str(idx-1)+" posts scrapped\n")
f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] Scrapping end, Process time: " + str(end-start)+"s\n")
f.close()
