import db
import button_maker as button
from PIL import Image
import time
import random

def show_userinfo(bot):

    result = db.get_userinfo("telegram",str(bot.chat_id))

    text = '''{}님이 입력하신 정보는 아래와 같습니다\n성별 : {}\n나이 : {}\n여행지 : {}\n여행기간 : {}\n여행정보 : {}\n''' \
        .format(bot.name, result['sex'][0], result['age'][0], result['city'][0], result['start_date'][0] \
                + "  ~  " + result['end_date'][0], result['appeal_tag'][0])
    bot.send_img(result['profile_image'][0],text,button.userinfo_update_keyboard())

    # if bot.state == "update":
    #
    #     bot.send_message("test",button.userinfo_update_keyboard())
    # else:
    #     bot.send_message("test", button.existing_user_keyboard())



def create_callback_data(button_type,category):
    """ Create the callback data associated to each button"""
    return ";".join([button_type,category])

def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")

# 사용자의 버튼 입력 컨트롤러
def button_controller(bot):

    query = bot.text['callback_query']

    # 어떤 keyboard 입력인지 구분
    button_type = separate_callback_data(query['data'])[0]


    if bot.state == 'sex':

        sex = separate_callback_data(query['data'])[1]
        db.insert_value(bot.chat_id,'sex',sex)
        db.insert_value(bot.chat_id,'dialog_state', "age")

        bot.send_message("이번에는 너의 나이를 알고 싶어")

    elif bot.state == 'date' or bot.state=="update_date":
        #
        message_id = query['message']['message_id']
        text = query['message']['text']

        user_input = button.process_calendar_selection(bot)

        if user_input:
            print(user_input)

            if not db.get_single_value(bot.chat_id,'is_end'):
                db.insert_value(bot.chat_id,'start_date',user_input)
                db.insert_value(bot.chat_id,'is_end',1)
                start = db.get_single_value(bot.chat_id,'start_date')
                end = db.get_single_value(bot.chat_id, 'end_date')
                bot.edit_message(text,message_id,button.create_calendar(start=start,end=end))

            else:
                db.insert_value(bot.chat_id,'end_date',user_input)
                db.insert_value(bot.chat_id,'is_end',0)
                start = db.get_single_value(bot.chat_id, 'start_date')
                end = db.get_single_value(bot.chat_id, 'end_date')
                bot.edit_message(text, message_id, button.create_calendar(start=start, end=end))



    elif bot.state == "match":

        prev_or_next = query['data']
        match_photo_id = db.get_single_value(bot.chat_id, "match_photo_id")
        print("==",match_photo_id)
        matched_list = (db.get_single_value(bot.chat_id,"matched_list")).split(",")
        print("matched_list" , matched_list)
        match_cnt = len(matched_list)

        idx = db.get_single_value(bot.chat_id,"match_idx")
        print(idx)

        if prev_or_next == "RIGHT":
            idx += 1
            db.insert_value(bot.chat_id,"match_idx",int(idx))
        else:
            idx -= 1
            db.insert_value(bot.chat_id, "match_idx", int(idx))
        if idx >= match_cnt or idx == -1:
            db.insert_value(bot.chat_id,"match_idx",0)
            idx = db.get_single_value(bot.chat_id, "match_idx")


        matched_person_platform = matched_list[idx][0]
        matched_person_id = matched_list[idx][1:]

        if matched_person_platform == 't':

            matched_person_info = db.get_userinfo("telegram",matched_person_id)

            img_url = matched_person_info['profile_image'][0]
            text = '''{}님의 정보는 아래와 같습니다\n성별 : {}\n나이 : {}\n여행지 : {}\n여행기간 : {}\n태그 : {}\n''' \
                .format(matched_person_info['user_id'][0], str(matched_person_info['sex'][0]), matched_person_info['age'][0],
                        matched_person_info['city'][0], matched_person_info['start_date'][0] + "  ~  " +matched_person_info['end_date'][0],
                        matched_person_info['appeal_tag'][0])

            bot.edit_media(img_url, match_photo_id)
            bot.edit_caption(text, match_photo_id)

        elif matched_person_platform =='k':
            matched_person_info = db.get_userinfo("kakaotalk", matched_person_id)

            img_url = matched_person_info['profile_image'][0]
            print(img_url)
            text = '''{}님의 정보는 아래와 같습니다\n성별 : {}\n나이 : {}\n여행지 : {}\n여행기간 : {}\n태그 : {}\n''' \
                .format(matched_person_info['user_id'][0], str(matched_person_info['sex'][0]),
                        matched_person_info['age'][0],
                        matched_person_info['city'][0],
                        matched_person_info['start_date'][0] + "  ~  " + matched_person_info['end_date'][0],
                        matched_person_info['appeal_tag'][0])
            print("=",match_photo_id)

            bot.edit_media(img_url, match_photo_id)
            bot.edit_caption(text, match_photo_id)

        elif matched_person_platform == 'f':

            matched_person_info = db.get_userinfo("facebook", matched_person_id)

            img_url = matched_person_info['profile_image'][0]
            text = '''{}님의 정보는 아래와 같습니다\n성별 : {}\n나이 : {}\n여행지 : {}\n여행기간 : {}\n태그 : {}\n''' \
                .format(matched_person_info['user_id'][0], str(matched_person_info['sex'][0]),
                        matched_person_info['age'][0],
                        matched_person_info['city'][0],
                        matched_person_info['start_date'][0] + "  ~  " + matched_person_info['end_date'][0],
                        matched_person_info['appeal_tag'][0])
            print(text)
            bot.edit_media(img_url, match_photo_id)
            bot.edit_caption(text, match_photo_id)


        # match_photo_id = db.get_single_value(bot.chat_id,"match_photo_id")
        # bot.edit_media("https://imgur.com/a/yWDcVZc",match_photo_id)
        # bot.edit_caption("바뀐다",match_photo_id)




# 사용자의 텍스트 입력 컨트롤러
def text_controller(bot):


    if bot.text == '/start':
        bot.send_message("여행을 떠난다는 건 정말 행복한 일이지,,\n나도 이 지구별에 여행온지 벌써 2342년이나 됐네\n"
                         + "아래 버튼 중에 원하는 버튼을 눌러보렴",button.main_keyboard())
        db.insert_value(bot.chat_id,"dialog_state","start")

    elif bot.text == '동행 시작':

        if bot.is_member == False:
            bot.send_message("다른 동행 구하는 사람들에게 너를 알려주기 위해서 너에 대해서 몇가지 알고싶어!  몇가지 질문에 대답해줬으면 좋겠어")
            bot.send_message("동행을 구하기 위해서는 우선적으로 너의 성별을 알려줘",button.sex())
            db.insert_value(bot.chat_id, 'dialog_state', 'sex')
        else:
            result = db.get_userinfo("telegram",str(bot.chat_id))
            bot.send_message("{} 동안 {}에 간다고 기억하고 있는데 맞으면 동행 찾기를 눌러줘 새로운 여행을 원하면 새로운 여정을 알려줘"
            .format(result['start_date'][0]+"  ~  "+format(result['end_date'][0]), result['city'][0]),button.existing_user_keyboard())

    elif bot.text == '사용자 정보 수정':

        db.insert_value(bot.chat_id,"dialog_state","update")
        bot.state = "update"
        show_userinfo(bot)


    elif bot.text == "사진 바꾸기":

        db.insert_value(bot.chat_id,"dialog_state","update_photo")
        bot.send_message("바꾸고 싶은 사진을 올려줘",button.userinfo_update_keyboard())



    elif bot.text == "태그 바꾸기":

        db.insert_value(bot.chat_id,"dialog_state","update_appeal_tag")
        bot.send_message("변경할 내용을 작성해서 보내줘",button.userinfo_update_keyboard())

    elif bot.text == "여행 일정 바꾸기":

        db.insert_value(bot.chat_id, "dialog_state", "update_date")
        bot.send_message("아래 달력으로 여행 일정 수정해",button.userinfo_update_keyboard())
        bot.send_message("여행일정 선택",button.create_calendar())




    elif bot.text == "여행지 바꾸기":

        db.insert_value(bot.chat_id,"dialog_state","update_city")
        bot.send_message("변경할 여행지를 입력해줘")

    elif bot.text == "새로운 여행 등록":

        db.insert_value(bot.chat_id, 'dialog_state', 'date')
        bot.send_message("새로운 여행의 기간을 골라줘", button.create_calendar())

    elif bot.text == "동행 찾기":


        _list=db.search_user("telegram",bot.chat_id)
        print(_list)
        if _list:
            bot.send_message("너와 어울리는 동행을 찾았어!", button.swiping_button())
            matched_list = []
            for item in _list:
                if item[1] == "telegram":
                    matched_list.append("t"+item[0])
                elif item[1] == "kakaotalk":
                    matched_list.append("k" + item[0])
                elif item[1] == "facebook":
                    matched_list.append("f" + item[0])


            random.shuffle(matched_list)
            matched_str = (",".join(matched_list))

            db.insert_value(bot.chat_id,"matched_list",matched_str)
            db.insert_value(bot.chat_id,"dialog_state","match")
            db.insert_value(bot.chat_id,"match_idx",0)


            match1 = _list[0]
            match1_info = db.get_userinfo("facebook",match1[0])
            #print(match1_info)


            text = '''{}님의 정보는 아래와 같습니다\n성별 : {}\n나이 : {}\n여행지 : {}\n여행기간 : {}\n태그 : {}\n''' \
                    .format(match1_info['user_id'][0], str(match1_info['sex'][0]), match1_info['age'][0], match1_info['city'][0], match1_info['start_date'][0]+ "  ~  " + match1_info['end_date'][0], match1_info['appeal_tag'][0])

            bot.send_img(match1_info['profile_image'][0],text,button.existing_user_keyboard())


            db.insert_value(bot.chat_id, "match_photo_id", bot.message_id +2)


        else:
            bot.send_message("동행을 찾지 못했어 ㅜㅜ", button.main_keyboard())
        #bot.delete_message(bot.message_id+3)
        #
        # for i in _list:
        #
        #     bot.send_img(open(str(i[0])+".png","rb"))
        #     text = '''{}님의 정보는 아래와 같습니다\n성별 : {}\n나이 : {}\n여행지 : {}\n여행기간 : {}\n여행정보 : {}\n''' \
        #         .format(i[1], str(i[2]), i[3], i[4], i[5]+ "  ~  " + i[6], i[7])
        #     bot.send_message(text,button.main_keyboard())


    elif bot.state == 'age':

        db.insert_value(bot.chat_id,'age',str(bot.text))
        db.insert_value(bot.chat_id,'dialog_state','profile_image')
        bot.send_message("너의 사진이 있으면 사람들이 알아보기 쉬울꺼야!")

    elif bot.state == "city":

        db.insert_value(bot.chat_id, 'city', str(bot.text))

        show_userinfo(bot)

        #이제 더이상 신규회원X
        db.insert_value(bot.chat_id,'user_state',1)

        db.insert_value(bot.chat_id,'dialog_state','search')


    elif bot.state == "appeal_tag":
        db.insert_value(bot.chat_id,'appeal_tag',str(bot.text))

        db.insert_value(bot.chat_id, 'dialog_state', 'date')
        bot.send_message("여행 기간을 골라줘", button.create_calendar())


    elif bot.state == "update_appeal_tag":

        db.insert_value(bot.chat_id,"appeal_tag",str(bot.text))
        bot.send_message("너의 정보가 아래와 같이 수정되었어")


        show_userinfo(bot)

    elif bot.state == "update_city":

        db.insert_value(bot.chat_id,"city",str(bot.text))
        bot.send_message("너의 정보가 아래와 같이 수정되었어")
        show_userinfo(bot)

    else:
        bot.send_message("아직 개발중이다!!!!")