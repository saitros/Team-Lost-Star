from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove,ReplyKeyboardMarkup
import calendar
import datetime
import requests
from telegram_modules.config import ANSWER_CALLBACK_QUERY, EDIT_MESSAGE_TEXT, EDIT_MESSAGE_REPLY_MARKUP,DELETE_MESSAGE,SEND_MESSAGE
import telegram_modules.db as db
# import telegram_modules.button_maker as button

def show_userinfo(bot):
    bot.send_message("너의 정보가 아래와 같이 수정 되었어")
    result = db.get_userinfo("telegram",str(bot.chat_id))

    text = '''성별 : {}\n나이 : {}\n여행지 : {}\n여행기간 : {}\n여행정보 : {}\n''' \
        .format(result['sex'][0], result['age'][0], result['city'][0], result['start_date'][0] \
                + "  ~  " + result['end_date'][0], result['appeal_tag'][0])

    bot.send_img(result['profile_image'][0],text,button.update_button())
    #bot.send_message(" ", button.existing_user_keyboard())

def main_keyboard():

    keyboard = {
            'keyboard':[[{
                    'text': '동행 시작'
                        },
                    {'text': '여행 정보'
                        }
                    ]
                    ],
            'one_time_keyboard' : False
            }
    return keyboard

def existing_user_keyboard():

    keyboard = {
        'keyboard': [[
            {'text': '새로운 여행 등록'},{'text': '동행 찾기'},{'text' : '사용자 정보 수정'},{'text' : '홈으로'}]],
        'one_time_keyboard': False
    }
    return keyboard

def userinfo_update_keyboard():

    keyboard = {
        'keyboard': [[
            {'text': '사진 바꾸기'},{'text': '태그 바꾸기'},{'text' : '여행 일정 바꾸기'},{'text' : '여행지 바꾸기'}]],
        'one_time_keyboard': False

    }
    return keyboard


def create_binary_callback_data(button_type,category):
    """ Create the callback data associated to each button"""
    return ";".join([button_type,category])


def create_calendar_callback_data(action,year,month,day):
    """ Create the callback data associated to each button"""
    return ";".join(['calendar',action,str(year),str(month),str(day)])



def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")

def sex():

    keyboard = []
    row = []

    keyboard.append([InlineKeyboardButton("남자",callback_data=create_binary_callback_data('sex',"남자"))])
    keyboard.append([InlineKeyboardButton("여자",callback_data=create_binary_callback_data('sex',"여자"))])

    return InlineKeyboardMarkup(keyboard).to_json()


def update_button():

    keyboard = []

    keyboard.append([InlineKeyboardButton("사진 바꾸기",callback_data="사진 바꾸기")])
    keyboard.append([InlineKeyboardButton("태그 바꾸기",callback_data="태그 바꾸기")])
    keyboard.append([InlineKeyboardButton("여행 일정 바꾸기",callback_data="여행 일정 바꾸기")])
    keyboard.append([InlineKeyboardButton("여행지 바꾸기",callback_data="여행지 바꾸기")])


    return InlineKeyboardMarkup(keyboard).to_json()


def country_button():


    _list = db.GetCountryList("telegram","123")

    keyboard = []
    for country in _list:
        keyboard.append([InlineKeyboardButton(country, callback_data="나라;"+country)])


    return InlineKeyboardMarkup(keyboard).to_json()

def info_category_button():

    keyboard = []
    keyboard.append([InlineKeyboardButton("전통음식",callback_data="정보종류;전통음식")])
    keyboard.append([InlineKeyboardButton("추천 음식점",callback_data="정보종류;추천 음식점")])
    keyboard.append([InlineKeyboardButton("여행지",callback_data="정보종류;여행지")])


    return InlineKeyboardMarkup(keyboard).to_json()

def food_button(bot):


    foods = db.GetInfoList("telegram",bot.chat_id,"먹거리")
    keyboard = []
    for food in foods:
        keyboard.append([InlineKeyboardButton(food, callback_data="전통음식;"+food)])

    return InlineKeyboardMarkup(keyboard).to_json()




def create_calendar(year=None,month=None,start="여행 시작일",end="여행 종료일"):

    '''
    :param year,month : 사용자에게 보여질 달력에 필요한 날짜 정보
    :return: telegram 서버에 전달만 하면 되는 완성된 inline keyboard button
    '''

    keyboard = []

    # next / prev 버튼 안 누른 경우
    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month

    # 날짜, next/prev 버튼과 상관없는 버튼들의 callback_data 설정
    data_ignore = create_calendar_callback_data("IGNORE", year, month, 0)

    #첫번째 줄 생성
    row=[]
    row.append(InlineKeyboardButton(calendar.month_name[month]+" "+str(year),callback_data=data_ignore))
    keyboard.append(row)

    #두번째 줄 생성
    row=[]
    for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
        row.append(InlineKeyboardButton(day,callback_data=data_ignore))
    keyboard.append(row)

    #달력 날짜 생성
    my_calendar = calendar.monthcalendar(year, month)

    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(InlineKeyboardButton(" ",callback_data=data_ignore))

            else:
                row.append(InlineKeyboardButton(str(day),callback_data=create_calendar_callback_data("DAY",year,month,day)))

        keyboard.append(row)

    # prev/next 버튼 생성
    row=[]
    row.append(InlineKeyboardButton("<",callback_data=create_calendar_callback_data("PREV-MONTH",year,month,day)))
    row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
    row.append(InlineKeyboardButton(">",callback_data=create_calendar_callback_data("NEXT-MONTH",year,month,day)))

    keyboard.append(row)



    # start-end 버튼 생성
    row=[]

    row.append(InlineKeyboardButton(start,callback_data=data_ignore))
    row.append(InlineKeyboardButton("~", callback_data=data_ignore))
    row.append(InlineKeyboardButton(end, callback_data=data_ignore))
    keyboard.append(row)

    row = []
    row.append(InlineKeyboardButton("여행 기간 선택 완료", callback_data=create_calendar_callback_data("FINISH",year,month,0)))
    keyboard.append(row)
    return InlineKeyboardMarkup(keyboard).to_json()

def process_calendar_selection(bot):


    query = bot.text['callback_query']

    # 사용자가 실제로 달력의 버튼을 누른다면 위의 create_calendar를 만들때 설정한 callback_data가 돌아오게 된다
    # 그 callback_data는 ';'으로 구분했고 아래에서 ';' 을 구분자로 쪼개서 사용자의 버튼 입력 정보를 저장한다
    action = separate_callback_data(query['data'])[1] #IGNORE인지/DAY인지/PREV-MONTH인지/NEXT-MONTH인지
    year = separate_callback_data(query['data'])[2]
    month = separate_callback_data(query['data'])[3]
    day = separate_callback_data(query['data'])[4]

    curr = datetime.datetime(int(year), int(month), 1)

    if action == "IGNORE":
        params = {'callback_query_id': query['id']}
        requests.post(ANSWER_CALLBACK_QUERY, json=params)

    elif action == "DAY":

        # params = {'chat_id': query['message']['chat']['id'], 'message_id': query['message']['message_id']}
        # requests.post(DELETE_MESSAGE_URL, json=params)
        date = datetime.datetime(int(year), int(month), int(day))



        return str(date.strftime("%Y-%m-%d"))

    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)

        params = {'chat_id': query['message']['chat']['id'], 'text': query['message']['text'],
                  'message_id': query['message']['message_id'],
                  'reply_markup': create_calendar(int(pre.year), int(pre.month))}

        requests.post(EDIT_MESSAGE_TEXT, json=params)


    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        params = {'chat_id': query['message']['chat']['id'], 'text': query['message']['text'],
                  'message_id': query['message']['message_id'],
                  'reply_markup': create_calendar(int(ne.year), int(ne.month))}

        requests.post(EDIT_MESSAGE_TEXT, json=params)

    elif action == "FINISH":

        if bot.state == "date":
            db.insert_two_value(bot.chat_id,"dialog_state","is_end",'city',0)
            text = "내가 가봤던곳 중 가장 좋았던 여행지는 어린왕자와 함께한 B612 행성인데!!\n너는 어디로 떠나?(예시: 파리 O , 프랑스 파리 X)"
            #bot.send_message("내가 가봤던곳 중 가장 좋았던 여행지는 B612 행성인데, 너는 어디로 떠나?(예시: 파리 O , 프랑스 파리 X)")
            bot.send_img("https://i.pinimg.com/564x/63/7b/f6/637bf69ded8c4025036ef21a9dc75ec6.jpg",text)

        elif bot.state == "update_date":

            show_userinfo(bot)
            db.insert_two_value(bot.chat_id, "dialog_state","is_end","update",0)


    return None

def swiping_button():

    row = []
    keyboard= []
    row.append(InlineKeyboardButton("<", callback_data="LEFT"))
    row.append(InlineKeyboardButton(">", callback_data="RIGHT"))
    keyboard.append(row)
    return InlineKeyboardMarkup(keyboard).to_json()


def kakao_button(kakao_id):

    keyboard = []
    keyboard.append([InlineKeyboardButton("카카오id 보기",callback_data="kakao_id"+';'+kakao_id)])

    return InlineKeyboardMarkup(keyboard).to_json()


def city_button(bot,res=True):

    citys = db.GetCityList("telegram",bot.chat_id)

    keyboard = []
    if not res:
        for city in citys:

            keyboard.append([InlineKeyboardButton(city, callback_data="도시이름" + ';' + city+";"+"음식점")])
    else:
        for city in citys:
            keyboard.append([InlineKeyboardButton(city, callback_data="도시이름" + ';' + city+";"+"여행지")])

    return InlineKeyboardMarkup(keyboard).to_json()

def restaurant_button(bot):


    restaurants = db.GetInfoCity("telegram",bot.chat_id,"음식점")
    print(restaurants)
    keyboard = []
    for restaurant in restaurants:
        keyboard.append([InlineKeyboardButton(restaurant, callback_data="음식점이름;"+restaurant)])

    return InlineKeyboardMarkup(keyboard).to_json()

def place_button(bot):


    places = db.GetInfoCity("telegram",bot.chat_id,"여행지")

    keyboard = []
    for place in places:
        keyboard.append([InlineKeyboardButton(place, callback_data="여행지;"+place)])

    return InlineKeyboardMarkup(keyboard).to_json()