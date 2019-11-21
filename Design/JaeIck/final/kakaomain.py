from flask import Flask, request, jsonify
import sys
import SQL_function
import CheckInput
import re
app = Flask(__name__)
SHOWDB = {}
IDDB = {}
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
                ],
                "quickReplies" : [
                {
                    "action": "message",
                    "label": "처음으로",                       
                    "messageText": "처음으로"
                    
                }]
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
            ],
            "quickReplies" : [
                {
                    "action": "message",
                    "label": "처음으로",                       
                    "messageText": "처음으로"
                    
                }]
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
                        ],
                        "quickReplies" : [
                {
                    "action": "message",
                    "label": "처음으로",                       
                    "messageText": "처음으로"
                    
                }]
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

def UserLocDataGet(VarName,id,answer):
    SQL_function.update_data("kakaotalk","{}".format(VarName),answer,id)
    return 0
    
def UserDateDataGet():
    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    SQL_function.update_data("kakaotalk","start_date",user_answer[0:2]+"-"+user_answer[2:4]+"-"+user_answer[4:6],user_id)
    SQL_function.update_data("kakaotalk","end_date",user_answer[7:9]+"-"+user_answer[9:11]+"-"+user_answer[11:13],user_id)
    
    return 0

def UserShow(id,DB):
    count = SQL_function.search_data("kakaotalk","show_count",id,1)[0]
    #USER정보 같은사람을 따로 추출하여 DB화하는 작업은 여기에 들어가야함
    message = {
                "version": "2.0",
                "template": {
                    "outputs": [
                    {
                        "carousel": {
                        "type": "basicCard",
                        "items": [
                            
                            
                        ]
                    }}],
            "quickReplies" : [
                {
                    "action": "message",
                    "label": "이전사람보기",                       
                    "messageText": "이전사람보기"
                    
                },
                {
                    "action":"message",
                    "label":"다음사람보기",                       
                    "messageText":"다음사람보기"
                    
                },
                {
                    "action":"message",
                    "label":"그만보기",                       
                    "messageText":"그만보기"
                    
                }

                    
                    ]
                }
                }
    tempDB = DB[count:count+10]
    num = 0
    IDDB[id] = {}
    for i in tempDB:
        buttons = {
                            "description": "성별 : {}  나이 : {}\n여행지역 : {}\n여행날짜 : {}\n어필태그 : {}".format(i[0],i[1],(i[2]+' '+i[3]),(i[5]+'~'+i[6]),i[7]),
                            "thumbnail": {
                                "imageUrl": "{}".format(i[4])
                            },
                            "buttons": [
                                {
                                "action": "webLink",
                                "label": "프로필사진 크게보기",
                                "webLinkUrl" : "{}".format(i[4])
                                
                                },
                                {
                                "action": "message",
                                "label": "이사람이 좋아! 연락처 줘",
                                "messageText" : "이사람이 좋아"+"!"*num +" 연락처 줘"
                                
                                }


                            ]
                    }
        IDDB[id][num]=i[8]
        count += 1
        num += 1
        
        message["template"]["outputs"][0]["carousel"]["items"].append(buttons)
    SQL_function.update_data("kakaotalk","show_count",count,id)
    return message

@app.route('/GoTogether', methods=['POST'])
def IsUserNew():
    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    answer = content['userRequest']['utterance']

    #신규회원이 들어올경우 웰컴 메시지
    if SQL_function.is_user_new("kakaotalk",user_id) and answer =="동행 찾아볼래!":
        SQL_function.insert_id_data("kakaotalk",(user_id,"new","new",0,0))
        message = Send_Button("처음왔구나 동행을 찾기위해선 너의 정보가 필요해! 작성 도중 처음화면으로 돌아가게되면 정보가 저장되지 않으니 주의해!\n너의 정보를 내가 물어봐도 괜찮아?","응","아니")
        
    #신규회원이 작성도중 처음으로 갔을경우의 Flow
    elif SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and answer =="동행 찾아볼래!":
        SQL_function.update_data("kakaotalk","dialog_state","new",user_id)
        message = Send_Button("저번에 작성하다가 그만뒀구나! 그럼 처음부터 다시물어봐야하는데 괜찮지?\n너의 정보를 내가 물어봐도 괜찮아?","응","아니")
    
    elif SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='Existing' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]!='done' and answer =="동행 찾아볼래!":
        SQL_function.update_data("kakaotalk","dialog_state","done",user_id)
        message = UserProfile_Button("저번에 수정하다가 그만뒀구나 혹시 너의 정보가 이상하진 않은지 확인해봐!\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n이정보로 동행 바로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],
                                                                                                                                            SQL_function.search_data("kakaotalk","age",user_id,1)[0],
                                                                                                                                            (SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),
                                                                                                                                            (SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),
                                                                                                                                            SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,
                                                                                                                                            "응","정보 수정할래","내 프로필 사진 볼래")
   
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
        a = CheckInput.CheckCityName(answer)
        print("여기는 kakaotest")
        print(a)
        if a is False:
            SQL_function.update_data("kakaotalk","dialog_state","country",user_id)
            message = send_message("입력한게 오타가 있거나 지역이름이 아닌거 같아. 다시 입력해줄래?")
        else:
            SQL_function.update_data("kakaotalk","dialog_state","countrycheck",user_id)
            UserLocDataGet("country",user_id,a)
            message = Send_Button("{} 여행하는거 맞아?".format(SQL_function.search_data("kakaotalk","country",user_id,1)[0]),"응","오타났나봐")

        
        # SQL_function.update_data("kakaotalk","dialog_state","countrycheck",user_id)
        
        # UserDataGet('country')
        
        # message = Send_Button("{} 여행하는거 맞아?".format(SQL_function.search_data("kakaotalk","country",user_id,1)[0]),"응","오타났나봐")
        
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='countrycheck' and answer == "응":
        SQL_function.update_data("kakaotalk","dialog_state","city",user_id)
        message = send_message("{} 여행하는구나! 여행하는 도시는 어디야? ".format(SQL_function.search_data("kakaotalk","country",user_id,1)[0]))

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='countrycheck' and answer == "오타났나봐":
        SQL_function.update_data("kakaotalk","dialog_state","country",user_id)
        message = send_message("여행하는 나라를 다시 입력해줘")

    #신규회원 여행도시묻기
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='city':
        a = CheckInput.CheckCityName(answer)
        print(a)
        if a is False:
            SQL_function.update_data("kakaotalk","dialog_state","city",user_id)
            message = send_message("입력한게 오타가 있거나 지역이름이 아닌거 같아. 다시 입력해줄래?")
        else:
            SQL_function.update_data("kakaotalk","dialog_state","citycheck",user_id)
            UserLocDataGet("city",user_id,a)
            message = Send_Button("{} 여행하는거 맞아?".format(SQL_function.search_data("kakaotalk","city",user_id,1)[0]),"응","오타났나봐")
    
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='citycheck' and answer == "오타났나봐":
        SQL_function.update_data("kakaotalk","dialog_state","city",user_id)
        message = send_message("여행하는 도시를 다시 입력해줘")
    
       
        # SQL_function.update_data("kakaotalk","dialog_state","citycheck",user_id)
        # UserDataGet('city')
        # message = Send_Button("{} 여행하는거 맞아?".format(SQL_function.search_data("kakaotalk","city",user_id,1)[0]),"응","오타났나봐")
    #신규회원 여행기간 묻기    
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='citycheck' and answer == "응":
        SQL_function.update_data("kakaotalk","dialog_state","datecheck",user_id)
        message = send_message("{} 여행하는구나! 여행 시작날짜를 알려줘! Ex) 191125~191128  ".format(SQL_function.search_data("kakaotalk","city",user_id,1)[0]))

    # elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='date':
    #     SQL_function.update_data("kakaotalk","dialog_state","datecheck",user_id)
    #     message = send_message("그럼 다시 여행 시작날짜를 알려줘! Ex) 191125~191128")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='datecheck':
        try:
            if (len(answer) != 13 or answer[6]!="~" or (int(answer[0:6]) > int(answer[7:])) or int(answer[2:4])>12 or int(answer[9:11]) > 12 or int(answer[4:6])>31 or int(answer[12:])>31) is True:
                SQL_function.update_data("kakaotalk","dialog_state","datecheck",user_id)
                message = send_message("뭔가 잘 못 입력한거 같아..\n여행날짜를 아래형식에 맞게 다시 입력해줘 Ex) 191125~191128")
            else:
                SQL_function.update_data("kakaotalk","dialog_state","profile_image",user_id)
                UserDateDataGet()
                message = send_message("프로필 사진에 사용될 사진을 앨범에서 보내줘")

        except:
            SQL_function.update_data("kakaotalk","dialog_state","date",user_id)
            message = send_message("뭔가 잘 못 입력한거 같아..\n여행날짜를 아래형식에 맞게 다시 입력해줘 Ex) 191125~191128")
     
    #신규회원 사진받아오기
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='profile_image':
        SQL_function.update_data("kakaotalk","dialog_state","kakao_id",user_id)
        UserDataGet('profile_image')
        message = send_message("그럼 다른 사람이 너에게 연락할 수 있도록 카카오톡 ID를 알려줄래?")

    #신규회원 카톡아이디 받기
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='kakao_id':
        SQL_function.update_data("kakaotalk","dialog_state","kakao_idcheck",user_id)
        UserDataGet("kakao_id")
        message = Send_Button("{}이 너의 카카오톡 아이디가 맞아?".format(SQL_function.search_data("kakaotalk","kakao_id",user_id,1)[0]),"응","오타났나봐")
    
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='kakao_idcheck' and answer == "응":
        SQL_function.update_data("kakaotalk","dialog_state","appeal_tag",user_id)
        message = send_message("마지막으로 너를 어필하는 태그들을 작성해봐 ex)#먹방 #잠만보")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='new' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='kakao_idcheck' and answer == "오타났나봐":
        SQL_function.update_data("kakaotalk","dialog_state","kakao_id",user_id)
        message = send_message("카카오톡 아이디 다시 알려줄래?")

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
        SQL_function.update_data("kakaotalk", "dialog_state", "datecheck", user_id)
        message = send_message("알겠어! 여행 날짜를 다시 입력해줘! Ex)191115~191118")
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "datecheck":
        
        try:
            if (len(answer) != 13 or answer[6]!="~" or (int(answer[0:6]) > int(answer[7:])) or int(answer[2:4])>12 or int(answer[9:11]) > 12 or int(answer[4:6])>31 or int(answer[12:])>31) is True:
                SQL_function.update_data("kakaotalk","dialog_state","datecheck",user_id)
                message = send_message("뭔가 잘 못 입력한거 같아..\n여행날짜를 아래형식에 맞게 다시 입력해줘 Ex) 191125~191128")
            else:
                SQL_function.update_data("kakaotalk","dialog_state","done",user_id)
                UserDateDataGet()
                message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}  나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

        except:
            SQL_function.update_data("kakaotalk","dialog_state","datecheck",user_id)
            message = send_message("뭔가 잘 못 입력한거 같아..\n여행날짜를 아래형식에 맞게 다시 입력해줘 Ex) 191125~191128")
   
#    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "date":
#         SQL_function.update_data("kakaotalk", "dialog_state", "done", user_id)
#         UserDateDataGet()
#         message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}  나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    #기존회원 프로필사진 수정 FLOW
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "프로필사진 수정할래":
        SQL_function.update_data("kakaotalk", "dialog_state", "profile_image", user_id)
        message = send_message("알겠어! 앨범에서 사진을 골라서 나한테 다시 보내줘")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "profile_image":
        SQL_function.update_data("kakaotalk", "dialog_state", "done", user_id)
        UserDataGet('profile_image')
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}  나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")
    
    #기존회원 어필태그 수정 FLOW
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "어필 태그 수정할래":
        SQL_function.update_data("kakaotalk", "dialog_state", "appeal_tag", user_id)
        message = send_message("알겠어! 어필 태그 다시 써줘! Ex) #먹방 #잠만보")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "appeal_tag":
        SQL_function.update_data("kakaotalk", "dialog_state", "done", user_id)
        UserDataGet('appeal_tag')
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}  나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    #기존회원 여행지 수정 FLOW
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='Existing' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "여행지 수정할래":
        SQL_function.update_data("kakaotalk","dialog_state","country",user_id)
        message = send_message("알겠어! 여행하는 나라이름 알려줘!")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='Existing' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='country' :
        
        a = CheckInput.CheckCityName(answer)
        print("여기는 kakaotest")
        print(a)
        if a is False:
            SQL_function.update_data("kakaotalk","dialog_state","country",user_id)
            message = send_message("입력한게 오타가 있거나 지역이름이 아닌거 같아. 다시 입력해줄래?")
        else:
            SQL_function.update_data("kakaotalk","dialog_state","countrycheck",user_id)
            UserLocDataGet("country",user_id,a)
            message = Send_Button("{} 여행하는거 맞아?".format(SQL_function.search_data("kakaotalk","country",user_id,1)[0]),"응","오타났나봐")

        
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='Existing' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='countrycheck' and answer == "응":
        SQL_function.update_data("kakaotalk","dialog_state","city",user_id)
        message = send_message("{} 여행하는구나! 여행하는 도시는 어디야? ".format(SQL_function.search_data("kakaotalk","country",user_id,1)[0]))

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='Existing' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='countrycheck' and answer == "오타났나봐":
        SQL_function.update_data("kakaotalk","dialog_state","country",user_id)
        message = send_message("여행하는 나라를 다시 입력해줘")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "city":
        
        a = CheckInput.CheckCityName(answer)
        print(a)
        if a is False:
            SQL_function.update_data("kakaotalk","dialog_state","city",user_id)
            message = send_message("입력한게 오타가 있거나 지역이름이 아닌거 같아. 다시 입력해줄래?")
        else:
            SQL_function.update_data("kakaotalk","dialog_state","citycheck",user_id)
            UserLocDataGet("city",user_id,a)
            message = Send_Button("{} 여행하는거 맞아?".format(SQL_function.search_data("kakaotalk","city",user_id,1)[0]),"응","오타났나봐")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='Existing' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='citycheck' and answer == "오타났나봐":
        SQL_function.update_data("kakaotalk","dialog_state","city",user_id)
        message = send_message("여행하는 도시를 다시 입력해줘")
    
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0]=='Existing' and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0]=='citycheck' and answer == "응":
        SQL_function.update_data("kakaotalk","dialog_state","done",user_id)
        message = UserProfile_Button("수정이 완료된 정보를 확인해봐\n성별 : {}  나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")
  
    
    #기존회원의 경우 기존의 정보로 찾아달라고 하기
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer =="응":
        # DB = SQL_function.my_kakao_user_search(user_id)
        # if DB is False:
        DB = SQL_function.search_user("kakaotalk",user_id)
        count = SQL_function.search_data("kakaotalk","show_count",user_id,opt=1)[0]
        if len(DB) == 0:
            message = Send_Button("미안해 동행이 가능한 사람이 없는거 같아..","처음으로","정보 수정할래")
        else:
            if len(DB)>count:
                SHOWDB[user_id] = DB
                message = UserShow(user_id,SHOWDB[user_id])
            else:
                message = send_message("더 이상 가능한 사람이 없어! 지금까지 보여준 사람중에 선택해봐!")
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer =="그냥 수정 안할래":
        message = UserProfile_Button("너의 정보를 확인해봐\n성별 : {}\n나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n이정보로 동행 바로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],
                                                                                                                                            SQL_function.search_data("kakaotalk","age",user_id,1)[0],
                                                                                                                                            (SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),
                                                                                                                                            (SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),
                                                                                                                                            SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,
                                                                                                                                            "응","정보 수정할래","내 프로필 사진 볼래")
   
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer =="다음사람보기":
        # DB = SQL_function.my_kakao_user_search(user_id)
        # if DB is False:
        DB = SQL_function.search_user("kakaotalk",user_id)
        count = SQL_function.search_data("kakaotalk","show_count",user_id,opt=1)[0]
        if len(DB) == 0:
            message = Send_Button("미안해 동행이 가능한 사람이 없는거 같아..","처음으로","정보 수정할래")
        else:
            if len(DB)>count:
                SHOWDB[user_id] = DB
                message = UserShow(user_id,SHOWDB[user_id])
            else:
                message = send_message("더 이상 가능한 사람이 없어! 지금까지 보여준 사람중에 선택해봐!")
    
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer =="이전사람보기":
        # DB = SQL_function.my_kakao_user_search(user_id)
        # if DB is False:
        DB = SQL_function.search_user("kakaotalk",user_id)
        count = SQL_function.search_data("kakaotalk","show_count",user_id,opt=1)[0]
        SQL_function.update_data("kakaotalk","show_count",((count//10)*10)-10,user_id)
        count = SQL_function.search_data("kakaotalk","show_count",user_id,opt=1)[0]
        if len(DB) == 0:
            message = Send_Button("미안해 동행이 가능한 사람이 없는거 같아..","처음으로","정보 수정할래")
        else:
            if len(DB)>count:
                SHOWDB[user_id] = DB
                message = UserShow(user_id,SHOWDB[user_id])
            else:
                message = send_message("더 이상 가능한 사람이 없어! 지금까지 보여준 사람중에 선택해봐!")
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer =="그만보기":
        del SHOWDB[user_id]
        del IDDB[user_id]
        message = Send_Button("원하는 동행상대를 찾았길 바래!\n다시 찾아보려면 동행 찾아볼래!를 선택해줘","처음으로","동행 찾아볼래!")
    
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer =="동행 찾아볼래!":
        SQL_function.update_data("kakaotalk","show_count",0,user_id)
        message = UserProfile_Button("현재 저장된 정보를 확인해봐\n성별 : {}  나이 : {}\n여행지 : {}\n여행날짜 : {}\n어필태그 : {}\n같은 정보로 찾아줄까?".format(SQL_function.search_data("kakaotalk","sex",user_id,1)[0],SQL_function.search_data("kakaotalk","age",user_id,1)[0],(SQL_function.search_data("kakaotalk","country",user_id,1)[0]+' '+SQL_function.search_data("kakaotalk","city",user_id,1)[0]),(SQL_function.search_data("kakaotalk","start_date",user_id,1)[0] + '~'+SQL_function.search_data("kakaotalk","end_date",user_id,1)[0]),SQL_function.search_data("kakaotalk","appeal_tag",user_id,1)[0]),user_id,"응","정보 수정할래","내 프로필 사진 볼래")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","user_state",user_id,1)[0] == "Existing" and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer =="정보 수정할래":
        message = Change_Button()

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "이사람이 좋아 연락처 줘" :
        num = SQL_function.search_data("kakaotalk","open_cnt",user_id,1)[0]
        if num < 3:
            SQL_function.update_data("kakaotalk","open_cnt",num+1,user_id)
            message = send_message("카카오톡 ID : {}".format(IDDB[user_id][0]))
        elif num >= 3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "이사람이 좋아! 연락처 줘" :
        num = SQL_function.search_data("kakaotalk","open_cnt",user_id,1)[0]
        if num < 3:
            SQL_function.update_data("kakaotalk","open_cnt",num+1,user_id)
            message = send_message("카카오톡 ID : {}".format(IDDB[user_id][1]))
        elif num >= 3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
        
        
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == 'done' and answer == "이사람이 좋아!! 연락처 줘" :
        num = SQL_function.search_data("kakaotalk","open_cnt",user_id,1)[0]
        if num < 3:
            SQL_function.update_data("kakaotalk","open_cnt",num+1,user_id)
            message = send_message("카카오톡 ID : {}".format(IDDB[user_id][2]))
        elif num >=3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")

    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "이사람이 좋아!!! 연락처 줘" :
        num = SQL_function.search_data("kakaotalk","open_cnt",user_id,1)[0]
        if num < 3:
            SQL_function.update_data("kakaotalk","open_cnt",num+1,user_id)
            message = send_message("카카오톡 ID : {}".format(IDDB[user_id][3]))
        elif num >= 3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "이사람이 좋아!!!! 연락처 줘" :
        num = SQL_function.search_data("kakaotalk","open_cnt",user_id,1)[0]
        if num < 3:
            SQL_function.update_data("kakaotalk","open_cnt",num+1,user_id)
            message = send_message("카카오톡 ID : {}".format(IDDB[user_id][4]))
        elif num >= 3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "이사람이 좋아!!!!! 연락처 줘" :
        num = SQL_function.search_data("kakaotalk","open_cnt",user_id,1)[0]
        if num < 3:
            SQL_function.update_data("kakaotalk","open_cnt",num+1,user_id)
            message = send_message("카카오톡 ID : {}".format(IDDB[user_id][5]))
        elif num >= 3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
    
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "이사람이 좋아!!!!!! 연락처 줘" :
        num = SQL_function.search_data("kakaotalk","open_cnt",user_id,1)[0]
        if num < 3:
            SQL_function.update_data("kakaotalk","open_cnt",num+1,user_id)
            message = send_message("카카오톡 ID : {}".format(IDDB[user_id][6]))
        elif num >= 3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
    
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "이사람이 좋아!!!!!!! 연락처 줘" :
        num = SQL_function.search_data("kakaotalk","open_cnt",user_id,1)[0]
        if num < 3:
            SQL_function.update_data("kakaotalk","open_cnt",num+1,user_id)
            message = send_message("카카오톡 ID : {}".format(IDDB[user_id][7]))
        elif num >= 3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "이사람이 좋아!!!!!!!! 연락처 줘" :
        num = SQL_function.search_data("kakaotalk","open_cnt",user_id,1)[0]
        if num < 3:
            SQL_function.update_data("kakaotalk","open_cnt",num+1,user_id)
            message = send_message("카카오톡 ID : {}".format(IDDB[user_id][8]))
        elif num >= 3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "이사람이 좋아!!!!!!!!! 연락처 줘" :
        num = SQL_function.search_data("kakaotalk","open_cnt",user_id,1)[0]
        if num < 3:
            SQL_function.update_data("kakaotalk","open_cnt",num+1,user_id)
            message = send_message("카카오톡 ID : {}".format(IDDB[user_id][9]))
        elif num >= 3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
    
    elif not SQL_function.is_user_new("kakaotalk",user_id) and SQL_function.search_data("kakaotalk","dialog_state",user_id,1)[0] == "done" and answer == "이사람이 좋아!!!!!!!!!! 연락처 줘" :
        num = SQL_function.search_data("kakaotalk","open_cnt",user_id,1)[0]
        if num < 3:
            SQL_function.update_data("kakaotalk","open_cnt",num+1,user_id)
            message = send_message("카카오톡 ID : {}".format(IDDB[user_id][10]))
        elif num >= 3:
            message = send_message("금일 검색가능한 횟수를 초과했어! 더 알고싶으면 결제를 해야해")
    
    else:
        message = send_message("미안해 잘 못알아들었어! 다시 말해줄래?")

    return jsonify(message)




if __name__ == "__main__":
    app.run(host='0.0.0.0',port =5000)



