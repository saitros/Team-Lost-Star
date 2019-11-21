import requests, json


UPLOAD_URL = "https://api.imgur.com/3/image"

def img_upload(img_url=None):
    header = {
        'Authorization': 'Client-ID 02af95d016f943d'
    }
    data = {
        'image' : img_url
    }
    res = requests.post(url=UPLOAD_URL, data=data, headers= header)
    return res.json()['data']['link']


if __name__ == '__main__':
    print(img_upload("https://api.telegram.org/file/bot1039143523:AAHTngxT5pk8WG_XSh562-vHoOvVxQj1fGI/photos/file_16.jpg"))


