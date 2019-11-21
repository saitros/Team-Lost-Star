import requests
from config import SEND_MESSAGE,SEND_PHOTO,EDIT_MESSAGE_TEXT,GET_FILE_PATH,GET_FILE,EDIT_MEDIA,DELETE_MESSAGE,EDIT_CAPTION
import db
import imgur_api_call
import button_maker as button
from PIL import Image
from io import BytesIO
from telegram import InputMediaPhoto
import imgur_api_call

class TelegramBot:

    def __init__(self):

        self.chat_id = None
        self.text = None
        self.name = None
        self.state = None
        self.is_member = False
        self.message_id = None
    def __call__(self, data):

        if not 'callback_query' in data.keys():

            if 'photo' in data['message'].keys():

                chat_id = data['message']['chat']['id']
                msg = data['message']['photo'][0]['file_id']
                user_name = data['message']['chat']['first_name'] + data['message']['chat']['last_name']
                self.chat_id = str(chat_id)
                self.text = msg
                self.name = user_name
            else:
                chat_id = data['message']['chat']['id']
                msg = data['message']['text']
                user_name = data['message']['chat']['first_name'] + data['message']['chat']['last_name']
                message_id = data['message']['message_id']
                self.chat_id = str(chat_id)
                self.text =msg
                self.name = user_name
                self.message_id = message_id

        else:
            chat_id = data['callback_query']['from']['id']
            #msg = data['callback_query']['data']
            user_name = data['callback_query']['from']['first_name'] + data['callback_query']['from']['last_name']
            self.chat_id = str(chat_id)
            self.text = data
            self.name = user_name

        # 신규 고객이면 db insert
        isExist = db.get_user(self.chat_id)

        #신규고객
        if not isExist:
            db.insert_user(self.chat_id,self.name)
        #기존고객이라면 isnew변수 update
        else:
            if db.get_single_value(self.chat_id, 'user_state'):
               self.is_member = True

        # 사용자의 현재 상태 저장
        self.state = db.get_single_value(self.chat_id,'dialog_state')



    def send_message(self,text,keyboard=None):

        if not keyboard:
            params = {'chat_id': self.chat_id, 'text': text}
            requests.post(SEND_MESSAGE, json=params)
        else:
            params = {'chat_id': self.chat_id, 'text': text,'reply_markup':keyboard}
            requests.post(SEND_MESSAGE, json=params)

    def edit_message(self,text,message_id,keyboard=None):

        if not keyboard:
            print("edit_message")
            params = {'chat_id': self.chat_id, 'text': text,'message_id':message_id}
            requests.post(EDIT_MESSAGE_TEXT, json=params)
        else:
            params = {'chat_id': self.chat_id, 'text': text,'message_id': message_id, 'reply_markup': keyboard}
            requests.post(EDIT_MESSAGE_TEXT, json=params)


    def send_img(self, url,caption,keyboard=None):
        if keyboard:
            params = {'chat_id': self.chat_id, 'caption': caption, 'photo' : url,'reply_markup':keyboard}
            requests.post(SEND_PHOTO, json=params)
        else:
            params = {'chat_id': self.chat_id, 'caption': caption, 'photo': url}
            requests.post(SEND_PHOTO, json=params)
        # params = {'chat_id': self.chat_id, 'caption': caption}
        # requests.post(SEND_PHOTO, data=params, files={'photo': url})

        # if keyboard is not None:
        #     params = {'chat_id': self.chat_id, 'caption' : caption, 'reply_markup' : keyboard}
        #     requests.post(SEND_PHOTO, json=params, files = {'photo': url})
        # else:
        #     params = {'chat_id': self.chat_id, 'caption': caption}
        #     requests.post(SEND_PHOTO, json=params, files={'photo': url})

    def save_image2db(self,file_id):

        params = {'file_id': file_id}
        res = requests.post(GET_FILE_PATH, json=params)
        path = (res.json())['result']['file_path']

        #print(GET_FILE+path)
        url=imgur_api_call.img_upload(GET_FILE+path)
        print(url)
        db.insert_value(self.chat_id,"profile_image",url)
        # res = requests.get(GET_FILE+path)
        # img = Image.open(BytesIO(res.content))
        # img.save(self.chat_id+'.png')

    def edit_media(self,url,id,keyboard):

        print("edit_media")
        params = {'chat_id': self.chat_id, 'message_id': id, "media":  {'type':'photo','media' : url},'reply_markup':keyboard}
        requests.post(EDIT_MEDIA, json=params)


    def delete_message(self, message_id):


        params = {'chat_id': self.chat_id, 'message_id': message_id}
        requests.post(DELETE_MESSAGE, json=params)

    def edit_caption(self,text,id,keyboard):

        print("edit_caption")
        params = {'chat_id': self.chat_id, 'message_id': id, "caption": text,'reply_markup':keyboard}
        requests.post(EDIT_CAPTION, json=params)