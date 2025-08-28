import sqlite3, os, csv, time
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()  # .env 파일의 환경변수 로드

DATABASE = os.getenv('DATABASE')
DB_PATH = os.path.join('/','Users','seSAC','src','nowinseoul','nowinseoul','instance',DATABASE)  # 데이터베이스 파일 경로


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
def insert_data(table_name, result_list): # fetch api data
    columns = {'detail_raw': 'id, realtime_pop, realtime_pop_dttm',
               'density_raw':'id, fcst_dt, level',
               'weather_raw':'id, fcst_dt, fcst_temp, rain_chance',
               'bike_station_info':'id, station_id, station_name_ko'}[table_name]

    place_holder = {'detail_raw': ':id, :AREA_CONGEST_LVL, :PPLTN_TIME',
                    'density_raw':':id, :FCST_TIME, :FCST_CONGEST_LVL',
                    'weather_raw':':id, :fcstDate, :TMP, :POP',
                    'bike_station_info':':id, :SBIKE_SPOT_ID, :SBIKE_SPOT_NM'}[table_name]

    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute(f'DELETE FROM {table_name}')
    print(f'{result_list[0]=}')
    print(f'{table_name=} {columns=} {place_holder=}')
    # cur.executemany : 여러 개의 SQL 명령을 하나씩 반복 실행하는 것
    cur.executemany(f"""INSERT INTO {table_name} ({columns}) 
                                    VALUES ({place_holder})""", result_list)
                                    # VALUES ({place_holder}, {datetime.now().strftime('%Y%m%d%H%M%S')})""", result_list)
    
    conn.commit()
    conn.close()

# 데이터 조회 함수
def get_data(attr, table_name):
    if table_name not in table_list():
        raise KeyError('존재하지 않는 테이블명입니다.')
    
    conn = connect_db()
    cur = conn.cursor()
    
    #  여기에 구현할것
    cur.execute(f'SELECT {attr} FROM {table_name}')
    result_list = [dict(i) for i in cur.fetchall()]
    
    conn.commit()
    conn.close()
    
    return result_list

def get_info_by_id(table_name, attraction_id):
    conn = connect_db()
    cur = conn.cursor()

    #  여기에 구현할것
    cur.execute(f"SELECT * FROM {table_name} WHERE id = ?", (attraction_id,))
    attr_value = [dict(i) for i in cur.fetchall()]  # 사용자 한명만
    
    conn.commit()
    conn.close()
    
    return attr_value

def get_info_for_map():
    conn = connect_db()
    cur = conn.cursor()

    #  여기에 구현할것
    # [{'id': 'POI001', 'name': 'Gangnam MICE Special Tourist Zone', 'crowd': 'Crowded', 'beauty': '241', 'food': '25', 'drama': '18', 'movie': '14', 'lat': '37.512693', 'lng': '127.0624'},]
    cur.execute(f"""SELECT att.id
                         , att.name_en AS name
                         , dtl.realtime_pop AS crowd
                         , att.beauty
                         , att.food
                         , att.drama
                         , att.movie
                         , att.lat
                         , att.lng
                      FROM attraction att
                      JOIN detail_cache dtl ON att.id = dtl.id
                 """)
    attr_value = [dict(i) for i in cur.fetchall()]  # 사용자 한명만
    
    conn.commit()
    conn.close()

    return attr_value

def get_images(tags:list):
    conn = connect_db()
    cur = conn.cursor()
    
    if tags:
        cur.execute(f'SELECT id, name_en AS name FROM attraction ORDER BY {'+'.join(tags)} DESC LIMIT 6')
    else:
        cur.execute(f'SELECT id, name_en AS name FROM attraction ORDER BY food+beauty+drama+movie DESC LIMIT 6')
    
    result_list = [dict(i) for i in cur.fetchall()]
    
    conn.commit()
    conn.close()    

    return result_list

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

def update_xy(id_nx_ny_list):
    conn = connect_db()
    cur = conn.cursor()

    cur.executemany("""UPDATE attraction
                          SET nx = :nx,
                              ny = :ny
                        WHERE id = :id
                    """, id_nx_ny_list) # 여러 개의 SQL 명령을 하나씩 반복 실행하는 것

    conn.commit()
    conn.close()

def update_traffic(id_traffic_list):
    conn = connect_db()
    cur = conn.cursor()

    cur.executemany("""UPDATE detail_raw
                          SET realtime_road = :realtime_road,
                              realtime_road_dttm = :realtime_road_dttm
                        WHERE id = :id
                    """, id_traffic_list) # 여러 개의 SQL 명령을 하나씩 반복 실행하는 것

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

# 현재 호출 안함    
def download_csv(table_name):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(f'SELECT * FROM {table_name}')
    rows = cur.fetchall()

    # 컬럼명 가져오기
    fieldnames = rows[0].keys()

    with open(f'./data/{table_name}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # 헤더 작성
        for row in rows:
            writer.writerow(dict(row))  # Row 객체를 딕셔너리로 변환해 씀
    print(f'./data/{table_name}.csv 파일로 내보내기 완료')

    conn.close()

# csv -> table
def import_bike_station_info():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute('DELETE FROM bike_station_info')

    csv_path = os.path.join('data', 'bike_station_info.csv')
    with open(csv_path, newline='', encoding='utf-8') as f: # newline=''은 파일의 줄바꿈 문자 변환을 하지 않고 "있는 그대로" 처리
        reader = csv.DictReader(f.readlines())
        rows = list(reader)

        insert_sql = f"""INSERT INTO bike_station_info (id,station_id,station_name_ko,station_name_en) 
                                                VALUES (:id,:station_id,:station_name_ko,:station_name_en)"""
    
        cur.executemany(insert_sql, rows)

    conn.commit()
    conn.close()
    print(f"[CSV] bike_station_info.csv → bike_station_info 업로드 완료.")

if __name__ == "__main__":
    print(get_info_by_id('weather_cache', 'POI007'))
    # print(get_attraction_by_id('desc_ko' , 'POI007'))