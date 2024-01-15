from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
def chromedriver():
    try:
        driver.quit()
    except Exception as e:
        print(e)
        
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    #option.add_argument('--disable-gpu')
    option.add_argument('lang=ko_KR')
    driver = webdriver.Chrome(options=option)
    return driver
driver = chromedriver()
def getUrl(mode,query):
    start = time.time()
    global driver
    #option = webdriver.ChromeOptions()
    #option.add_argument('headless')
    #option.add_argument('--disable-gpu')
    #option.add_argument('lang=ko_KR')
    #driver = webdriver.Chrome(options=option)
   
    if mode == 1:
        max = 2
       
    url = f"https://www.youtube.com/results?search_query={query}"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml') 
    tags = soup.find_all('ytd-video-renderer',
                         class_='style-scope ytd-item-section-renderer')
    rank = 1
    for i in tags:
        title = i.find(
            class_='yt-simple-endpoint style-scope ytd-video-renderer', id='video-title')['title']
        name = i.find(
            class_='yt-simple-endpoint style-scope yt-formatted-string').text
        name = name.replace('\n', '')

        link = i.find(
            class_='yt-simple-endpoint style-scope ytd-video-renderer', id='video-title')['href']
        imgLink = link
        re1 = imgLink.split('=')
        re2 = re1[1].split('&')
        musicTime = i.find(
            class_='yt-simple-endpoint style-scope ytd-video-renderer', id='video-title')['aria-label']
        print(musicTime)
        imgurl = f'https://img.youtube.com/vi/{re2[0]}/0.jpg'
        link = 'https://www.youtube.com'+link
        imgLink = f'https://img.youtube.com/vi/{link[32:]}/0.jpg'
        rank += 1
        if rank == max:break
    #driver.close()
    return title,name,link,imgurl

def auto():
    autoList = []
    global driver
    #option = webdriver.ChromeOptions()
    #option.add_argument('headless')
    #option.add_argument('--disable-gpu')
    #option.add_argument('lang=ko_KR')
    #driver = webdriver.Chrome(options=option)
    max = 10
    url = f"https://www.youtube.com/playlist?list=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m"
        
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml') 
    tags = soup.find_all('ytd-playlist-video-renderer',
                         class_='style-scope ytd-playlist-video-list-renderer')
    rank = 1
    for i in tags:
        title = i.find(
            class_='yt-simple-endpoint style-scope ytd-playlist-video-renderer', id='video-title')['title']
        name = i.find(
            class_='yt-simple-endpoint style-scope yt-formatted-string').text
        name = name.replace('\n', '')

        link = i.find(
            class_='yt-simple-endpoint style-scope ytd-playlist-video-renderer', id='video-title')['href']
        imgLink = link
        re1 = imgLink.split('=')
        re2 = re1[1].split('&')
        imgurl = f'https://img.youtube.com/vi/{re2[0]}/0.jpg'
        link = 'https://www.youtube.com'+link
        imgLink = f'https://img.youtube.com/vi/{link[32:]}/0.jpg'
        autoList.append([title,name,link,imgurl])
        rank += 1
        if rank == max:break
    #driver.close()
    return autoList


getUrl(1,'비의랩소디')



