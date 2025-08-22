import sqlite3, os, csv, time
from dotenv import load_dotenv
from datetime import datetime
import time # 타임 데코레이터

load_dotenv()  # .env 파일의 환경변수 로드

DATABASE = os.getenv('DATABASE')
DB_PATH = os.path.join('instance',DATABASE)  # 데이터베이스 파일 경로


def execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 함수 실행 시간: {round(end_time - start_time/60,1)}분")
        return result
    return wrapper

# db에 접속하는 함수
def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # 각각의 행이 tuple 이 아닌 dict로 반환된다
    return conn

# 테이블 목록
def table_list():
    conn =  connect_db()
    cur = conn.cursor()
    
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cur.fetchall()]
    
    conn.commit()
    conn.close()

    return tables
    
# 데이터 삽입 함수
def insert_congestion_lvl(result_list): # fetch api data
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM detail_raw')
    # [{'id': 'POI003', 'realtime_pop': 'Comfortable'},]
    cur.executemany(f"""INSERT INTO detail_raw (id, realtime_pop, insert_dttm) 
                                    VALUES (:id, :realtime_pop, {datetime.now().strftime('%Y%m%d%H%M%S')})""", result_list)
    
    conn.commit()
    conn.close()

def insert_bike_station_info(bike_station_info):
    conn = connect_db()
    cur = conn.cursor()

    cur.executemany(f"""INSERT INTO bike_station_info (station_id, station_no, station_lat, station_lon, station_name_ko, insert_dttm)
                                              VALUES (:RENT_ID, :RENT_NO, :STA_LAT, :STA_LONG, :RENT_ID_NM,{datetime.now().strftime('%Y%m%d%H%M%S')})""", bike_station_info) # 여러 개의 SQL 명령을 하나씩 반복 실행하는 것
    '''-- 따릉이 대여소 기본 정보
      id              TEXT NOT NULL, -- 장소 고유식별자
      station_id      TEXT NULL    , -- 대여소 id
      station_no      TEXT NOT NULL, -- 대여소 no
      station_lat     REAL NULL    , -- 대여소 위도
      station_lon     REAL NULL    , -- 대여소 경도
      station_name_ko TEXT NOT NULL, -- 한국어 대여소명
      station_name_en TEXT NULL    , -- 영어 대여소명
      insert_dttm     TEXT NOT NULL, -- 입력일시
      PRIMARY KEY (station_name_ko),
      FOREIGN KEY (id) REFERENCES detail_cache (id)
    '''

    conn.commit()
    conn.close()
    
# 데이터 조회 함수
def get_station_info(attraction_id):
    conn = connect_db()
    cur = conn.cursor()
    
    #  여기에 구현할것
    cur.execute('SELECT id, station_id, station_name_en FROM bike_station_info WHERE id = ?',(attraction_id,))
    rows = cur.fetchall()
    
    conn.commit()
    conn.close()
    
    return [dict(r) for r in rows]  # 가져온 사용자 반환

def get_attraction_name():
    conn = connect_db()
    cur = conn.cursor()
    
    #  여기에 구현할것
    cur.execute('SELECT name FROM attraction')
    name_list = cur.fetchall()
    
    conn.commit()
    conn.close()
    
    return [dict(i)['name'] for i in name_list]

def get_attraction_name_by_id(attraction_id):
    conn = connect_db()
    cur = conn.cursor()
    
    #  여기에 구현할것
    cur.execute('SELECT name FROM attraction WHERE id = ?', (attraction_id,))
    attr_name = cur.fetchone()  # 사용자 한명만
    
    conn.commit()
    conn.close()
    
    return attr_name

def get_desc(attraction_id):
    conn = connect_db()
    cur = conn.cursor()
    
    #  여기에 구현할것
    cur.execute('SELECT description FROM attraction WHERE id = ?', (attraction_id,))
    attr_desc = cur.fetchone()[0] 
    
    conn.commit()
    conn.close()
    
    return attr_desc

# 데이터 수정 함수
def update_id(station_id_mapping_list):
    conn = connect_db()
    cur = conn.cursor()

    cur.executemany("""UPDATE bike_station_info
                          SET id = :id
                        WHERE station_id = :station_id
                    """, station_id_mapping_list) # 여러 개의 SQL 명령을 하나씩 반복 실행하는 것
    '''
    id              TEXT NOT NULL,       -- 장소 고유식별자
    station_id      TEXT : RENT_ID       -- 대여소 id
    station_no      TEXT : RENT_NO       -- 대여소 no
    station_lat     REAL : STA_LAT       -- 대여소 위도
    station_lon     REAL : STA_LONG      -- 대여소 경도
    station_name_ko TEXT : RENT_ID_NM    -- 한국어 대여소명
    station_name_en TEXT : RENT_ID_NM_EN -- 영어 대여소명
    '''

    conn.commit()
    conn.close()

# 데이터 삭제 함수    
def delete_table(table_name):
    if table_name not in table_list():
        print(table_list(), table_name)
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

def download_csv():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute('SELECT * FROM bike_station_info')
    rows = cur.fetchall()

    # 컬럼명 가져오기
    fieldnames = rows[0].keys()

    with open('./data/bike_station_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # 헤더 작성
        for row in rows:
            writer.writerow(dict(row))  # Row 객체를 딕셔너리로 변환해 씀
    print('/data/bike_station_info.csv 파일로 내보내기 완료')

    conn.close()

def import_bike_station_info():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute('DELETE FROM bike_station_info')

    csv_path = os.path.join('data', 'bike_station_info.csv')
    with open(csv_path, newline='', encoding='utf-8') as f: # newline=''은 파일의 줄바꿈 문자 변환을 하지 않고 "있는 그대로" 처리
        reader = csv.DictReader(f.readlines())
        rows = list(reader)

        insert_sql = f"""INSERT INTO bike_station_info (id,station_id,station_no,station_lat,station_lon,station_name_ko,station_name_en,insert_dttm) 
                                                VALUES (:id,:station_id,:station_no,:station_lat,:station_lon,:station_name_ko,:station_name_en,{datetime.now().strftime('%Y%m%d%H%M%S')})"""
    
        cur.executemany(insert_sql, rows)

    conn.commit()
    conn.close()
    print(f"[CSV] bike_station_info.csv → bike_station_info 업로드 완료.")

if __name__ == "__main__":
    # print(get_null_station_id())
    # print(get_attraction_name())
    # print(get_station_info('POI007'))
    print(get_desc('POI007'))