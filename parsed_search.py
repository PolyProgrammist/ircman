from bs4 import BeautifulSoup
import requests
import re
import urllib
import os
import json
import urllib.parse
#https://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search
def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')

def images_links(query):
    query= query.split()
    query='+'.join(query)
    query = urllib.parse.quote(query, encoding='utf-8')
    url=u"https://www.google.co.in/search?q=" + query + u"&source=lnms&tbm=isch"
    header={u'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }
    soup = get_soup(url,header)

    ActualImages=[]# contains the link for Large original images, type of  image
    for a in soup.find_all("div",{"class":"rg_meta"}):
        link=json.loads(a.text)["ou"]
        ActualImages.append(link)
    return ActualImages
