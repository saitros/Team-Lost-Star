import pymysql
import pandas as pd
from config import host_name,username,password,database_name


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
            id_list.remove((str(id),))
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


if __name__ == '__main__':
    #print(get_single_value(964322422,'sex'))
    #get_userinfo(964322422)
    #print(search_data("telegram"))
    #print(search_data("telegram", "open_cnt", "964322422", 1))
    print(search_user("telegram","964322422"))