from download_file import download
from jpg2ascii import ascii_from_image


def get_correct_image_url(urls, file_name):
    for url in urls:
        try:
            download(url, file_name)
            ascii_from_image(file_name, 50)
            return url
        except:
            continue
