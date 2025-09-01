import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import sqlite3, csv, os, db
from dotenv import load_dotenv
from datetime import datetime
from flask import current_app

load_dotenv()  # .env 파일의 환경변수 로드

DATABASE = os.getenv('DATABASE')
if not DATABASE:
    print(f'.env 파일에서 DATABASE를 입력하세요')
DB_PATH = os.path.join('instance',DATABASE)  # 데이터베이스 파일 경로
CSV_FOLDER = 'data'     # CSV 파일이 있는 폴더 경로

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

### 예시 테이블 생성
# -- 관광지 기본 정보
    cur.execute('''
CREATE TABLE IF NOT EXISTS attraction
(
  id          TEXT    NOT NULL,  -- 관광지 고유식별자
  name_ko     TEXT    NOT NULL,  -- 관광지 한국어명
  name_en     TEXT    NULL    ,  -- 관광지 영어명
  name_ja     TEXT    NULL    ,  -- 관광지 일본어명
  lat         REAL    NOT NULL,  -- 관광지 위도
  lng         REAL    NOT NULL,  -- 관광지 경도
  nx          INTEGER NULL    ,  -- 예보지점의 X 좌표값 = 동네예보 격자 번호(동서방향)
  ny          INTEGER NULL    ,  -- 예보지점의 Y 좌표값 = 동네예보 격자 번호(동서방향)
  food        BOOLEAN NULL    ,
  beauty      BOOLEAN NULL    ,
  drama       BOOLEAN NULL    ,
  movie       BOOLEAN NULL    ,
  desc_ko     TEXT    NULL    ,  -- 관광지 한국어 설명
  desc_en     TEXT    NULL    ,  -- 관광지 영어 설명
  desc_ja     TEXT    NULL    ,  -- 관광지 일본어 설명 / 국제 표준 코드 - ja 
  insert_dttm TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),  -- 입력일시
  PRIMARY KEY (id)
)''')

# -- 따릉이 대여소 기본 정보
    cur.execute('''
CREATE TABLE IF NOT EXISTS bike_station_info
(
  id              TEXT NOT NULL, -- 관광지 고유식별자
  station_id      TEXT NOT NULL, -- 대여소 id
  station_name_ko TEXT NOT NULL, -- 대여소 한국어명
  station_name_en TEXT NULL    , -- 대여소 영어명
  station_name_ja TEXT NULL    , -- 대여소 일본어명
  insert_dttm     TEXT NOT NULL DEFAULT (datetime('now', 'localtime')), -- 입력일시
  PRIMARY KEY (id, station_id),
  FOREIGN KEY (id) REFERENCES attraction_info (id)
)''')

#     cur.execute('''
# CREATE INDEX idx_station_location
#   ON bike_station_info (station_lat ASC, station_lon ASC)
#  ''')

# -- 인구밀도 예측 캐싱 테이블
    cur.execute('''
CREATE TABLE IF NOT EXISTS density_cache
(
  id          TEXT NOT NULL,   -- 관광지 고유식별자
  fcst_dt     TEXT NOT NULL,   -- 예측 일시
  level       TEXT NULL    ,   -- 인구밀도 수준
  insert_dttm TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),   -- 입력일시
  PRIMARY KEY (id, fcst_dt),
  FOREIGN KEY (id, fcst_dt) REFERENCES density_raw (id, fcst_dt)
)''')

# -- 인구밀도 예측 원본 테이블
    cur.execute('''
CREATE TABLE IF NOT EXISTS density_raw
(
  id          TEXT NOT NULL,   -- 관광지 고유식별자
  fcst_dt     TEXT NOT NULL,   -- 예측 일시
  level       TEXT NULL    ,   -- 인구밀도 수준
  insert_dttm TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),   -- 입력일시
  PRIMARY KEY (id, fcst_dt),
  FOREIGN KEY (id) REFERENCES attraction_info (id)
)''')

# -- 각 지역 상세 캐싱 데이터 from 실시간 인구데이터 (영문)
    cur.execute('''
CREATE TABLE IF NOT EXISTS detail_cache
(
  id                 TEXT NOT NULL,  -- 관광지 고유식별자
  realtime_pop       TEXT NULL    ,  -- 실시간 인구밀도 수준( 5분마다 갱신 )
  realtime_pop_dttm  TEXT NULL    ,  -- 실시간 인구 데이터 업데이트 시간
  realtime_road      TEXT NULL    ,  -- 실시간 주변 도로 (평균)혼잡도( 5분마다 갱신 )
  realtime_road_dttm TEXT NULL    ,  -- 실시간 주변 도로 (평균)혼잡도 데이터 업데이트 시간
  realtime_road_msg  TEXT NULL    ,  -- 실시간 주변 도로 (평균) 혼잡도 관련 메세지
  insert_dttm        TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),  -- 입력일시
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES detail_raw (id)
)''')

# -- 각 지역 상세 원본 데이터 from 실시간 인구데이터 (영문)
    cur.execute('''
CREATE TABLE IF NOT EXISTS detail_raw
(
  id                 TEXT NOT NULL,  -- 관광지 고유식별자
  realtime_pop       TEXT NULL    ,  -- 실시간 인구밀도 수준 ( 5분마다 갱신 )
  realtime_pop_dttm  TEXT NULL    ,  -- 실시간 인구 데이터 업데이트 시간
  realtime_road      TEXT NULL    ,  -- 실시간 주변 도로 (평균) 혼잡도( 5분마다 갱신 )
  realtime_road_dttm TEXT NULL    ,  -- 실시간 주변 도로 (평균) 혼잡도 데이터 업데이트 시간
  realtime_road_msg  TEXT NULL    ,  -- 실시간 주변 도로 (평균) 혼잡도 관련 메세지
  insert_dttm        TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),  -- 입력일시
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES attraction_info (id)
)''')

# -- 날씨 예측 캐싱 테이블
    cur.execute('''
CREATE TABLE IF NOT EXISTS weather_cache
(
  id          TEXT    NOT NULL,   -- 관광지 고유식별자
  fcst_dt     TEXT    NOT NULL,   -- 예측 일시
  fcst_temp   INTEGER NULL    ,   -- 예측 온도
  rain_chance INTEGER NULL    ,   -- 예측 강수확률
  insert_dttm TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),   -- 입력일시
  PRIMARY KEY (id, fcst_dt),
  FOREIGN KEY (id, fcst_dt) REFERENCES weather_raw (id, fcst_dt)
)''')

# -- 날씨 예측 원본 테이블
    cur.execute('''
CREATE TABLE IF NOT EXISTS weather_raw
(
  id          TEXT    NOT NULL,   -- 관광지 고유식별자
  fcst_dt     TEXT    NOT NULL,   -- 예측 일시
  fcst_temp   INTEGER NULL    ,   -- 예측 온도
  rain_chance INTEGER NULL    ,   -- 예측 강수확률
  insert_dttm TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),   -- 입력일시
  PRIMARY KEY (id, fcst_dt),
  FOREIGN KEY (id) REFERENCES attraction_info (id)
)''')

    print("[DB] 테이블 생성 완료.")
    conn.commit()
    conn.close()

def import_attraction():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('DELETE FROM attraction')

    # id, name, desc_en, lat, lng 데이터 import
    csv_path = os.path.join(CSV_FOLDER, 'attraction.csv')
    with open(csv_path, newline='', encoding='utf-8') as f: # newline=''은 파일의 줄바꿈 문자 변환을 하지 않고 "있는 그대로" 처리
        reader = csv.DictReader(f.readlines())
        rows = list(reader)

        insert_sql = f"""INSERT INTO attraction (id,name_ko,name_en,name_ja,lat,lng,desc_ko,desc_en,desc_ja) 
                                         VALUES (:id,:name_ko,:name_en,:name_ja,:lat,:lng,:desc_ko,:desc_en,:desc_ja)"""
        cur.executemany(insert_sql, rows)

    print(f"[CSV] attraction.csv → attraction 업로드 완료.")

    # id에 따른 food, beauty, drama, movie 데이터 import
    csv_path = os.path.join(CSV_FOLDER, 'main_feature.csv')
    with open(csv_path, newline='', encoding='utf-8') as f: # newline=''은 파일의 줄바꿈 문자 변환을 하지 않고 "있는 그대로" 처리
        reader = csv.DictReader(f.readlines())
        rows = list(reader)

        cur.executemany("""UPDATE attraction
                              SET beauty = :beauty,
                                  drama = :drama,
                                  food = :food,
                                  movie = :movie
                            WHERE 1=1
                              AND id = :id
                        """, rows) # 여러 개의 SQL 명령을 하나씩 반복 실행하는 것

    conn.commit()
    conn.close()
    print(f"[CSV] main_feature.csv → main_feature 업데이트 완료.")

    # Tag 정보는 csv에서 업데이트 하므로 csv import 후에 refresh
    current_app.config['tag_cases'] = db.generate_tag_cases()
    print(f"[tag_cases] current_app.config[]._tag_cases 업데이트 완료.")


if __name__ == '__main__':
    ## models.init_db
    # 1. 데이터베이스 초기화
    if not os.path.exists('instance'):
        os.mkdir('instance')
    init_db()

    # 2. CSV 파일 업로드
    import_attraction()

    # 3. update nx, ny
    asyncio.run(main())
