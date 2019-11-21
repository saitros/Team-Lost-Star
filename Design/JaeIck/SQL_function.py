import pymysql

conn = pymysql.connect(host = 'localhost', user = 'root', password = 'root', db = 'loststar', charset = 'utf8')
curs = conn.cursor()

def is_user_new(platform,user_id):
    if (search_data(platform,"id",user_id,1)) is False:
        # print("신규유저")
        return True
    else: 
        # print("기존유저")
        return False

# id 데이터 삽입
def insert_id_data(platform, data):
    
    sql = "insert into {platform}_user_tb(id,dialog_state,user_state,open_cnt,show_count) values (%s, %s,%s,%s,%s)".format(platform=platform)
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
        
    try:
        if len(rows) != 0:
            # print("정보있음")
            # print(rows)
            return rows
    except:
        # print("정보없음")
        return False

# 데이터 업데이트
def update_data(platform, column, data, id):
    sql = "update {platform}_user_tb set {column} = %s where id = %s".format(platform=platform, column=column)
    curs.execute(sql, (data, id))
    conn.commit()

#카카오톡에서만 유저검색
def my_kakao_user_search(id):
    mydata = search_data("kakaotalk",'*',id)
    print(mydata[0][7])
    print(mydata[0][8])
    print(mydata[0][9])
    
    sql = "select * from kakaotalk_user_tb where city = '{}' and (start_date >= {} or end_date <= {}) and id != '{}'".format(mydata[0][7],mydata[0][8],mydata[0][9],id)
    curs.execute(sql)
    rows = curs.fetchall()
    #없으면 False 를 반환
    if len(rows) == 0:
        return False
    else:
        return rows

# 동행 유저 검색
def search_user(platform, id):
    # 카카오톡 아이디 최대 열람 횟수, 테이블 갯수
    # MAX_OPEN_CNT = 3
    MAX_TABLE_CNT = 3

    # 플랫폼 리스트
    platform_list = ["telegram", "facebook", "kakaotalk"]
    
    # open_cnt 조회, 최대 열람 횟수를 넘어가면 -1 리턴후 함수 종료
    # cnt = search_data(platform, "open_cnt", id, 1)
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
            id_list.remove((id,))
            id_list = tuple(id_list)
        
        # 아이디 리스트에서 하나씩 뽑으면서 조회
        for item in id_list:
            info = search_data(other_platform, "sex, age,country, city,profile_image ,start_date, end_date, appeal_tag,kakao_id", item)
            info = list(info[0])
            trip_users.append(info)

            # if other_platform == "facebook":
            #     info = search_data(other_platform, "id, profile_image,sex, age,country, city, start_date, end_date, appeal_tag", item)
            #     info = list(info[0])
            #     info[0] = "f" + info[0]
            #     trip_users.append(info)
            # elif other_platform == "kakaotalk":
            #     info = search_data(other_platform, "id,profile_image, sex, age,country, city, start_date, end_date, appeal_tag", item)
            #     info = list(info[0])
            #     info[0] = "k" + info[0]
            #     trip_users.append(info)
            # elif other_platform == "telegram":
            #     info = search_data(other_platform, "id,profile_image, sex, age,country, city, start_date, end_date, appeal_tag", item)
            #     info = list(info[0])
            #     info[0] = "t" + info[0]
            #     trip_users.append(info)
    
    return trip_users



if __name__ == "__main__":
    # insert_data("facebook", (24, "마", "남자", 29, "http://", "마", "파리", "2019-11-17", "2019-11-19", "#테스트, #테스트2", "state?", "기존", 1))
    # insert_id_data("kakaotalk",(5,"New","New",0))
    
    # insert_id_data("telegram", (2, "lee"))
    su = search_user("kakaotalk","f65ae1aabf7764aa7b18af50c25fe526eee49ee90c55433401616f448e28aa5e6d")
    # su = search_data('kakaotalk','show_count','4d3d473a6eade2e478f23568ce920972b5a5ea726b128403e972865097f23c2c48',1)
    print(len(su))
    
    
    # update_data("kakaotalk", "user_state", 'Existing', user_id)
    # is_user_new('kakaotalk',"f65ae1a1616f448e28aa5e6d")
    # users = search_user("facebook", 24)
    # print(users)

    conn.close()