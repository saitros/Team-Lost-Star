import pymysql

conn = pymysql.connect(host = 'localhost', user = 'root', password = 'hwanSQL123!', db = 'tripdb_01', charset = 'utf8')
curs = conn.cursor()

# id 데이터 삽입
def insert_id_data(platform, data):
    sql = "insert into {platform}_user_tb(id, user_id) values (%s, %s)".format(platform=platform)
    curs.execute(sql, data)
    conn.commit()


# 전체 데이터 삽입
def insert_data(platform, data):
    sql = """insert into {platform}_user_tb(id, user_id, sex, age, profile_image, kakao_id, 
            city, start_date, end_date, appeal_tag, dialog_state, user_state, open_cnt) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(platform=platform)  
    curs.execute(sql, data)
    conn.commit()


# 데이터 삭제
def delete_data(platform, column = "*", id = "NULL"):
    sql = "delete {column} from {platform}_user_tb".format(column=column, platform=platform)

    if (id != "NULL"):
        sql = sql + " where id = {id}".format(id=id)
    curs.execute(sql)
    conn.commit()

# 데이터 검색 기본값으로 fetchall
def search_data(platform, column = "*", id = "NULL", opt = 0):
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

    return rows

# 데이터 업데이트
def update_data(platform, column, data, id):
    sql = "update {platform}_user_tb set {column} = %s where id = %s".format(platform=platform, column=column)
    curs.execute(sql, (data, id))
    conn.commit()


# 동행 유저 검색
def search_user(platform, id):
    # 카카오톡 아이디 최대 열람 횟수, 테이블 갯수
    MAX_OPEN_CNT = 5
    MAX_TABLE_CNT = 3

    # 플랫폼 리스트
    platform_list = ["telegram", "facebook", "kakaotalk"]
    
    # open_cnt 조회, 최대 열람 횟수를 넘어가면 -1 리턴후 함수 종료
    cnt = search_data(platform, "open_cnt", id, 1)
    if (cnt[0] > MAX_OPEN_CNT):
        return -1
    
    # 2차원 tuple 형식으로 반환됨
    # print(city) --> (('파리',),)
    city = search_data(platform, "city", id)
    start_date = search_data(platform, "start_date", id, 1)
    end_date = search_data(platform, "end_date", id, 1)
    
    # 동행 유저 리스트 초기화
    trip_users = []

    # 모든 테이블 개별적으로 조인
    i = 0
    while(i < MAX_TABLE_CNT):
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
            id_list.remove((str(id),))
            id_list = tuple(id_list)
        
        # 아이디 리스트에서 하나씩 뽑으면서 조회
        for item in id_list:
            info = search_data(other_platform, "user_id, sex, age, city, start_date, end_date", item)
            trip_users.append(info[0])
    
    return trip_users


# 여행 정보를 보여줄 나라 리스트
def GetCountryList(platform, id):
    sql = "select distinct country from info_trip_tb;"
    curs.execute(sql)

    # 튜플안에 튜플의 형태
    # ex) (('스페인',), ('필리핀',), ('포르투갈',), ('프랑스',), ('스위스',))
    rows = curs.fetchall()

    # 튜플의 각 원소만 리스트로 바꿈
    # ['스페인', '필리핀', '포르투갈', '프랑스', '스위스']
    country = list(map(lambda x: x[0], rows))

    return country

# 유저가 선택한 나라를 가져오는 함수
def GetCountry(platform, id):
    sql = "select info_country from {platform}_user_tb where id = (%s)".format(platform=platform)
    curs.execute(sql, id)
    country = curs.fetchone()

    return country

def GetCity(platform, id):
    sql = "select info_city from {platform}_user_tb where id = (%s)".format(platform=platform)
    curs.execute(sql, id)
    country = curs.fetchone()

    return country

# 보여줄 여행 정보의 카테고리
def GetCateList(platform, id):
    # 유저가 선택한 여행 정보의 나라를 가져온다
    # ex) ('스페인',)
    country = GetCountry(platform, id)

    # 그 나라가 가진 정보 카테고리를 가져온다
    sql = "select distinct d_type from info_trip_tb where country = (%s);"
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
       
    return category

def GetCityList(platform, id):
    country = GetCountry(platform, id)

    # 여행 정보 테이블에 있는 도시 리스트를 가져온다
    sql = "select distinct city from info_trip_tb where country = (%s) and city != ''"
    curs.execute(sql, country)
    rows = curs.fetchall()

    # ['바르셀로나', '마드리드', '세비야', '그라나다']
    cities = list(map(lambda x: x[0], rows))

    return cities

def GetInfoList(platform, id, d_type):
    # 유저가 선택한 여행 정보의 나라를 가져온다
    country = GetCountry(platform, id)

    # 나라와 입력받은 type에 맞는 행을 가져온다
    sql = "select d_title from info_trip_tb where country = (%s) and d_type = (%s)"
    curs.execute(sql, (country[0], d_type))
    rows = curs.fetchall()

    # ['빠에야(Paella)', '하몬', '가스파초', '추로스', '핀쵸스 (Pinchos)']
    food = list(map(lambda x: x[0], rows))

    return food

def GetInfoDetail(platform, id, type, title):
    country = GetCountry(platform, id)

    # 설명과 이미지 url을 가져온다
    sql = "select d_source, d_url from info_trip_tb where country = (%s) and d_type = (%s) and d_title = (%s)"
    curs.execute(sql, (country[0], type, title))
    info_detail = curs.fetchone()

    return info_detail

def GetInfoCity(platform, id, d_type):
    city = GetCity(platform, id)

    # 도시에 해당하는 정보만 가져온다
    sql = "select d_title from info_trip_tb where city = (%s) and d_type = (%s)"
    curs.execute(sql, (city, d_type))
    rows = curs.fetchall()

    info_city = list(map(lambda x: x[0], rows))

    return info_city


if __name__ == "__main__":
    # insert_data("telegram", ("24", "마", "남자", 29, "http://", "마", "파리", "2019-11-17", "2019-11-19", "#테스트, #테스트2", "state?", "기존", 1))
    
    
    # insert_id_data("telegram", ("2", "lee"))
    # search_data("telegram")
    # update_data("telegram", "user_state", 'new_member', "2")

    # users = search_user("facebook", '24')
    # print(users)

    # counties = GetCountryList("telegram", '24')
    # category = GetCateList("telegram", '24')
    print(GetInfoList("telegram", '24', "여행지"))
    print(GetInfoDetail("telegram", '24', '여행지', '람블라스 거리'))
    print(GetCityList("telegram", '24'))
    print(GetInfoCity("telegram", '24', "여행지"))

    # update_data("telegram", "info_city", "바르셀로나", '24')

    conn.close()