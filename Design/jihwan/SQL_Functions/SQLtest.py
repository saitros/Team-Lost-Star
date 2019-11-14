import pymysql

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

# 데이터 검색
def search_data(platform, column = "*", id = "NULL"):
    sql = "select {column} from {platform}_user_tb".format(column=column, platform=platform)

    if (id != "NULL"):
        sql = sql + " where id = {id}".format(id=id)
    curs.execute(sql)
    rows = curs.fetchall()
    print(rows)

# 데이터 업데이트
def update_data(platform, column, data, id):
    sql = "update {platform}_user_tb set {column} = %s where id = %s".format(platform=platform, column=column)
    curs.execute(sql, (data, id))
    conn.commit()

def search_user(city):
    # 텔레그램 테이블과 카카오톡 테이블 조인을 통해 카카오톡 유저 id 알아냄
    sql = """select distinct k.id from telegram_user_tb as t
            join kakaotalk_user_tb as k
            on k.city = %s
            where t.city = k.city;"""

    curs.execute(sql, city)
    rows = curs.fetchall()
    print(rows)


if __name__ == "__main__":
    conn = pymysql.connect(host = 'localhost', user = 'root', password = 'hwanSQL123!', db = 'tripdb_01', charset = 'utf8')
    curs = conn.cursor()
    
    # insert_data("kakaotalk", (14, "H", "남자", 23, "http://", "KH", "파리", "2019-11-05", "2019-11-12", "#테스트, #테스트2", "state?", "기존", 1))
    
    
    # insert_id_data("telegram", (2, "lee"))
    # search_data("telegram")
    # update_data("telegram", "user_state", 'new_member', 2)

    search_user("파리")

    conn.close()