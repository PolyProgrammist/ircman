# -*- coding: utf-8 -*-
from download_file import download
from jpg2ascii import ascii_from_image
from parsed_search import images_links 

file_name = 'res/telochka.jpg'
query=u'девушка'

url = images_links(query)[20]
download(url, file_name)
ascii_image = ascii_from_image(file_name)
print(ascii_image) 
