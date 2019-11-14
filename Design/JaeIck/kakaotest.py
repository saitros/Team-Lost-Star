from flask import Flask, request, jsonify
import sys
app = Flask(__name__)
USERINFO = {"USER1":{'Flag': 5, 'Sex': '여자', 'Age': '25', 'Country': '스페인', 'City': '바르셀로나', 'Date': '191115~191118','Photo':'http://dn-m.talk.kakao.com/talkm/bl3pyYUSIOW/7W4dKnjongiKIxu3XkIGf0/i_4z0ltufqhvph1.jpeg'},
            "USER2":{'Flag': 5, 'Sex': '남자', 'Age': '22', 'Country': '스페인', 'City': '바르셀로나', 'Date': '191115~191118','Photo':'http://dn-m.talk.kakao.com/talkm/bl3pyUdR9s1/Gr6VQYRpAdR5UY17uo6u61/i_djwoz2tu3ln6.jpeg'}}
#flag 0 = ID만등록된상황
#flag 1 = 성별까지 등록된 상황
#flag 2 = 나이까지 등록된 상황
#flag 3 = 나라까지 등록된 상황
#flag 4 = 도시까지 등록된 상황
#flag 5 = 사진등록 할 지 안할지
#flag 6 = 모두 등록된 상황

#간단한 메시지를 보내는 함수
def send_message(message):
    message = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText":{
                            "text":"{}".format(message)
                        }
                    }
                ]
            }
        }
    return message

#버튼이 2개짜리 버튼을 만들어 보내는 함수
def Send_Button(message,button1,button2):
    button = {
        "version" : "2.0",
        "template" : {
            "outputs":[
                {
                    "basicCard":{
                        "description":"{}".format(message),
                
                        "buttons":[
                            {
                                "action":"message",
                                "label":"{}".format(button1),
                                "messageText" : "{}".format(button1)
                            },
                            {
                                "action":"message",
                                "label":"{}".format(button2),
                                "messageText":"{}".format(button2)
                            }                                
                        ]   
                    }
                }
            ]
        }
    }
    return button
   
def UserSex():

    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    USERINFO[user_id]['Sex']=user_answer

    print(USERINFO)
    return 0

def UserAge():

    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    USERINFO[user_id]['Age']=user_answer

    print(USERINFO)
    return 0

def UserCountry():

    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    USERINFO[user_id]['Country']=user_answer

    print(USERINFO)
    return 0

def UserCity():

    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    USERINFO[user_id]['City']=user_answer

    print(USERINFO)
    return 0

def UserDate():

    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    USERINFO[user_id]['Date']=user_answer

    print(USERINFO)
    return 0

def UserPhoto():

    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    USERINFO[user_id]['Photo']=user_answer

    print(USERINFO)
    return 0

def UserShow():
    #USER정보 같은사람을 따로 추출하여 DB화하는 작업은 여기에 들어가야함
    message = {
                "version": "2.0",
                "template": {
                    "outputs": [
                    {
                        "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                            "description": "성별 : {}\n나이 : {}\n여행지역 : {}\n여행날짜 : {}".format(USERINFO['USER1']['Sex'],USERINFO['USER1']['Age'],(USERINFO['USER1']['Country']+' '+USERINFO['USER1']['City']),USERINFO['USER1']['Date']),
                            "thumbnail": {
                                "imageUrl": "{}".format(USERINFO['USER1']['Photo'])
                            },
                            "buttons": [
                                {
                                "action": "message",
                                "label": "이사람이 좋아! 연락처 줘",
                                
                                }

                            ]
                            },
                            {
                            "description": "성별 : {}\n나이 : {}\n여행지역 : {}\n여행날짜 : {}".format(USERINFO['USER2']['Sex'],USERINFO['USER2']['Age'],(USERINFO['USER2']['Country']+' '+USERINFO['USER2']['City']),USERINFO['USER2']['Date']),
                            "thumbnail": {
                                "imageUrl": "{}".format(USERINFO['USER2']['Photo'])
                            },
                            "buttons": [
                                {
                                "action": "message",
                                "label": "이사람이 좋아! 연락처 줘",
                                },
                                
                            ]
                            },
                            
                        ]
                        }
                    }
                    ]
                }
                }
    return message

@app.route('/IsUserNew', methods=['POST'])
def IsUserNew():
    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    answer = content['userRequest']['utterance']
    if user_id not in USERINFO.keys():
        USERINFO[user_id] = {}
        USERINFO[user_id]['Flag'] = 0
        message = send_message("처음왔구나 넌 남자야 여자야?")
        print(USERINFO)
    #성별묻기
    elif user_id in USERINFO.keys() and USERINFO[user_id]['Flag'] == 6 and answer =="응":
        message = UserShow()

    elif user_id in USERINFO.keys() and USERINFO[user_id]['Flag'] == 6:
        message = Send_Button("저번에 저장된 정보가 넌 {}고 {}살인데 {}를 {} 에 여행하는거지? \n같은 정보로 찾아줄까?".format(USERINFO[user_id]['Sex'],USERINFO[user_id]['Age'],(USERINFO[user_id]['Country']+' '+USERINFO[user_id]['City']),USERINFO[user_id]['Date']),"응","아니")
    

    elif USERINFO[user_id]['Flag'] == 0:
        USERINFO[user_id]['Flag'] = 1
        UserSex()
        user_answer = USERINFO[user_id]['Sex']
        message = send_message("{}구나! 그럼 몇 살이야? 20살이라면 20처럼 숫자만 입력해봐 ".format(user_answer))
    
        # message = send_message("{}살 이구나! 여행하는 나라는 어디야? ".format(user_answer))
    
    #나이묻기
    elif USERINFO[user_id]['Flag'] == 1:
        USERINFO[user_id]['Flag'] = 2
        UserAge()
        user_answer = USERINFO[user_id]['Age']
        message = send_message("{}살 이구나! 여행하는 나라는 어디야? ".format(user_answer))
    
    #여행국가묻기
    elif USERINFO[user_id]['Flag'] == 2:
        USERINFO[user_id]['Flag'] = 3
        UserCountry()
        user_answer = USERINFO[user_id]['Country']
        message = send_message("{} 여행하는구나! 여행하는 도시는 어디야? ".format(user_answer))
    
    #여행도시묻기
    elif USERINFO[user_id]['Flag'] == 3:
        USERINFO[user_id]['Flag'] = 4
        UserCity()
        user_answer = USERINFO[user_id]['City']
        message = send_message("{} 여행하는구나! 여행날짜도 좀 적어줘! ex)191114~191117  ".format(user_answer))
    
    #여행기간 묻기
    elif USERINFO[user_id]['Flag'] == 4:
        USERINFO[user_id]['Flag'] = 5
        UserDate()
        # message = Send_Button("그럼 넌 {}고 {}살인데 {}를 {} 에 여행하는거지?".format(USERINFO[user_id]['Sex'],USERINFO[user_id]['Age'],(USERINFO[user_id]['Country']+' '+USERINFO[user_id]['City']),USERINFO[user_id]['Date']),"응","아니")
        message = send_message("프로필 사진에 사용될 사진을 앨범에서 보내줘")

    #사진받아오기
    elif USERINFO[user_id]['Flag'] == 5:
        USERINFO[user_id]['Flag'] = 6
        UserPhoto()
        message = Send_Button("그럼 넌 {}고 {}살인데 {}를 {} 에 여행하는거지?".format(USERINFO[user_id]['Sex'],USERINFO[user_id]['Age'],(USERINFO[user_id]['Country']+' '+USERINFO[user_id]['City']),USERINFO[user_id]['Date']),"응","아니")
        

    

    return message



if __name__ == "__main__":
    app.run(host='0.0.0.0',port =5000)



