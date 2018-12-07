# -*- coding: utf-8 -*-
from download_file import download
from jpg2ascii import ascii_from_image
from google_worker import images_links 

file_name = 'res/temp.jpg'
query = 'девушка png'

urls = images_links(query)
url = urls[1]

print(url)
download(url, file_name)
ascii_image = ascii_from_image(file_name, 170, 'coterm$@')
print(ascii_image)
