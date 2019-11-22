import telegram_modules.db as db
import telegram_modules.button_maker as button
from telegram_modules.CheckInput import CheckCityName
import random

def show_userinfo(bot):

    result = db.search_data("telegram", "*", bot.chat_id)[0]
    text = '''성별 : {}\n나이 : {}\n여행지 : {}\n여행기간 : {}\n태그 : {}\n''' \
        .format(str(result[2]), result[3],
                result[4], result[5] + "  ~  " + result[6],
                result[7])
    bot.send_img(result[11], text,button.update_button())

def create_callback_data(button_type,category):
    """ Create the callback data associated to each button"""
    return ";".join([button_type,category])

def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def send_profile(bot,edit,telegram,matched_person_info,match_photo_id):

    if telegram:
        img_url = matched_person_info[11]

        text = '''성별 : {}\n나이 : {}\n여행지 : {}\n여행기간 : {}\n태그 : {}\n''' \
            .format(str(matched_person_info[2]), matched_person_info[3],
                    matched_person_info[4], matched_person_info[5] + "  ~  " + matched_person_info[6],
                    matched_person_info[7])

        if edit:
            bot.edit_media(img_url, match_photo_id, button.kakao_button(matched_person_info[17]))
            bot.edit_caption(text, match_photo_id, button.kakao_button(matched_person_info[17]))

        else:
            bot.send_img(matched_person_info[11], text, button.kakao_button(matched_person_info[5]))
    else:
        img_url = matched_person_info[4]

        text = '''성별 : {}\n나이 : {}\n여행지 : {}\n여행기간 : {}\n태그 : {}\n''' \
            .format(str(matched_person_info[2]), matched_person_info[3],
                    matched_person_info[6], matched_person_info[7] + "  ~  " + matched_person_info[8],
                    matched_person_info[9])

        if edit:
            bot.edit_media(img_url, match_photo_id, button.kakao_button(matched_person_info[5]))
            bot.edit_caption(text, match_photo_id, button.kakao_button(matched_person_info[5]))
        else:
            bot.send_img(matched_person_info[4], text, button.kakao_button(matched_person_info[5]))








# 사용자의 버튼 입력 컨트롤러
def button_controller(bot):

    query = bot.text['callback_query']

    # 어떤 keyboard 입력인지 구분
    button_type = separate_callback_data(query['data'])[0]

    try:
        if bot.state == 'sex':

            sex = separate_callback_data(query['data'])[1]
            db.insert_value(bot.chat_id,'sex',sex)
            db.insert_value(bot.chat_id,'dialog_state', "age")

            bot.send_message("이번에는 너의 나이를 알고 싶어\n숫자만 써줘!!!")

        elif bot.state == 'date' or bot.state=="update_date":

            message_id = query['message']['message_id']
            #text = query['message']['text']

            user_input = button.process_calendar_selection(bot)

            if user_input:
                print(user_input)

                if not db.get_single_value(bot.chat_id,'is_end'):
                    # db.insert_value(bot.chat_id,'start_date',user_input)
                    # db.insert_value(bot.chat_id,'is_end',1)
                    db.insert_two_value(bot.chat_id,"start_date","is_end",user_input,1)
                    start = db.get_single_value(bot.chat_id,'start_date')
                    end = db.get_single_value(bot.chat_id, 'end_date')
                    bot.edit_message("여행 일정 선택",message_id,button.create_calendar(start=start,end=end))

                else:
                    db.insert_two_value(bot.chat_id, "end_date", "is_end", user_input, 0)
                    # db.insert_value(bot.chat_id,'end_date',user_input)
                    # db.insert_value(bot.chat_id,'is_end',0)
                    start = db.get_single_value(bot.chat_id, 'start_date')
                    end = db.get_single_value(bot.chat_id, 'end_date')
                    bot.edit_message("여행 일정 선택", message_id, button.create_calendar(start=start,end=end))


        elif button_type =="kakao_id":

            open_cnt = db.get_single_value(bot.chat_id, "open_cnt")

            if open_cnt > 3:
                bot.send_message("카카오톡id는 하루에 3번만 볼 수 있어 ㅜㅜ")
            else:
                bot.send_message(separate_callback_data(query['data'])[1])


            db.insert_value(bot.chat_id,"open_cnt",int(open_cnt)+1)

        elif bot.state == "match":

            prev_or_next = query['data']

            #update할 메세지 id
            match_photo_id = db.get_single_value(bot.chat_id, "match_photo_id")

            #db에서 리스트 받아온다
            matched_list = (db.get_single_value(bot.chat_id,"matched_list")).split(",")
            match_cnt = len(matched_list)

            #현재 사용자의 idx (초기값은 0)
            idx = db.get_single_value(bot.chat_id, "match_idx")

            if prev_or_next == "RIGHT":
                idx += 1
                if idx >= match_cnt:
                    idx=0
                db.insert_value(bot.chat_id, "match_idx", int(idx))
            else:

                idx -= 1
                if idx<0:
                    idx = match_cnt-1

                db.insert_value(bot.chat_id, "match_idx", int(idx))

            #방향키 액션에 의한 인덱스에 대한 사람 찾기
            matched_person_platform = matched_list[idx][0]
            matched_person_id = matched_list[idx][1:]

            if matched_person_platform == 't':

                matched_person_info = db.search_data("telegram","*",matched_person_id)[0]
                send_profile(bot,edit=True,telegram=True,matched_person_info=matched_person_info,match_photo_id=match_photo_id)


            elif matched_person_platform =='k':

                matched_person_info = db.search_data("kakaotalk", "*", matched_person_id)[0]
                send_profile(bot, edit=True, telegram=False, matched_person_info=matched_person_info,match_photo_id=match_photo_id)


            elif matched_person_platform == 'f':

                matched_person_info = db.search_data("facebook", "*", matched_person_id)[0]
                send_profile(bot, edit=True, telegram=False, matched_person_info=matched_person_info,match_photo_id=match_photo_id)


        elif bot.state == "update":

            data = query['data']
            print(data)
            if data == "사진 바꾸기":

                db.insert_value(bot.chat_id, "dialog_state", "update")
                bot.send_message("바꾸고 싶은 사진을 올려줘",button.existing_user_keyboard())


            elif data == "태그 바꾸기":

                db.insert_value(bot.chat_id, "dialog_state", "update_appeal_tag")
                bot.send_message("변경할 내용을 작성해서 보내줘", button.existing_user_keyboard())

            elif data == "여행 일정 바꾸기":
                db.insert_value(bot.chat_id, "dialog_state", "update_date")
                bot.send_message("아래 달력으로 여행 일정 수정해", button.existing_user_keyboard())
                bot.send_message("여행일정 선택", button.create_calendar())

            elif data == "여행지 바꾸기":
                db.insert_value(bot.chat_id, "dialog_state", "update_city")
                bot.send_message("변경할 여행지를 입력해줘",button.existing_user_keyboard())

        elif button_type == "나라":

            country = separate_callback_data(query['data'])[1]

            db.insert_value(bot.chat_id,"info_country",country)

            bot.send_message("이중에 어떤 정보가 필요해?",button.info_category_button())

        elif button_type == "정보종류":

            select=separate_callback_data(query['data'])[1]

            country = db.GetCountry("telegram",bot.chat_id)[0]

            if select == "전통음식":


                bot.send_message("{country}의 전통음식들이야\n 클릭하면 자세한 내용을 알려줄게".format(country=country),button.food_button(bot))



            elif select == "추천 음식점":

                bot.send_message("어떤 도시의 음식점 정보가 필요해?", button.city_button(bot))

            elif select == "여행지":

                bot.send_message("어떤 도시의 여행지 정보가 필요해?", button.city_button(bot))

        elif button_type == "전통음식":

            food = separate_callback_data(query['data'])[1]

            text = db.GetInfoDetail("telegram",bot.chat_id,"먹거리",food)[0]
            #print(str(text[0],"utf-8"))

            url = db.GetInfoDetail("telegram", bot.chat_id, "먹거리", food)[1]

            if url == "":
                url = "https://i.imgur.com/nGtXBZL.png"
            if text == "":
                text = "아직 설명을 준비중이야"
            bot.send_photo(url,button.main_keyboard())
            bot.send_message(text)

        elif button_type == "도시이름":

            city = separate_callback_data(query['data'])[1]
            res = separate_callback_data(query['data'])[2]

            db.insert_value(bot.chat_id,"info_city",city)

            if res == "음식점":
                bot.send_message(city+"의 추천음식점들이야 클릭하면 자세히 알려줄꼐",button.restaurant_button(bot))
            else:
                bot.send_message(city+"의 여행지들이야 클릭하면 자세히 알려줄꼐",button.place_button(bot))

        elif button_type == "음식점이름":

            restaurant = separate_callback_data(query['data'])[1]

            text = db.GetInfoDetail("telegram", bot.chat_id, "음식점", restaurant)[0]
            # print(str(text[0],"utf-8"))

            url = db.GetInfoDetail("telegram", bot.chat_id, "음식점", restaurant)[1]

            if url == "":
                url = "https://i.imgur.com/nGtXBZL.png"

            if text == "":
                text = "아직 설명을 준비중이야"
            bot.send_photo(url, button.main_keyboard())
            bot.send_message(text)

        elif button_type == "여행지":

            place = separate_callback_data(query['data'])[1]

            text = db.GetInfoDetail("telegram", bot.chat_id, "여행지", place)[0]
            # print(str(text[0],"utf-8"))

            url = db.GetInfoDetail("telegram", bot.chat_id, "여행지", place)[1]

            if url == "":
                url = "https://i.imgur.com/nGtXBZL.png"

            if text == "":
                text = "아직 설명을 준비중이야"
            bot.send_photo(url, button.main_keyboard())
            bot.send_message(text)


        else:
            bot.send_message("먼저 물어본거부터 대답해줄래?")
    except:
        bot.send_message("에러")



# 사용자의 텍스트 입력 컨트롤러
def text_controller(bot):


    if bot.text == '/start' or bot.text == "홈으로":
        bot.send_img("https://www.nypl.org/sites/default/files/maxresdefault_8.jpg","우리는 서로 길들이는 사이가 될 수 있을까?")

        bot.send_message("여행을 떠난다는 건 정말 행복한 일이지..\n\n여행을 하다보면 세상에 하나뿐인 친구를 만날 수도 있을꺼야\n\n"
                         + "아래 버튼 중에 원하는 버튼을 눌러보렴\n\n 그리고 지금 메인화면으로 오고 싶으면 언제든지"+'"'+ " 홈으로 "+'"'+"라고 치면 돼",button.main_keyboard())
        db.insert_value(bot.chat_id,"dialog_state","start")

    elif bot.text == '동행 시작':

        if bot.is_member == False:
            text = "나는 너에게 다른 수만 마리의 여우들과 다를바 없는\n똑같은 한마리의 여우일 뿐이지..\n하지만 우리가 서로 알게되면\n나는 너에게 세상에 하나뿐인 여우가 될거야\n내 질문에 대답해줄래?"
            bot.send_img("https://mblogthumb-phinf.pstatic.net/MjAxNzAyMDFfMjc1/MDAxNDg1OTEzMTk4ODcw.SkRJkcGDGMrK3wBwGg1CV2Jmn1nZNinv_v0k0hriiK0g.02XbcWWiN38RxSK5BiyG1AMaO20Wl5CK0U1AE_hLHe0g.JPEG.kumdongil/13402665_957088144411779_930553472_n.jpg?type=w2",text)
            bot.send_message("너의 성별을 알려줘",button.sex())
            db.insert_value(bot.chat_id, 'dialog_state', 'sex')
        else:
            result = db.get_userinfo("telegram",str(bot.chat_id))
            bot.send_message("{} 동안 {}에 간다고 기억하고 있는데 맞으면 동행 찾기를 눌러줘 새로운 여행을 원하면 새로운 여정을 알려줘"
            .format(result['start_date'][0]+"  ~  "+format(result['end_date'][0]), result['city'][0]),button.existing_user_keyboard())

    elif bot.text == "여행 정보":

        bot.send_message("내가 여행 정보를 줄 수 있는 나라들이야",button.country_button())

    elif bot.text == '사용자 정보 수정':

        db.insert_value(bot.chat_id,"dialog_state","update")
        bot.state = "update"
        show_userinfo(bot)

    elif bot.text == "새로운 여행 등록":

        db.insert_value(bot.chat_id, 'dialog_state', 'date')
        bot.send_message("새로운 여행의 기간을 골라줘", button.create_calendar())

    elif bot.text == "동행 찾기":


        _list=db.search_user("telegram",bot.chat_id)

        print("매칭된 사람들 리스트 입니다",_list)

        if _list:
            text = '좋아 성공적으로 너와 일정이 겹치는 동행들을 구해봤어!\n\n다음 사람들중에서 하루 최대 3명까지 카카오톡 ID를 알려줄꺼야\n\n하지만 알아둬\n동행을 찾는다는건 말이야\n아주 설레는 일이야 또 아주 무서운 일이기도 하지.\n\n너의 경험을 누구와 공유한다는건 정말 좋은 일이야\n그게 또 새로운 인연의 시작일 수도 있지\n하지만 잘못된 만남은 악연의 시작일 수도 있다는거 알아둬\n\n\n동행은 너가 혼자서 할 수 없는 일들을 가능하게 해줄꺼야\n할인, 다양한 음식, 사진찍기, 여행 정보 공유 등등\n하지만 너가 혼자서 할 수 있는 일들을 못하게 될 수도있어\n사람이 많아지면 변수도 많아지고 그러면 너의 여행이 계획대로\n흘러가지 않을 수도 있어'
            bot.send_message(text, button.swiping_button())
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


            matched_person_platform = matched_list[0][0]
            matched_person_id = matched_list[0][1:]


            if matched_person_platform == "t":


                match1_info = db.search_data("telegram", "*",matched_person_id)[0]
                send_profile(bot, edit=False, telegram=True, matched_person_info=match1_info, match_photo_id=None)

            elif matched_person_platform == "k":

                match1_info = db.search_data("kakaotalk","*",matched_person_id)[0]
                send_profile(bot, edit=False, telegram=False, matched_person_info=match1_info, match_photo_id=None)

            elif matched_person_platform == "f":
                match1_info = db.search_data("facebook","*",matched_person_id)[0]
                send_profile(bot, edit=False, telegram=False, matched_person_info=match1_info, match_photo_id=None)

            db.insert_value(bot.chat_id, "match_photo_id", bot.message_id +2)

        else:
            bot.send_message("동행을 찾지 못했어 ㅜㅜ", button.main_keyboard())



    elif bot.state == 'age':

        db.insert_value(bot.chat_id,'age',str(bot.text))
        db.insert_value(bot.chat_id,'dialog_state','profile_image')
        bot.send_message("너의 사진이 있으면 사람들이 알아보기 쉬울꺼야!\n사진 하나만 보내줄래?\n\n 대신 형식은 꼭!!!  [사진]으로 보내줘 [파일]은 아직 못 읽어ㅠㅠ")

    elif bot.state == "city":


        city = str(bot.text)
        city = CheckCityName(city)
        if city:

            db.insert_value(bot.chat_id, 'city', str(bot.text))

            db.insert_value(bot.chat_id,"dialog_state","kakao_id")

            bot.send_message("카카오톡 아이디를 알려주면 매칭된 사람들과 연락할 수 있는데 알려줄래?")
        else:
            bot.send_message("잘못된 도시 이름을 입력한 것 같은데 확인하고 다시 입력해줘")


    elif bot.state == "kakao_id":
        db.insert_three_value(bot.chat_id,"kakao_id","user_state","dialog_state",str(bot.text),1,'update')
        # db.insert_value(bot.chat_id, "kakao_id",str(bot.text))
        #
        show_userinfo(bot)
        # # 이제 더이상 신규회원X
        # db.insert_value(bot.chat_id, 'user_state', 1)
        #
        # db.insert_value(bot.chat_id, 'dialog_state', 'update')


    elif bot.state == "appeal_tag":
        db.insert_value(bot.chat_id,'appeal_tag',str(bot.text))

        db.insert_value(bot.chat_id, 'dialog_state', 'date')
        bot.send_message("여행 기간을 골라줘", button.create_calendar())


    elif bot.state == "update_appeal_tag":

        db.insert_value(bot.chat_id,"appeal_tag",str(bot.text))
        bot.send_message("너의 정보가 아래와 같이 수정되었어")
        db.insert_value(bot.chat_id,"dialog_state","update")

        show_userinfo(bot)

    elif bot.state == "update_city":


        city = str(bot.text)
        city = CheckCityName(city)
        if city:

            db.insert_value(bot.chat_id, 'city', city)

            bot.send_message("너의 정보가 아래와 같이 수정되었어")
            show_userinfo(bot)
            db.insert_value(bot.chat_id, "dialog_state", "update")

        else:
            bot.send_message("잘못된 도시 이름을 입력한 것 같은데 확인하고 다시 입력해줘")


    else:
        bot.send_message("아직 개발중이다!!!!")



if __name__ == "__main__":

    print(CheckCityName("바르셀로나"))
