from download_file import download
from jpg2ascii import ascii_from_image


url = 'http://voronezh-room.ru/uploads/voronezh/2017/06/hwM7qtlutv0.jpg'
file_name = 'res/telochka.jpg'

download(url, file_name)
print(ascii_from_image(file_name)) 
