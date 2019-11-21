from googletrans import Translator
import requests
import json

API_KEY = "AIzaSyAjNDn5zApqM3juQPo74ur24OukKz_9MQY"

def CheckCityName(input_city):

    # 한국어 -> 영어 번역
    translator = Translator()
    en_city = translator.translate(str(input_city), src='ko', dest='en').text

    # 구글 Place API를 통해 도시 정확도 체크
    url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input={en_city}&key={API_KEY}".format(en_city=en_city,API_KEY=API_KEY)
    
    response = requests.get(url).text
    city_data = json.loads(response)

    # 결과가 없을 경우를 위한 예외처리
    try:
        api_city = city_data['predictions'][0]["structured_formatting"]["main_text"]

        # if input string is city, then types include "geocode"
        api_city_type = city_data['predictions'][0]["types"]
    except IndexError:
        return False

    # 구글 Place API의 main_text 결과와 비교
    if (en_city != api_city) or ("geocode" not in api_city_type):
        return False

    # 영어 -> 한국어 번역
    ko_city = translator.translate(en_city, src='en', dest='ko').text

    # 다시 한국어로 번역된 도시 이름 반환
    return ko_city




if __name__ == "__main__":
    city = CheckCityName("바르셀로나")
    print(type(city))
    if city is False:
        print("입력한 도시 이름을 확인해주세요\n")
    else:

        print("목적지가 {} 맞습니까?\n".format(city))
