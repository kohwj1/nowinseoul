 # 앱 초기 설치 및 셋업 함수 모음

from models.init_db import *
from services.init_bike_station import *
from services.init_weather import *


def init_app_fetch_data():
    ## models.init_db
    # 1. 데이터베이스 초기화
    if os.path.exists(DB_PATH):
        os.mkdir('instance')
    init_db()

    # 2. CSV 파일 업로드
    import_attraction()

    # 3. update nx, ny
    asyncio.run(main())


    ## services.init_bike_station
    ## 1. 실시간 도시 데이터에서 도시ID - 대여소ID 매핑
    db.insert_data('bike_station_info',concurrent_processing(mapping_id,db.get_data('name_ko', 'attraction')))
    print('bike_station_info')

def init_app_before_translation():
    ## 2. csv로 Export
    db.download_csv('bike_station_info')
    print("bike_station_info.csv export 완료")
    print("구글 시트에서 영문번역하되 '1문' ~ '6문' -> 'Gate 1' ~ 'Gate 6'으로 바꾸기")
    print("구글 시트에서 영문번역하되 '381. 장충체육관' -> '381. Jangchung Arena'으로 바꾸기")
    print("구글 시트에서 영문번역하되 '2003. 사육신공원앞' -> '2003. In front of Sayuksin Park'으로 바꾸기")

def init_app_after_translation():    
    ## 3. import csv
    db.import_bike_station_info()
    print("bike_station_info.csv import 완료")
    print("초기화 완료")

if __name__ == "__main__":
    ## 기존 대여소 영문번역명 사용
    init_app_fetch_data()

    ## 대여소 한글명 번역전
    # init_app_before_translation()

    ## 아래 함수는 bike_station_info.csv 번역 후에 실행하세요
    ## 혹은 
    init_app_after_translation()