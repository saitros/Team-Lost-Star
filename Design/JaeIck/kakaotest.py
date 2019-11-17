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
                                    "imageUrl": "{}".format(SQL_function.search_data("kakaotalk","profile_image",user_id,1)[0])
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
                                    "webLinkUrl" : "{}".format(SQL_function.search_data("kakaotalk","profile_image",user_id,1)[0])
                                    
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
                    "label":"어필 태그",
                    "messageText":"어필 태그 수정할래"
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
    SQL_function.update_data("kakaotalk","{}".format(VarName),user_answer,user_id)
    
    return 0

def UserDateDataGet():
    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    SQL_function.update_data("kakaotalk","start_date",user_answer[0:6],user_id)
    SQL_function.update_data("kakaotalk","end_date",user_answer[7:],user_id)
    
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
    if SQL_function.is_user_new("kakaotalk",user_id) and answer =="동행 찾아볼래!":
        SQL_function.insert_id_data("kakaotalk",(user_id,"new","new",0))
        message = Send_Button("처음왔구나 동행을 찾기위해선 너의 정보가 필요해! 작성 도중 처음화면으로 돌아가게되면 정보가 저장되지 않으니 주의해!\n너의 정보를 내가 물어봐도 괜찮아?","응","아니")
        
    #신규회원이 작성도중 처음으로 갔을경우의 Flow
    elif SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and answer =="동행 찾아볼래!":
        SQL_function.update_data("kakaotalk","dialog_state","new",user_id)
        message = Send_Button("저번에 작성하다가 그만뒀구나! 그럼 처음부터 다시물어봐야하는데 괜찮지?\n너의 정보를 내가 물어봐도 괜찮아?","응","아니")
    
    #정보 물어도 된다고 하면 성별 묻기
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='new' and answer =="응":
        SQL_function.update_data("kakaotalk","dialog_state","sex",user_id)
        message = Send_Button("알겠어! 그럼 넌 남자야 여자야??","남자","여자")
       
    #신규회원 성별묻기
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='sex':
        SQL_function.update_data("kakaotalk","dialog_state","age",user_id)
        UserDataGet('sex')
        message = send_message("{}구나! 그럼 몇 살이야? 20살이라면 20처럼 숫자만 입력해봐 ".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0]))
    
        
    #신규회원 나이묻기
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='age':
        SQL_function.update_data("kakaotalk","dialog_state","country",user_id)
        UserDataGet('age')
        message = send_message("{}살 이구나! 여행하는 나라는 어디야? ".format(SQL_function.search_data("kakaotalk","age",user_id,1)[0]))
    
    #신규회원 여행국가묻기
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='country':
        SQL_function.update_data("kakaotalk","dialog_state","city",user_id)
        UserDataGet('country')
        message = send_message("{} 여행하는구나! 여행하는 도시는 어디야? ".format(SQL_function.search_data("kakaotalk","country",user_id,1)[0]))
    
    #신규회원 여행도시묻기
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='city':
        SQL_function.update_data("kakaotalk","dialog_state","date",user_id)
        UserDataGet('city')
        
        message = send_message("{} 여행하는구나! 여행날짜도 좀 적어줘! ex)191114~191117  ".format(SQL_function.search_data("kakaotalk","city",user_id,1)[0]))
    
    #신규회원 여행기간 묻기
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='date':
        SQL_function.update_data("kakaotalk","dialog_state","profile_image",user_id)
        UserDateDataGet()
        message = send_message("프로필 사진에 사용될 사진을 앨범에서 보내줘")

    #신규회원 사진받아오기
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='profile_image':
        SQL_function.update_data("kakaotalk","dialog_state","kakao_id",user_id)
        UserDataGet('profile_image')
        message = send_message("그럼 다른 사람이 너에게 연락할 수 있도록 카카오톡 ID를 알려줄래?")
    
    #신규회원 어필태그작성
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='kakao_id':
        SQL_function.update_data("kakaotalk","dialog_state","appeal_tag",user_id)
        UserDataGet("kakao_id")
        message = send_message("마지막으로 너를 어필하는 태그들을 작성해봐 ex)#먹방 #잠만보")

    #신규회원이 자신의 정보를 모두 입력하는 순간 기존회원으로 등업이된다
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='appeal_tag':
        SQL_function.update_data("kakaotalk","user_state","Existing",user_id)
        SQL_function.update_data("kakaotalk","dialog_state","done",user_id)
        
        UserDataGet('appeal_tag')
        message = UserProfile_Button("너의 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n이정보로 동행 바로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],
                                                                                                                                            SQL_function.search_data("kakaotalk","age",user_id,1)[0],
                                                                                                                                            (SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),
                                                                                                                                            (SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),
                                                                                                                                            SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,
                                                                                                                                            "응","정보 수정할래","내 프로필 사진 볼래")
   
    #기존회원 성별 수정 FLOW
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "성별 수정할래":
        SQL_function.update_data("kakaotalk", "dialog_state", "sex", user_id)
        message = Send_Button("알겠어! 그럼 넌 남자야 여자야??","남자","여자")
       

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and  SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "sex":
        SQL_function.update_data("kakaotalk", "dialog_state", "done", user_id)
        UserDataGet('sex')
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    #기존회원 나이 수정 FLOW
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "나이 수정할래":
        SQL_function.update_data("kakaotalk", "dialog_state", "age", user_id)
        message = send_message("알겠어! 나이를 다시 입력해줘! 숫자로만 입력해! Ex)20")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "age":
        SQL_function.update_data("kakaotalk", "dialog_state", "done", user_id)
        UserDataGet('age')
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    #기존회원 여행날짜 수정 FLOW
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "여행 날짜 수정할래":
        SQL_function.update_data("kakaotalk", "dialog_state", "date", user_id)
        message = send_message("알겠어! 여행 날짜를 다시 입력해줘! Ex)191115~191118")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "date":
        SQL_function.update_data("kakaotalk", "dialog_state", "done", user_id)
        UserDateDataGet()
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    #기존회원 프로필사진 수정 FLOW
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "프로필사진 수정할래":
        SQL_function.update_data("kakaotalk", "dialog_state", "profile_image", user_id)
        message = send_message("알겠어! 앨범에서 사진을 골라서 나한테 다시 보내줘")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "profile_image":
        SQL_function.update_data("kakaotalk", "dialog_state", "done", user_id)
        UserDataGet('profile_image')
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")
    
    #기존회원 어필태그 수정 FLOW
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "어필 태그 수정할래":
        SQL_function.update_data("kakaotalk", "dialog_state", "appeal_tag", user_id)
        message = send_message("알겠어! 어필 태그 다시 써줘! Ex) #먹방 #잠만보")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "appeal_tag":
        SQL_function.update_data("kakaotalk", "dialog_state", "done", user_id)
        UserDataGet('appeal_tag')
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    #기존회원 여행지 수정 FLOW
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "여행지 수정할래":
        SQL_function.update_data("kakaotalk", "dialog_state", "country", user_id)
        message = send_message("알겠어! 여행하는 나라이름 알려줘!")
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "country":
        SQL_function.update_data("kakaotalk", "dialog_state", "city", user_id)
        UserDataGet('country')
        message = send_message("여행하는 도시는 어디야?")
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "city":
        SQL_function.update_data("kakaotalk", "dialog_state", "done", user_id)
        UserDataGet('city')
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")
  
    
    #기존회원의 경우 기존의 정보로 찾아달라고 하기
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer =="응":
        message = UserShow()
    
    
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer =="동행 찾아볼래!":
        message = UserProfile_Button("현재 저장된 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer =="정보 수정할래":
        message = Change_Button()

    
    # 수정필요
    # elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "이사람이 좋아! 연락처 줘" :
    #     if USERINFO[user_id]['SearchTimes']<3:
    #         USERINFO[user_id]['SearchTimes']+=1
    #         message = send_message("카카오톡 ID : {}".format(USERINFO['USER1']['KakaoID']))
    #     elif USERINFO[user_id]['SearchTimes']>=3:
    #         message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
        
        
    # elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == 'done' and answer == "이사람이 좋아!! 연락처 줘" and SQL_function.search_data("kakaotalk","open_cnt",user_id,1) < 3:
    #     num = SQL_function.search_data("kakaotalk","open_cnt",user_id,1)
    #     if SQL_function.search_data("kakaotalk","open_cnt",user_id,1) < 3:
    #         SQL_function.update_data("kakaotalk","open_cnt",num+1,user_id)
    #         message = send_message("카카오톡 ID : {}".format(USERINFO['USER2']['KakaoID']))
    #     elif SQL_function.search_data("kakaotalk","open_cnt",user_id,1) >=3:
    #         message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
        
    else:
        message = send_message("미안해 잘 못알아들었어! 다시 말해줄래?")
    return jsonify(message)



if __name__ == "__main__":
    app.run(host='0.0.0.0',port =5000)



