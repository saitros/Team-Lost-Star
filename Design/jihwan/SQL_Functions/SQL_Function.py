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
            id_list.remove((id,))
            id_list = tuple(id_list)
        
        # 아이디 리스트에서 하나씩 뽑으면서 조회
        for item in id_list:
            info = search_data(other_platform, "user_id, sex, age, city, start_date, end_date", item)
            trip_users.append(info[0])
    
    return trip_users


if __name__ == "__main__":
    # insert_data("facebook", (24, "마", "남자", 29, "http://", "마", "파리", "2019-11-17", "2019-11-19", "#테스트, #테스트2", "state?", "기존", 1))
    
    
    # insert_id_data("telegram", (2, "lee"))
    # search_data("telegram")
    # update_data("telegram", "user_state", 'new_member', 2)

    users = search_user("facebook", 24)
    print(users)

    conn.close()