# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import requests
import json
import time
API_KEY = '809923506:AAHvl4bNcKd32rltJ7Vlje6tz_uBHYcXfag'
# Flask 객체를 생성 __name__ 을 인수로 입력


#{'chat_id': {'나이': 26,
#  '성별': '남자',
#  '여행국가': '스페인',
#  '여행도시': '바르셀로나',
#  '사진': 'URL',
#  '카톡ID': 'kakaotalk',
#  '여행기간': '19.12.01-19.12.18',
#  '관심태그': '#캄프누 #메시 #파에야 #바르셀로나'}}
UserInfo = {}
app = Flask(__name__)
send_URL =  'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY) 
def parse_message(message):

    chat_id = message['message']['chat']['id']
    msg = message['message']['text']
    
    return chat_id, msg
def send_message(chat_id, text):

    params = {'chat_id': chat_id, 'text': text}
    
    response = requests.post(send_URL, json=params)
    print(response)
    print("SendMessage")
    return response

def IsUserNew(chat_id):
    if chat_id not in UserInfo.keys():
        UserInfo[chat_id]={}
    else:
        pass

    return 0

def UserAge(chat_id):
    send_message(chat_id,text = "너의 나이를 입력해줘  EX) 25")
    switch = True
    while(switch):
        if request.method == 'POST':
            message = request.get_json()
            chat_id, msg = parse_message(message)
            switch = False
        else:
            pass

    UserInfo[chat_id]["AGE"] = msg
    return 0

def UserSex(chat_id):
    send_message(chat_id,text = "너의 성별을 버튼에서 골라줘")
    switch = True
    while(switch):
        Select_two_Menu(chat_id,"text","남자","여자")
        if request.method == 'POST':
            message = request.get_json()
            chat_id, msg = parse_message(message)
            switch = False
        else:
            pass
    UserInfo[chat_id]["SEX"] = msg
    return 0

def UserTravelCountry(chat_id):
    send_message(chat_id,text = "너의 여행하는 나라를 입력해줘")
    switch = True
    while(switch):
        if request.method == 'POST':
            message = request.get_json()
            chat_id, msg = parse_message(message)
            switch = False
        else:
            pass

    UserInfo[chat_id]["COUNTRY"] = msg
    return 0

def UserTravelCity(chat_id):
    send_message(chat_id,text = "너의 여행하는 도시를 입력해줘")
    switch = True
    while(switch):
        if request.method == 'POST':
            message = request.get_json()
            chat_id, msg = parse_message(message)
            switch = False
        else:
            pass

    UserInfo[chat_id]["CITY"] = msg
    return 0

def UserPhoto(chat_id):
    send_message(chat_id,text = "너의 사진를 입력해줘")
    switch = True
    while(switch):
        if request.method == 'POST':
            message = request.get_json()
            chat_id, msg = parse_message(message)
            switch = False
        else:
            pass
    UserInfo[chat_id]["PHOTO"] = msg
    return 0

def UserKakaoID(chat_id):
    send_message(chat_id,text = "너의 카카오톡 아이디를 입력해줘")
    switch = True
    while(switch):
        if request.method == 'POST':
            message = request.get_json()
            chat_id, msg = parse_message(message)
            switch = False
        else:
            pass
    UserInfo[chat_id]["KAKAOID"] = msg
    return 0

def UserTravelDate(chat_id):
    send_message(chat_id,text = "너의 여행하는 날짜를 입력해줘")
    switch = True
    while(switch):
        if request.method == 'POST':
            message = request.get_json()
            chat_id, msg = parse_message(message)
            switch = False
        else:
            pass
    UserInfo[chat_id]["DATE"] = msg
    return 0

def UserTag(chat_id):
    send_message(chat_id,text = "너를 잘 표현하는 태그들을 적어봐")
    switch = True
    while(switch):
        if request.method == 'POST':
            message = request.get_json()
            chat_id, msg = parse_message(message)
            switch = False
        else:
            pass
    UserInfo[chat_id]["TAG"] = msg
    return 0

def Select_two_Menu(chat_id,text,menu1,menu2):
    keyboard = {                                        # Keyboard 형식
            'keyboard':[[{'text': menu1},
                {'text': menu2}]],

            'one_time_keyboard' : True
            }
        
    params = {'chat_id':chat_id, 'text': text, 'reply_markup' : keyboard}
    requests.post(send_URL, json=params)
    return 0

def FirstScreen(chat_id,text):
    send_message(chat_id, text = "안녕! 난 여행을 좋아하는 로스야! 뭐하러왔어? ")
    
    Select_two_Menu(chat_id,text,"동행을 찾아볼래","여행정보 알려줘")
    
    return 0

def 동행정보입력(chat_id):
    send_message(chat_id,text = "지금부터 동행을 찾기위해 너에대해 알아볼게")
    IsUserNew(chat_id)
    UserAge(chat_id)
    UserSex(chat_id)
    UserTravelCountry(chat_id)
    UserTravelCity(chat_id)
    UserPhoto(chat_id)
    UserKakaoID(chat_id)
    UserTag(chat_id)

# 경로 설정, URL 설정
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        message = request.get_json()
        chat_id, msg = parse_message(message)
        if msg == "/start":
            FirstScreen(chat_id,"text")
        elif msg =="동행을 찾아볼래":
            send_message(chat_id,"동행을 찾고싶구나?")
            동행정보입력(chat_id)

        elif msg =="여행정보 알려줘":
            send_message(chat_id,"여행정보를 알고싶구나?")

        else:
            send_message(chat_id,"미안해 다시 말해줄래 ㅠ.ㅠ")

        return Response('ok', status=200)

    else:
        pass

    


if __name__ == '__main__':
    app.run(port=5000)

