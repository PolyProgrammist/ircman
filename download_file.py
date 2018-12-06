import requests

def download(url, file_name):
    r = requests.get(url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)

if __name__ == "__main__":
    download('http://voronezh-room.ru/uploads/voronezh/2017/06/hwM7qtlutv0.jpg', 'res/telochka.jpg')
