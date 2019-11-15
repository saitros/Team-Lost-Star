from flask import Flask, request, jsonify, redirect, url_for
import sys
app = Flask(__name__)
USERINFO = {}
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

def post(message):
    return jsonify(message)

@app.route('/IsUserNew', methods=['POST'])
def IsUserNew():
    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    if user_id not in USERINFO.keys():
        USERINFO[user_id]={}
        USERINFO[user_id]['LastMessage'] = user_answer
    else:
        pass


    print(USERINFO)

    message = send_message("넌 남자니 여자니")

    #UserSex로 재연결
    return message

@app.route('/UserSex/', methods=['POST'])
def UserSex():

    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    USERINFO[user_id]['Sex']=user_answer
    print(USERINFO)
    return jsonify(content)
# # @app.route('/test',methods=['POST'])
# def test():
#     send_message('성별이 뭐야')
#     content = request.get_json()
#     user_id = content['userRequest']['user']['id']
#     user_answer = content['userRequest']['utterance']
#     USERINFO[user_id]['SEX']=user_answer
#     send_message('나이는 몇살이야')
#     content = request.get_json()
#     user_id = content['userRequest']['user']['id']
#     user_answer = content['userRequest']['utterance']
#     USERINFO[user_id]['Age']=user_answer
#     print(USERINFO)
#     return jsonify(content)
@app.route('/UserAge', methods=['POST'])
def UserAge():
    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    USERINFO[user_id]['Age']=user_answer
    print(USERINFO)
    return jsonify(content)

@app.route('/UserPhoto', methods=['POST'])
def UserPhoto():
    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    USERINFO[user_id]['Photo']=user_answer
    print(USERINFO)
    
    return jsonify(content)

@app.route('/UserCountry',methods=['POST'])
def UserCountry():
    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    USERINFO[user_id]['Country']=user_answer
    print(USERINFO)
    
    return jsonify(content)

@app.route('/UserCity',methods=['POST'])
def UserCity():
    content = request.get_json()
    user_id = content['userRequest']['user']['id']
    user_answer = content['userRequest']['utterance']
    USERINFO[user_id]['City']=user_answer
    print(USERINFO)
    message = send_message("너는 {}고 나이는 {}살이고 {} {} 여행하는거 맞지?".format(USERINFO[user_id]['Sex'],USERINFO[user_id]['Age'],USERINFO[user_id]['Country'],USERINFO[user_id]['City']))
    return jsonify(message)

@app.route('/start', methods=['POST'])
def Message():
    
    content = request.get_json()
    print(content)
    content = content['userRequest']['utterance']
    
    if content == "동행 찾아볼래!":
        message = send_message("동행 찾아줄게!")

    elif content == "여행정보 알아볼래":
        message = send_message("여행정보 알려줄게!")

    else :
        message = send_message("아직 공부하고있습니다.")

    return jsonify(message)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port =5000)



