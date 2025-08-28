 # 앱 초기 설치 및 셋업 함수 모음

from models import init_db, db
from services import density_fetcher, etl, init_bike_station,init_weather,realtime_pop_fetcher,realtime_traffic_fetcher,weather_fetcher
import os, asyncio

def init_app_fetch_data():
    ## models.init_db
    # 1. 데이터베이스 초기화
    if not os.path.exists('instance'):
        os.mkdir('instance')
        print('instance folder를 추가했습니다.')

    init_db.init_db()

    # 2. attraction.csv CSV 파일 업로드
    init_db.import_attraction()

    # 3. update nx, ny
    ## 기상청 api 데이터에서 임의 위·경도 → 인근 동네예보 격자 번호 변환 (lat,lng -> nx,ny)
    asyncio.run(init_weather.main())


    ## services.init_bike_station
    if not os.path.exists('.env'):
        print('.env 파일을 추가해야합니다.')
        return 

    ## 1. 실시간 도시 데이터에서 도시ID - 대여소ID 매핑
    db.insert_data('bike_station_info',init_bike_station.concurrent_processing(init_bike_station.mapping_id,db.get_data('name_ko', 'attraction')))
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

if __name__ == "__main__":
    ## nowinseoul.db 생성
    # 테이블 생성

    ## attraction 테이블
    # import (attraction.csv, main_feature.csv), (nx, ny) 컬럼정보 추가
    init_app_fetch_data()

    ## bike_station_info
    # 대여소 한글명 번역전
    # init_app_before_translation()

    ## 아래 함수는 bike_station_info.csv 번역 후에 실행하세요
    ## 혹은 기존 대여소 영문번역명 사용
    init_app_after_translation()

    ## density_fetcher
    density_fetcher.fetch_density()

    ## realtime_pop_fetcher
    realtime_pop_fetcher.fetch_realtime_pop()

    ## realtime_traffic_fetcher
    realtime_traffic_fetcher.fetch_traffic()

    ## weather_fetcher
    asyncio.run(weather_fetcher.make_weather_dataset())

    ## etl
    for d in ['detail', 'weather','density']:
        etl.raw_to_cache_etl(d)

    
    print("초기화 완료")