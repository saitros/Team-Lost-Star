from flask import Flask, request, jsonify
import sys
import SQL_function
app = Flask(__name__)
USERINFO = {"USER1":{'IsNew':'Existing','Flag': 5,'KakaoID':'user1', 'Sex': '여자', 'Age': '25', 'Country': '스페인', 'City': '바르셀로나', 'Date': '191115~191118','Photo':'http://dn-m.talk.kakao.com/talkm/bl3pyYUSIOW/7W4dKnjongiKIxu3XkIGf0/i_4z0ltufqhvph1.jpeg'},
            "USER2":{'IsNew':'Existing','Flag': 5,'KakaoID':'user2', 'Sex': '남자', 'Age': '22', 'Country': '스페인', 'City': '바르셀로나', 'Date': '191115~191118','Photo':'http://dn-m.talk.kakao.com/talkm/bl3pyUdR9s1/Gr6VQYRpAdR5UY17uo6u61/i_djwoz2tu3ln6.jpeg'}}
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

#유저 본인 프로필버튼
def UserProfile_Button(message,user_id,button1,button2,button3):
    message = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                        {
                            "carousel": {
                            "type": "basicCard",
                            "items": [
                                {
                                "description": "{}".format(message),
                                "thumbnail": {
                                    "imageUrl": "{}".format(USERINFO[user_id]['Photo'])
                                },
                                "buttons": [
                                    {
                                    "action": "message",
                                    "label": "{}".format(button1),
                                    "messageText" : "{}".format(button1)
                                    
                                    },
                                    {
                                    "action": "message",
                                    "label": "{}".format(button2),
                                    "messageText" : "{}".format(button2)
                                    
                                    },
                                    {
                                    "action": "webLink",
                                    "label": "{}".format(button3),
                                    "webLinkUrl" : "{}".format(USERINFO[user_id]['Photo'])
                                    
                                    }


                                ]
                                }
                            ]
                            }
                        }
                        ]
                    }
                    }
    return message
def Change_Button():
    button = {
        "version": "2.0",
            "template": {
                "outputs": [{"simpleText":{"text": "수정하고 싶은걸 선택해 봐"}}],               
            "quickReplies" : [
                {
                    "action": "message",
                    "label": "성별",                       
                    "messageText": "성별 수정할래"
                    
                },
                {
                    "action":"message",
                    "label":"나이",                       
                    "messageText":"나이 수정할래"
                    
                },
                {
                    "action":"message",
                    "label":"여행지",                       
                    "messageText":"여행지 수정할래"
                    
                },
                {
                    "action":"message",
                    "label":"여행 날짜",                       
                    "messageText":"여행 날짜 수정할래"
                    
                },
                {
                    "action":"message",
                    "label":"프로필사진",                       
                    "messageText":"프로필사진 수정할래"
                    
                },
                {
                    "action":"message",
                    "label":"수정안하기",                       
                    "messageText":"그냥 수정 안할래"
                    
                }
            ]
    }}
    return button

def UserDataGet(VarName):

    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    USERINFO[user_id][VarName]=user_answer

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
                                "action": "webLink",
                                "label": "프로필사진 크게보기",
                                "webLinkUrl" : "{}".format(USERINFO['USER1']['Photo'])
                                
                                },
                                {
                                "action": "message",
                                "label": "이사람이 좋아! 연락처 줘",
                                "messageText" : "이사람이 좋아! 연락처 줘"
                                
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
                                "action": "webLink",
                                "label": "프로필사진 크게보기",
                                "webLinkUrl" : "{}".format(USERINFO['USER2']['Photo'])
                                
                                },
                                {
                                "action": "message",
                                "label": "이사람이 좋아!! 연락처 줘 ",                                
                                "messageText" : "이사람이 좋아!! 연락처 줘 "
                                
                                }
                                
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

    #신규회원이 들어올경우 웰컴 메시지
    if user_id not in USERINFO.keys() and answer =="동행 찾아볼래!":
        USERINFO[user_id] = {}
        USERINFO[user_id]['IsNew'] = 'New'
        USERINFO[user_id]['Flag'] = 'New'
        USERINFO[user_id]['SearchTimes']=0
        message = Send_Button("처음왔구나 동행을 찾기위해선 너의 정보가 필요해! 작성 도중 처음화면으로 돌아가게되면 정보가 저장되지 않으니 주의해!\n너의 정보를 내가 물어봐도 괜찮아?","응","아니")
        print(USERINFO)

    #신규회원이 작성도중 처음으로 갔을경우의 Flow
    elif USERINFO[user_id]['IsNew']=='New' and answer =="동행 찾아볼래!":
        USERINFO[user_id]['Flag']='New'
        message = Send_Button("저번에 작성하다가 그만뒀구나! 그럼 처음부터 다시물어봐야하는데 괜찮지?\n너의 정보를 내가 물어봐도 괜찮아?","응","아니")
       
    #기존회원 성별 수정 FLOW
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == "Done" and answer == "성별 수정할래":
        USERINFO[user_id]['Flag'] = 'Sex'
        message = Send_Button("알겠어! 그럼 넌 남자야 여자야??","남자","여자")
       

    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == "Sex":
        USERINFO[user_id]['Flag'] = "Done"
        UserDataGet('Sex')
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n같은 정보로 찾아줄까?".format(USERINFO[user_id]['Sex'],USERINFO[user_id]['Age'],(USERINFO[user_id]['Country']+' '+USERINFO[user_id]['City']),USERINFO[user_id]['Date']),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    #기존회원 나이 수정 FLOW
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == "Done" and answer == "나이 수정할래":
        USERINFO[user_id]['Flag'] = 'Age'
        message = send_message("알겠어! 나이를 다시 입력해줘! 숫자로만 입력해! Ex)20")

    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == "Age":
        USERINFO[user_id]['Flag'] = "Done"
        UserDataGet('Age')
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n같은 정보로 찾아줄까?".format(USERINFO[user_id]['Sex'],USERINFO[user_id]['Age'],(USERINFO[user_id]['Country']+' '+USERINFO[user_id]['City']),USERINFO[user_id]['Date']),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    #기존회원 여행날짜 수정 FLOW
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == "Done" and answer == "여행 날짜 수정할래":
        USERINFO[user_id]['Flag'] = 'Date'
        message = send_message("알겠어! 여행 날짜를 다시 입력해줘! Ex)191115~191118")

    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == "Date":
        USERINFO[user_id]['Flag'] = "Done"
        UserDataGet('Date')
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n같은 정보로 찾아줄까?".format(USERINFO[user_id]['Sex'],USERINFO[user_id]['Age'],(USERINFO[user_id]['Country']+' '+USERINFO[user_id]['City']),USERINFO[user_id]['Date']),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    #기존회원 프로필사진 수정 FLOW
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == "Done" and answer == "프로필사진 수정할래":
        USERINFO[user_id]['Flag'] = 'Photo'
        message = send_message("알겠어! 앨범에서 사진을 골라서 나한테 다시 보내줘")

    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == "Photo":
        USERINFO[user_id]['Flag'] = "Done"
        UserDataGet('Photo')
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n같은 정보로 찾아줄까?".format(USERINFO[user_id]['Sex'],USERINFO[user_id]['Age'],(USERINFO[user_id]['Country']+' '+USERINFO[user_id]['City']),USERINFO[user_id]['Date']),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    #기존회원 여행지 수정 FLOW
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == "Done" and answer == "여행지 수정할래":
        USERINFO[user_id]['Flag'] = 'Country'
        message = send_message("알겠어! 여행하는 나라이름 알려줘!")
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == "Country":
        USERINFO[user_id]['Flag'] = 'City'
        UserDataGet('Country')
        message = send_message("여행하는 도시는 어디야?")
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == "City":
        USERINFO[user_id]['Flag'] = 'Done'
        UserDataGet('City')
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n같은 정보로 찾아줄까?".format(USERINFO[user_id]['Sex'],USERINFO[user_id]['Age'],(USERINFO[user_id]['Country']+' '+USERINFO[user_id]['City']),USERINFO[user_id]['Date']),user_id,"응","정보 수정할래","내 프로필 사진 볼래")
  
    
    #기존회원의 경우 기존의 정보로 찾아달라고 하기
    elif user_id in USERINFO.keys() and  USERINFO[user_id]['Flag'] == 'Done' and answer =="응":
        message = UserShow()
    
    #정보 물어도 된다고 하면 성별 묻기
    elif user_id in USERINFO.keys() and USERINFO[user_id]['Flag'] == 'New' and answer =="응":
        USERINFO[user_id]['Flag']='Sex'
        message = Send_Button("알겠어! 그럼 넌 남자야 여자야??","남자","여자")
       
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == 'Done' and answer =="동행 찾아볼래!":
        message = UserProfile_Button("현재 저장된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n같은 정보로 찾아줄까?".format(USERINFO[user_id]['Sex'],USERINFO[user_id]['Age'],(USERINFO[user_id]['Country']+' '+USERINFO[user_id]['City']),USERINFO[user_id]['Date']),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "Existing" and USERINFO[user_id]['Flag'] == 'Done' and answer =="정보 수정할래":
        message = Change_Button()

    #신규회원 성별묻기
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "New" and USERINFO[user_id]['Flag'] == 'Sex':
        USERINFO[user_id]['Flag'] = 'Age'
        UserDataGet('Sex')
        message = send_message("{}구나! 그럼 몇 살이야? 20살이라면 20처럼 숫자만 입력해봐 ".format(USERINFO[user_id]['Sex']))
    
        
    #신규회원 나이묻기
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "New" and USERINFO[user_id]['Flag'] == 'Age':
        USERINFO[user_id]['Flag'] = 'Country'
        UserDataGet('Age')
        message = send_message("{}살 이구나! 여행하는 나라는 어디야? ".format(USERINFO[user_id]['Age']))
    
    #신규회원 여행국가묻기
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "New" and USERINFO[user_id]['Flag'] == 'Country':
        USERINFO[user_id]['Flag'] = 'City'
        UserDataGet('Country')
        message = send_message("{} 여행하는구나! 여행하는 도시는 어디야? ".format(USERINFO[user_id]['Country']))
    
    #신규회원 여행도시묻기
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "New" and USERINFO[user_id]['Flag'] == 'City':
        USERINFO[user_id]['Flag'] = 'Date'
        UserDataGet('City')
        message = send_message("{} 여행하는구나! 여행날짜도 좀 적어줘! ex)191114~191117  ".format(USERINFO[user_id]['City']))
    
    #신규회원 여행기간 묻기
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "New" and USERINFO[user_id]['Flag'] == 'Date':
        USERINFO[user_id]['Flag'] = 'Photo'
        UserDataGet('Date')
        message = send_message("프로필 사진에 사용될 사진을 앨범에서 보내줘")

    #신규회원 사진받아오기
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "New" and USERINFO[user_id]['Flag'] == 'Photo':
        USERINFO[user_id]['Flag'] = 'KakaoID'
        UserDataGet('Photo')
        message = send_message("그럼 다른 사람이 너에게 연락할 수 있도록 카카오톡 ID를 알려줄래?")
    
    #신규회원이 자신의 정보를 모두 입력하는 순간 기존회원으로 등업이된다
    elif user_id in USERINFO.keys() and USERINFO[user_id]['IsNew'] == "New" and USERINFO[user_id]['Flag'] == 'KakaoID':
        USERINFO[user_id]['IsNew']='Existing'
        USERINFO[user_id]['Flag'] = 'Done'
        UserDataGet('KakaoID')
        message = UserProfile_Button("너의 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n이정보로 동행 바로 찾아줄까?".format(USERINFO[user_id]['Sex'],USERINFO[user_id]['Age'],(USERINFO[user_id]['Country']+' '+USERINFO[user_id]['City']),USERINFO[user_id]['Date']),user_id,"응","정보 수정할래","내 프로필 사진 볼래")


    elif user_id in USERINFO.keys() and USERINFO[user_id]['Flag'] == 'Done' and answer == "이사람이 좋아! 연락처 줘" :
        if USERINFO[user_id]['SearchTimes']<3:
            USERINFO[user_id]['SearchTimes']+=1
            message = send_message("카카오톡 ID : {}".format(USERINFO['USER1']['KakaoID']))
        elif USERINFO[user_id]['SearchTimes']>=3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
        
        
    elif user_id in USERINFO.keys() and USERINFO[user_id]['Flag'] == 'Done' and answer == "이사람이 좋아!! 연락처 줘" and USERINFO[user_id]['SearchTimes']<3:
        if USERINFO[user_id]['SearchTimes']<3:
            USERINFO[user_id]['SearchTimes']+=1
            message = send_message("카카오톡 ID : {}".format(USERINFO['USER2']['KakaoID']))
        elif USERINFO[user_id]['SearchTimes']>=3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
        
    else:
        message = send_message("미안해 잘 못알아들었어! 다시 말해줄래?")
    return jsonify(message)



if __name__ == "__main__":
    app.run(host='0.0.0.0',port =5000)



