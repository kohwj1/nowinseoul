import sqlite3, os
from dotenv import load_dotenv

load_dotenv()  # .env 파일의 환경변수 로드

DATABASE = os.getenv('DATABASE')
DB_PATH = os.path.join('instance',DATABASE)  # 데이터베이스 파일 경로
tables = []

# db에 접속하는 함수
def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

# 테이블 목록
def table_list():
    conn =  connect_db()
    cur = conn.cursor()
    
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    global tables
    tables = [table[0] for table in cur.fetchall()]
    print('tables',tables)
    
    conn.commit()
    conn.close()

# 테이블 목록 전역변수에 업데이트
table_list()
    
# 데이터 삽입 함수
def insert_user(name, age):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    
    conn.commit()
    conn.close()

def insert_bike_station_info(bike_station_info):
    conn = connect_db()
    cur = conn.cursor()

    cur.executemany("""INSERT INTO bike_station_info (station_id, station_no, station_lat, station_lon, station_name_ko, station_name_en)
                                              VALUES (:RENT_ID, :RENT_NO, :STA_LAT, :STA_LONG, :RENT_ID_NM, :RENT_ID_NM_EN)""", bike_station_info) # 여러 개의 SQL 명령을 하나씩 반복 실행하는 것
    '''
    station_id      TEXT : RENT_ID       -- 대여소 id
    station_no      TEXT : RENT_NO       -- 대여소 no
    station_lat     REAL : STA_LAT       -- 대여소 위도
    station_lon     REAL : STA_LONG      -- 대여소 경도
    station_name_ko TEXT : RENT_ID_NM    -- 한국어 대여소명
    station_name_en TEXT : RENT_ID_NM_EN -- 영어 대여소명
    '''

    conn.commit()
    conn.close()
    
# 데이터 조회 함수
def get_null_station_id():
    conn = connect_db()
    cur = conn.cursor()
    
    #  여기에 구현할것
    cur.execute('SELECT station_no FROM bike_station_info WHERE station_id is NULL')
    rows = [ i[0] for i in cur.fetchall()]  # 모든거 다
    
    conn.commit()
    conn.close()
    
    return rows  # 가져온 사용자 반환

def get_user_by_name(name):
    conn = connect_db()
    cur = conn.cursor()
    
    #  여기에 구현할것
    cur.execute('SELECT * FROM users WHERE name = ?', (name,))
    user = cur.fetchone()  # 사용자 한명만
    
    conn.commit()
    conn.close()
    
    return user

# 데이터 수정 함수
def update_user_age(name, new_age):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute('UPDATE users SET age=? WHERE name=?', (new_age, name))
    
    conn.commit()
    conn.close()
    
def delete_table(table_name):
    if table_name not in tables:
        print(tables, table_name)
        raise ValueError("Invalid table name")

    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute(f"DELETE FROM  {table_name}") 
    # SQLite 공식적으로는 TRUNCATE 명령을 지원하지 않으므로, 전체 데이터 삭제는 DELETE FROM으로 수행
    # ? 플레이스홀더는 **값(value)**에 대해서만 쓸 수 있고, 테이블 이름 같은 SQL 식별자(identifier)는 플레이스홀더로 바인딩할 수 없습니다.
    
    conn.commit()
    conn.close()
    
def delete_user_by_age(age):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM users WHERE age=?', (age,))
    
    conn.commit()
    conn.close()
    
def delete_user_by_id(id):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM users WHERE id=?', (id,))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # print(get_null_station_id())

