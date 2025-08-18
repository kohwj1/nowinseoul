import sqlite3
import csv
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일의 환경변수 로드

DATABASE = os.getenv('DATABASE')
DB_PATH = os.path.join('instance',DATABASE)  # 데이터베이스 파일 경로
CSV_FOLDER = 'data'     # CSV 파일이 있는 폴더 경로

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 예시 테이블 생성
# -- 관광지 기본 정보
    cur.execute('''
CREATE TABLE IF NOT EXISTS attraction
(
  id          TEXT    NOT NULL,
  name        TEXT    NOT NULL,
  description TEXT    NULL    ,
  lat         DECIMAL NOT NULL,
  lon         DECIMAL NOT NULL,
  food        BOOLEAN NULL    ,
  beauty      BOOLEAN NULL    ,
  drama       BOOLEAN NULL    ,
  movie       BOOLEAN NULL    ,
  thumbnail   TEXT    NULL    ,
  insert_dttm TEXT    NOT NULL, -- 입력일시
  PRIMARY KEY (id)
)''')

# -- 인구밀도 예측 캐싱 테이블
    cur.execute('''
CREATE TABLE IF NOT EXISTS density_cache
(
  id          TEXT NOT NULL, -- 장소 고유식별자
  fcst_dt     TEXT NOT NULL, -- 예측 일시
  level       TEXT NULL    , -- 인구밀도 수준
  insert_dttm TEXT NOT NULL, -- 입력일시
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES detail_cache (id)
)''')

# -- 인구밀도 예측 원본 테이블
    cur.execute('''
CREATE TABLE IF NOT EXISTS density_raw
(
  id          TEXT NOT NULL, -- 장소 고유식별자
  fcst_dt     TEXT NOT NULL, -- 예측 일시
  level       TEXT NULL    , -- 인구밀도 수준
  insert_dttm TEXT NOT NULL, -- 입력일시
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES density_cache (id)
)''')

# -- 각 지역 상세 캐싱 데이터
    cur.execute('''
CREATE TABLE IF NOT EXISTS detail_cache
(
  id            TEXT NOT NULL, -- 장소 고유식별자
  realtime_pop  TEXT NULL    , -- 실시간 인구밀도 수준
  realtime_road TEXT NULL    , -- 실시간 도로상황 (상세 페이지 진입 시에만 업뎃치기?)
  insert_dttm   TEXT NOT NULL, -- 입력일시
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES attraction (id)
)''')

# -- 각 지역 상세 원본 데이터
    cur.execute('''
CREATE TABLE IF NOT EXISTS detail_raw
(
  id            TEXT NOT NULL, -- 장소 고유식별자
  realtime_pop  TEXT NULL    , -- 실시간 인구밀도 수준
  realtime_road TEXT NULL    , -- 실시간 도로상황 (상세 페이지 진입 시에만 업뎃치기?)
  insert_dttm   TEXT NOT NULL, -- 입력일시
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES detail_cache (id)
)''')

# -- 날씨 예측 캐싱 테이블
    cur.execute('''
CREATE TABLE IF NOT EXISTS weather_cache
(
  id          TEXT    NOT NULL, -- 장소 고유식별자
  fcst_dt     TEXT    NOT NULL, -- 예측 일시
  fcst_temp   INTEGER NULL    , -- 예측 온도
  rain_chance INTEGER NULL    , -- 예측 강수확률
  insert_dttm TEXT    NOT NULL, -- 입력일시
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES detail_cache (id)
)''')

# -- 날씨 예측 원본 테이블
    cur.execute('''
CREATE TABLE IF NOT EXISTS weather_raw
(
  id          TEXT    NOT NULL, -- 장소 고유식별자
  fcst_dt     TEXT    NOT NULL, -- 예측 일시
  fcst_temp   INTEGER NULL    , -- 예측 온도
  rain_chance INTEGER NULL    , -- 예측 강수확률
  insert_dttm TEXT    NOT NULL, -- 입력일시
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES weather_cache (id)
)''')

# -- 따릉이 대여소 기본 정보
    cur.execute('''
CREATE TABLE bike_station_info
(
  station_id      TEXT NULL    , -- 대여소 id
  station_no      TEXT NOT NULL, -- 대여소 no
  station_lat     REAL NULL    , -- 대여소 위도
  station_lon     REAL NULL    , -- 대여소 경도
  station_name_ko TEXT NOT NULL, -- 한국어 대여소명
  station_name_en TEXT NULL    , -- 영어 대여소명
  PRIMARY KEY (station_no)
)''')

    cur.execute('''
CREATE INDEX idx_station_location
  ON bike_station_info (station_lat ASC, station_lon ASC)
 ''')

    print("[DB] 테이블 생성 완료.")
    conn.commit()
    conn.close()

def import_bike_station_info():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('DELETE FROM bike_station_info')

    csv_path = os.path.join(CSV_FOLDER, 'bike_station_info.csv')
    with open(csv_path, newline='', encoding='utf-8') as f: # newline=''은 파일의 줄바꿈 문자 변환을 하지 않고 "있는 그대로" 처리
        reader = csv.DictReader(f.readlines())
        rows = list(reader)

        insert_sql = f"""INSERT INTO bike_station_info (station_no,station_lat,station_lon,station_name_ko,station_name_en) 
                                                VALUES (:station_no,:station_lat,:station_lon,:station_name_ko,:station_name_en)"""
        cur.executemany(insert_sql, rows)

    conn.commit()
    conn.close()
    print(f"[CSV] bike_station_info.csv → bike_station_info 업로드 완료.")

def import_attraction(table, csv_filename):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    csv_path = os.path.join(CSV_FOLDER, csv_filename)
    with open(csv_path, newline='', encoding='utf-8') as f: # newline=''은 파일의 줄바꿈 문자 변환을 하지 않고 "있는 그대로" 처리
        reader = csv.DictReader(f.readlines())
        print(list(reader))

        placeholders = ','.join(['?']*len(columns))
        insert_sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"

        for row in reader:
            cur.execute(insert_sql, row)

    conn.commit()
    conn.close()
    print(f"[CSV] {csv_filename} → {table} 업로드 완료.")

if __name__ == '__main__':
    # 1. 데이터베이스 초기화
    # if os.path.exists(DB_PATH):
    #     os.remove(DB_PATH)
    # init_db()

    # 2. CSV 파일 업로드 (예시)
    import_bike_station_info()
    # import_csv('products', 'products.csv')
    # import_csv('orders', 'orders.csv')
