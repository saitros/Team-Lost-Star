import requests, json


UPLOAD_URL = "https://api.imgur.com/3/image"

def img_upload(img_url=None):
    header = {
        'Authorization': 'Client-ID 02af95d016f943d'
    }
    data = {
        'image' : 'http://engineering.vcnc.co.kr/images/2016/05/old_architecture.png'
    }
    res = requests.post(url=UPLOAD_URL, data=data, headers= header)
    return res.json()['data']['link']


if __name__ == '__main__':
    print(img_upload())


