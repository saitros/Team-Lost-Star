import pymysql
import pandas as pd
from telegram_modules.config import host_name,username,password,database_name


def make_connection():

    conn = pymysql.connect(
        host=host_name,  # DATABASE_HOST
        port=3306,
        user=username,  # DATABASE_USERNAME
        passwd=password,  # DATABASE_PASSWORD
        db=database_name,  # DATABASE_NAME
        charset='utf8'
    )
    return conn


def get_user(chat_id):

    conn = make_connection()
    sql = "SELECT count(*) FROM telegram_user_tb WHERE id={}".format(chat_id)
    df = pd.read_sql(sql,conn)
    isNew = (df.loc[0, 'count(*)'])
    conn.close()
    return isNew


def insert_user(chat_id,name):
    conn = make_connection()
    sql = "INSERT INTO telegram_user_tb (id,user_id) VALUE (%s,%s)"

    val = (chat_id,name)

    mycursor = conn.cursor()
    mycursor.execute(sql,val)
    conn.commit()

    conn.close()

def insert_value(chat_id,column,value):

    conn = make_connection()
    sql = "UPDATE telegram_user_tb SET " + column + " = %s" + " WHERE id = " + chat_id

    mycursor = conn.cursor()

    mycursor.execute(sql,value)

    conn.commit()


    conn.close()

def insert_two_value(chat_id,c1,c2,v1,v2):

    conn = make_connection()
    sql = "UPDATE telegram_user_tb SET " + c1 + " = %s," +c2 + " = %s" + " WHERE id = " + chat_id

    mycursor = conn.cursor()

    value = (v1,v2)
    mycursor.execute(sql,value)

    conn.commit()


    conn.close()

def insert_three_value(chat_id,c1,c2,c3,v1,v2,v3):

    conn = make_connection()
    sql = "UPDATE telegram_user_tb SET " + c1 + " = %s," +c2 + " = %s,"+c3 + " = %s" + " WHERE id = " + chat_id

    mycursor = conn.cursor()

    value = (v1,v2,v3)
    mycursor.execute(sql,value)

    conn.commit()


    conn.close()

def get_state(chat_id):

    conn = make_connection()
    sql = "SELECT dialog_state FROM telegram_user_tb WHERE id={}".format(chat_id)
    df = pd.read_sql(sql, conn)
    cur_state = (df.loc[0, 'dialog_state'])
    conn.close()
    return cur_state

def get_single_value(chat_id,column):
    conn = make_connection()
    sql = "SELECT {} FROM telegram_user_tb WHERE id={}".format(column,chat_id)
    df = pd.read_sql(sql, conn)
    cur_state = (df.loc[0, column])
    conn.close()
    return cur_state

def get_userinfo(platform,chat_id):

    conn = make_connection()
    sql = "SELECT * FROM {}_user_tb WHERE id={}".format(platform,chat_id)
    df = pd.read_sql(sql, conn)

    result = df.to_dict()
    conn.close()
    return result


def get_userinfo(platform,chat_id):

    conn = make_connection()
    sql = "SELECT * FROM {}_user_tb WHERE id={}".format(platform,chat_id)
    df = pd.read_sql(sql, conn)

    result = df.to_dict()
    conn.close()
    return result


# 데이터 검색 기본값으로 fetchall
def search_data(platform, column = "*", id = "NULL", opt = 0):

    conn = make_connection()
    curs = conn.cursor()

    sql = "select {column} from {platform}_user_tb".format(column=column, platform=platform)





    if (id != "NULL"):
        sql = sql + " where id = (%s)"
        curs.execute(sql, id)

    else:
        curs.execute(sql)


    if (opt == 0):
        rows = curs.fetchall()
    else:
        rows = curs.fetchone()

    conn.close()
    return rows


# 동행 유저 검색
def search_user(platform, id):

    conn = make_connection()
    curs = conn.cursor()

    # 카카오톡 아이디 최대 열람 횟수, 테이블 갯수
    MAX_OPEN_CNT = 3
    MAX_TABLE_CNT = 3

    # 플랫폼 리스트
    platform_list = ["telegram", "facebook", "kakaotalk"]

    # open_cnt 조회, 최대 열람 횟수를 넘어가면 -1 리턴후 함수 종료
    cnt = search_data(platform, "open_cnt", id, 1)
    #print(cnt)
    # if (cnt[0] > MAX_OPEN_CNT):
    #     return -1

    # 2차원 tuple 형식으로 반환됨
    # print(city) --> (('파리',),)
    city = search_data(platform, "city", id)
    start_date = search_data(platform, "start_date", id, 1)
    end_date = search_data(platform, "end_date", id, 1)

    # 동행 유저 리스트 초기화
    trip_users = []

    # 모든 테이블 개별적으로 조인
    i = 0
    while (i < MAX_TABLE_CNT):
        other_platform = platform_list[i]
        i += 1
        sql = """select distinct t2.id from {platform}_user_tb as t1
                join {other_pf}_user_tb as t2
                on t1.city = t2.city
                where t2.city = %s 
                and t2.end_date >= %s and %s >= t2.start_date;""".format(platform=platform, other_pf=other_platform)
        curs.execute(sql, (city, start_date[0], end_date[0]))

        # 각 플랫폼에서 sql 조건에 해당하는 id 전부 가져오기
        id_list = curs.fetchall()

        # 같은 플랫폼 테이블 조인시 자기 자신은 제외
        if (platform == other_platform):

            id_list = list(id_list)
            id_list.remove(((id),))
            id_list = tuple(id_list)

        # 아이디 리스트에서 하나씩 뽑으면서 조회
        for item in id_list:
            #info = search_data(other_platform, "id, user_id, sex, age, city, start_date, end_date, appeal_tag", item)
            info = search_data(other_platform, "id", item)
            temp=list(info[0])
            temp.append(other_platform)
            trip_users.append(temp)



    conn.close()
    return trip_users


def GetCountryList(platform, id):
    sql = "select distinct country from info_trip_tb;"

    conn = make_connection()
    curs = conn.cursor()

    curs.execute(sql)

    # 튜플안에 튜플의 형태
    # ex) (('스페인',), ('필리핀',), ('포르투갈',), ('프랑스',), ('스위스',))
    rows = curs.fetchall()

    # 튜플의 각 원소만 리스트로 바꿈
    # ['스페인', '필리핀', '포르투갈', '프랑스', '스위스']
    country = list(map(lambda x: x[0], rows))

    conn.close()

    return country

# 유저가 선택한 나라를 가져오는 함수
def GetCountry(platform, id):
    sql = "select info_country from {platform}_user_tb where id = (%s)".format(platform=platform)
    conn = make_connection()
    curs = conn.cursor()
    curs.execute(sql, id)
    country = curs.fetchone()
    conn.close()

    return country

def GetCity(platform, id):
    sql = "select info_city from {platform}_user_tb where id = (%s)".format(platform=platform)
    conn = make_connection()
    curs = conn.cursor()
    curs.execute(sql, id)
    country = curs.fetchone()
    conn.close()
    return country

# 보여줄 여행 정보의 카테고리
def GetCateList(platform, id):
    # 유저가 선택한 여행 정보의 나라를 가져온다
    # ex) ('스페인',)
    country = GetCountry(platform, id)

    # 그 나라가 가진 정보 카테고리를 가져온다
    sql = "select distinct d_type from info_trip_tb where country = (%s);"

    conn = make_connection()
    curs = conn.cursor()
    curs.execute(sql, country)

    rows = curs.fetchall()

    # 튜플의 각 원소만 리스트로 바꿈
    # ['먹거리', '음식점', '여행지']
    category = list(map(lambda x: x[0], rows))

    # 버튼 이름 설정
    idx = category.index('먹거리')
    idx2 = category.index('음식점')
    if (idx != -1):
        category[idx] = '전통 음식'
    if (idx2 != -1):
        category[idx2] = '추천 음식점'

    conn.close()
    return category

def GetCityList(platform, id):
    country = GetCountry(platform, id)

    # 여행 정보 테이블에 있는 도시 리스트를 가져온다
    sql = "select distinct city from info_trip_tb where country = (%s) and city != ''"

    conn = make_connection()
    curs = conn.cursor()
    curs.execute(sql, country)
    rows = curs.fetchall()

    # ['바르셀로나', '마드리드', '세비야', '그라나다']
    cities = list(map(lambda x: x[0], rows))

    conn.close()
    return cities

def GetInfoList(platform, id, d_type):
    # 유저가 선택한 여행 정보의 나라를 가져온다
    country = GetCountry(platform, id)

    # 나라와 입력받은 type에 맞는 행을 가져온다
    sql = "select d_title from info_trip_tb where country = (%s) and d_type = (%s)"

    conn = make_connection()
    curs = conn.cursor()

    curs.execute(sql, (country[0], d_type))
    rows = curs.fetchall()

    # ['빠에야(Paella)', '하몬', '가스파초', '추로스', '핀쵸스 (Pinchos)']
    food = list(map(lambda x: x[0], rows))
    conn.close()
    return food

def GetInfoDetail(platform, id, type, title):
    country = GetCountry(platform, id)

    conn = make_connection()
    curs = conn.cursor()

    # 설명과 이미지 url을 가져온다
    sql = "select d_source, d_url from info_trip_tb where country = (%s) and d_type = (%s) and d_title = (%s)"
    curs.execute(sql, (country[0], type, title))
    info_detail = curs.fetchone()
    conn.close()
    return info_detail

def GetInfoCity(platform, id, d_type):
    city = GetCity(platform, id)

    # 도시에 해당하는 정보만 가져온다
    sql = "select d_title from info_trip_tb where city = (%s) and d_type = (%s)"
    conn = make_connection()
    curs = conn.cursor()
    curs.execute(sql, (city, d_type))
    rows = curs.fetchall()

    info_city = list(map(lambda x: x[0], rows))

    conn.close()
    return info_city

if __name__ == '__main__':

    print(search_data("telegram","*","740140183")[0])