# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:00:58 2018

@author: kerem durak
"""

import sys
from selenium import webdriver
import time
import requests
from io import open as iopen

# CHANGE BELOW LINE FOR YOUR KEYWORD
search_keyword = 'flower'


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
search = search_keyword.replace(' ','%20')
url = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
driver.get(url)

for i in range(0,10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
for i in range(0,10):
    try:
        nextbutton = driver.find_element_by_class_name('_kvc')
        nextbutton.click()
        time.sleep(1)
    except Exception:
        continue
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)


#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:     #If the Current Version of Python is 3.0 or above
        import urllib.request    #urllib library for Extracting web pages
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:                        #If the Current Version of Python is 2.x
        import urllib.request as urllib2
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"


#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    s = s.decode()
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            if('html' in str(item)):
                break
            print(str(item))
            items.append(item)      #Append all the links in the list named 'Links'
            time.sleep(0.1)        #Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items

def downloader(image_url, name):
    file_extension = 'jpg'
    full_file_name = str(name) + '.' + str(file_extension)
    try:
        i = requests.get(image_url)
    except Exception:
        return
    if ('photo_unavailable' in i.url):
        return
    if i.status_code == requests.codes.ok:
        with iopen(full_file_name, 'wb') as file:
            file.write(i.content)  


page_html = driver.page_source
page_html2 = (page_html).encode()
items = []
raw_html =  (download_page(url))
items = items + (_images_get_all_items(page_html2))
print ("Total Image Links = "+str(len(items)))

    
errorCount = 0
downloadedCount = 0
for index, item in enumerate(items):
    try:
        print(item)
        downloader(item, search_keyword+str(downloadedCount))
        downloadedCount += 1
    except requests.ConnectionError:
        errorCount+=1
        continue  
print(str(downloadedCount)+" items have been downloaded. " + str(errorCount) + ' items could not be downloaded.')

    
