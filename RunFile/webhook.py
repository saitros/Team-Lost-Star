from urllib.request import Request, urlopen
from telegram_modules.config import API_KEY,WEBHOOK,BOT_INFO,BOT_UPDATE,BOT_GET_INFO,BOT_DELETE,BOT_SET_WEBHOOK

## https://core.telegram.org/bots/api#getupdates

def bot_info_call():
    """
    bot 의 정보를 출력하는 함수
    """
    request = Request(BOT_INFO)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read().decode('utf-8')
    print(response_body)


def bot_update_call():
    """
    bot 의 업데이트 정보를 출력하는 함수
    """
    request = Request(BOT_UPDATE)
    print(BOT_UPDATE)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read().decode('utf-8')
    print(response_body)


def bot_set_webhook_call():
    """
    bot 의 Webhook 을 세팅하는 함수
    """
    request = Request(BOT_SET_WEBHOOK)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read().decode('utf-8')
    print(response_body)


def delete_webhook():
    """
    bot 의 Webhook 을 제거하는 함수
    """
    request = Request(BOT_DELETE)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read().decode('utf-8')
    print(response_body)

def get_webhook_info():
    request = Request(BOT_GET_INFO)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read().decode('utf-8')
    print(response_body)

if __name__ == '__main__':
    #bot_info_call()
    delete_webhook()
    #bot_update_call()
    bot_set_webhook_call()

    #get_webhook_info()