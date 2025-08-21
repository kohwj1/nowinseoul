### 실시간 도시데이터를 활용하여 bike_station_info 테이블 초기화 완성


# pip install googletrans
# https://pypi.org/project/googletrans/
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests, os
from dotenv import load_dotenv
from time import time
import sys
sys.path.append('/Users/seSAC/src/nowinseoul/nowinseoul')
from models import db
from itertools import chain


load_dotenv()  # .env 파일의 환경변수 로드
API_KEY = os.getenv('API_KEY')

def fetch(url):
    # https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
    # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    try:
        response = requests.get(url)
        # response.raise_for_status()  # HTTP 상태 코드 오류 체크
    except requests.exceptions.ConnectionError:
        print("네트워크 연결 문제 발생")
    except requests.exceptions.Timeout:
        print("요청이 타임아웃되었습니다.")
    except requests.exceptions.TooManyRedirects:
        print("너무 많은 리디렉션 발생")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 오류 발생: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"기타 오류 발생: {err}")
    # else:
    #     print("요청 성공:", response.status_code)
        
    return response.json()

## 2. 실시간 도시 데이터에서 도시ID - 대여소ID 매핑
def mapping_id(attraction_name_ko):
        # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    try:
        url = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/citydata/1/50/{attraction_name_ko}'
        print(f'fetching url :{url}')

        city_data = fetch(url).get('CITYDATA')
        area_code = city_data.get('AREA_CD') # POI008

        bike_state = city_data.get('SBIKE_STTS') # sbike stts list
        if not bike_state:
            print(f'No Bike Station near {city_data.get('AREA_NM')} : {area_code}')
            return []  # [] 반환해 나중에 필터링 예정

        return [
            {'station_id': station.get('SBIKE_SPOT_ID'), 'id': area_code}
            for station in bike_state
        ]
    except Exception as e:
        print(f'error message : {e}')
        print(f"error url : {url}")
        return []  # [] 반환해 나중에 필터링 예정
    
# bike_station_info 생성 함수
def concurrent_processing(fn, load:list): # 전역변수보다 인수로 전달하는 것이 안전
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fn, load))
        flattened = list(chain.from_iterable(results))

        return flattened

## 1. 서울특별시 운영중인 공공자전거 대여소 정보 api를 bike_station_info 에 입력
def insert_bike_station_api():
    db.delete_table('bike_station_info')
    for n in range(5): # 4001 부터는 없음
    # for n in [3]: # 4001 부터는 없음
        # 한번에 1000개 까지 get(조회)
        url = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/tbCycleStationInfo/{n*1000 +1}/{(n+1)*1000}'
        print(url)
        data = fetch(url).get('stationInfo',False)
        if not data:
            break

        # db에 적재
        db.insert_bike_station_info(data.get('row'))
        print(f"{n*1000 +1} ~ {(n+1)*1000} 범위의 대여소 정보 적재 완료")

if __name__ == "__main__":
    pass
    ## (추후 삭제) 1. 서울특별시 운영중인 공공자전거 대여소 정보 api를 bike_station_info 에 입력
    # insert_bike_station_api()

    ## 2. 실시간 도시 데이터에서 도시ID - 대여소ID 매핑
    # db.update_id(concurrent_processing(mapping_id,db.get_attraction_name()))
    ## 3. csv로 Export
    # db.download_csv()
    ## 4. import csv
    # db.import_bike_station_info()