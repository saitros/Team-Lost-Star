from flask import Flask,request
from telegram_bot import TelegramBot
import button_maker as button
from controller import button_controller,text_controller
import db
import time
app = Flask(__name__)


@app.route('/telegram', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':


        data = request.get_json()
        #print(data)
        bot = TelegramBot()
        bot(data)


        # 사용자의 text 입력 처리
        if not 'callback_query' in data.keys():

            #사용자가 사진 업로드 했을때는 여기로
            if 'photo' in data['message'].keys():

                #최초에 프로필 등록하기 위해 사진을 올린 경우
                if db.get_single_value(bot.chat_id,"dialog_state") == "profile_image":

                    bot.save_image2db(bot.text)
                    bot.send_message("너를 표현하는 태그를 남겨주면 관심있는 사람들이 볼 수 있어")
                    db.insert_value(bot.chat_id,'dialog_state','appeal_tag')

                #프로필 사진 변경을 위해 사진을 올린 경우
                elif db.get_single_value(bot.chat_id,"dialog_state") == "update":

                    bot.save_image2db(bot.text)
                    result = db.get_userinfo("telegram",str(bot.chat_id))
                    bot.send_message("너의 정보가 아래와 같이 수정되었어")


                    text = '''{}님이 입력하신 정보는 아래와 같습니다\n성별 : {}\n나이 : {}\n여행지 : {}\n여행기간 : {}\n여행정보 : {}\n''' \
                        .format(bot.name, result['sex'][0], result['age'][0], result['city'][0],
                                result['start_date'][0] \
                                + "  ~  " + result['end_date'][0], result['appeal_tag'][0])
                    bot.send_img(result['profile_image'][0],text,button.update_button())
                    db.insert_value(bot.chat_id,"dialog_state","update")

                else:
                    bot.send_message("갑자기 왠 사진??")


            else:
                # 사용자 로그
                print(bot.name + '(' + str(bot.chat_id) + ')' + '님이 ' + '[' + bot.text + ']' + '를 서버로 보냈습니다')

                text_controller(bot)


        # 사용자의 keyboard 입력 처리
        else:

            button_controller(bot)




    return ''

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
