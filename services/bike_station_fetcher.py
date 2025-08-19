### 따릉이 대여소 현황

import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests, os
from dotenv import load_dotenv
from time import time
import sys
sys.path.append('/Users/seSAC/src/nowinseoul/nowinseoul')
from models import db
from itertools import repeat

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

def parking_info(api_data, station_id_dict):
    station_id = api_data.get("stationId") 
    if station_id in station_id_dict:
        value = {'SBIKE_SPOT_NM' : station_id_dict.get(station_id),
                 'SBIKE_PARKING_CNT' : api_data.get('parkingBikeTotCnt'),
                 'SBIKE_X' : api_data.get('stationLatitude'),
                 'SBIKE_Y' : api_data.get('stationLongitude')
                }
    
        return station_id, value
    else:
        return '0', None

def concurrent_processing(fn, load:list, station_id_dict): # 전역변수보다 인수로 전달하는 것이 안전
    with ThreadPoolExecutor() as executor:
        results = dict(executor.map(fn, load, repeat(station_id_dict)))
        if '0' in results.keys():
            results.pop('0')

    return results

def get_info(attraction_id): # POI033 서울역
    # station_id만 필요한 station_no
    # 리스트 안에 원시값(숫자, 문자열 등 불변 객체)만 있다면 사실상 독립적인 리스트가 되고, 내부 요소 변경도 영향을 안 준다.
    # 여기서는 영향을 받아야하므로 얕은카피(.copy())하지 않음
    station_info_list = db.get_station_info(attraction_id)
    # [{'id': 'POI007', 'station_id': 'ST-10', 'station_lat': 37.55274582, 'station_lon': 126.9186173, 'station_name_en': '108. Seogyo-dong Intersection'},]
    result_data = []

    for n in range(5): # 4001 부터는 없음
    # for n in [2]: # 4001 부터는 없음
        # 한번에 1000개 까지 get(조회)
        url = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/bikeList/{n*1000 +1}/{(n+1)*1000}'
        data = fetch(url).get('rentBikeStatus',False)

        # 데이터가 없는 page가 되면 loop 중단
        if not data:
            break
        
        # api 데이터 중 적재할 데이터만 추출
        station_id_dict = {s.get('station_id'): s.get('station_name_en') for s in station_info_list}
        bike_station_info = concurrent_processing(parking_info, data.get('row'),station_id_dict)
        result_data += list(bike_station_info.values())
    
    return result_data

if __name__ == "__main__":
    get_info("POI033") # POI033 서울역