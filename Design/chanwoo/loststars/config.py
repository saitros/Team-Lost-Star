# telegram bot 의 api_key
API_KEY = '1039143523:AAHTngxT5pk8WG_XSh562-vHoOvVxQj1fGI'

# webhook을 걸 url
WEBHOOK = 'https://5c4af050.ap.ngrok.io/telegram'


BOT_INFO = 'https://api.telegram.org/bot{API_KEY}/getMe'.format(API_KEY=API_KEY)

'''webhook을 통해서 우리 서버로 오지 못하고 telegram 서버에 쌓여있는 request정보들 보여주는 메소드
이 메소드를 통해서 쌓인 request들을 출력해보고 아래 url을 
https://api.telegram.org/bot{API_KEY}/getUpdates?offset=[request_id] 로 바꾸면 쌓인 request를 삭제할 수 있다'''
BOT_UPDATE = 'https://api.telegram.org/bot{API_KEY}/getUpdates?offset=54233209'.format(API_KEY=API_KEY)

# telegram과 bot과의 webhook 연결 해주는 메소드
BOT_SET_WEBHOOK= 'https://api.telegram.org/bot{API_KEY}/setWebhook?url={WEBHOOK_URL}'\
    .format(API_KEY=API_KEY, WEBHOOK_URL=WEBHOOK)

# telegram과 bot의 webhook을 끊어주는 메소드
BOT_DELETE= 'https://api.telegram.org/bot{API_KEY}/deleteWebhook'.format(API_KEY=API_KEY)


BOT_GET_INFO = 'https://api.telegram.org/bot{API_KEY}/getWebhookInfo'.format(API_KEY=API_KEY)

# 서버에서 telegram으로 메세지를 보내주는 메소드
SEND_MESSAGE = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)

# 서버에서 telegram으로 사진을 보내주는 메소드
SEND_PHOTO = 'https://api.telegram.org/bot{token}/sendPhoto'.format(token=API_KEY)

GET_FILE_PATH = "https://api.telegram.org/bot{token}/getFile".format(token=API_KEY)
GET_FILE = "https://api.telegram.org/file/bot{API_KEY}/".format(API_KEY=API_KEY)
ANSWER_CALLBACK_QUERY = 'https://api.telegram.org/bot{API_KEY}/answerCallbackQuery'.format(API_KEY=API_KEY)
EDIT_MESSAGE_TEXT = 'https://api.telegram.org/bot{API_KEY}/editMessageText'.format(API_KEY=API_KEY)
EDIT_MESSAGE_REPLY_MARKUP = 'https://api.telegram.org/bot{API_KEY}/editMessageReplyMarkup'.format(API_KEY=API_KEY)
DELETE_MESSAGE = 'https://api.telegram.org/bot{API_KEY}/deleteMessage'.format(API_KEY=API_KEY)

EDIT_MEDIA = 'https://api.telegram.org/bot{API_KEY}/editMessageMedia'.format(API_KEY=API_KEY)
EDIT_CAPTION = 'https://api.telegram.org/bot{API_KEY}/editMessageCaption'.format(API_KEY=API_KEY)

# db connection 정보
host_name = "localhost"
username = "root"
password = "!dnzlxkfh0520!"
database_name = "loststars"


