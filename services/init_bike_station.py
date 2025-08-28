### 실시간 도시데이터를 활용하여 bike_station_info 테이블 초기화 완성

# pip install googletrans
# https://pypi.org/project/googletrans/
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from concurrent.futures import ThreadPoolExecutor
import os, utils
from dotenv import load_dotenv
from models import db
from itertools import chain


load_dotenv()  # .env 파일의 환경변수 로드
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    print(f'.env 파일에서 API_KEY를 입력하세요')

## 1. 실시간 도시 데이터에서 도시ID - 대여소ID 매핑
def mapping_id(attraction_dict):
        # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    try:
        url = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/citydata/1/50/{attraction_dict.get('name_ko')}'
        # print(f'fetching url :{url}')

        city_data = utils.fetch(url).get('CITYDATA')
        area_code = city_data.get('AREA_CD') # POI008

        bike_state = city_data.get('SBIKE_STTS') # sbike stts list
        if not bike_state:
            print(f'No Bike Station near {city_data.get('AREA_NM')} : {area_code}')
            return []  # [] 반환해 나중에 필터링 예정

        return [
            {'id': area_code, 'SBIKE_SPOT_ID': station.get('SBIKE_SPOT_ID'), 'SBIKE_SPOT_NM':station.get('SBIKE_SPOT_NM')}
            for station in bike_state
        ]
    except Exception as e:
        print(f'error message : {e}')
        print(f"error url : {url}")
        return []  # [] 반환해 나중에 필터링 예정

## 1. 실시간 도시 데이터에서 도시ID - 대여소ID 매핑    
# bike_station_info 생성 함수
def concurrent_processing(fn, load:list): # 전역변수보다 인수로 전달하는 것이 안전
    with ThreadPoolExecutor() as executor:
        # https://docs.python.org/ko/3/library/itertools.html#itertools.chain.from_iterable
        results = list(chain.from_iterable(executor.map(fn, load)))

        return results

if __name__ == "__main__":
    pass
    ## 1. 실시간 도시 데이터에서 도시ID - 대여소ID 매핑
    db.insert_data('bike_station_info',concurrent_processing(mapping_id,db.get_data('name_ko', 'attraction')))

    ## 2. csv로 Export
    # db.download_csv('bike_station_info')
    
    ## 3. import csv
    db.import_bike_station_info()