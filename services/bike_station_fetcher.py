### 따릉이 대여소 현황
# 4번 Fetch -> 데이터 전처리는 

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from concurrent.futures import ThreadPoolExecutor
import os, utils
from dotenv import load_dotenv
from models import db
from itertools import repeat

load_dotenv()  # .env 파일의 환경변수 로드
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    print(f'.env 파일에서 API_KEY를 입력하세요')

def parking_info(api_data, station_id_dict):
    station_id = api_data.get("stationId") # 'ST-10'
    if station_id in station_id_dict:
        value = {'SBIKE_SPOT_NM' : station_id_dict.get(station_id), # station_name_en(대여소 영어 이름)
                 'SBIKE_PARKING_CNT' : api_data.get('parkingBikeTotCnt'),
                 'SBIKE_X' : api_data.get('stationLatitude'),
                 'SBIKE_Y' : api_data.get('stationLongitude')
        }
    
        return station_id, value
    else:
        ## https://docs.python.org/ko/3.13/library/stdtypes.html#dict
        # 키워드 인자가 제공되면, 키워드 인자와 해당 값이 위치 인자로부터 만들어진 딕셔너리에 추가됩니다.
        # 추가되는 키가 이미 존재하면, 키워드 인자에서 온 값이 위치 인자에게서 온 값을 대체합니다.
        # 즉, 관광지와 관련없는 대여소라면'0'으로 (dict(results)의 키 중복제거 속성 활용하여) 제거
        return '0', None 

def concurrent_processing(fn, load:list, station_id_dict): # 전역변수보다 인수로 전달하는 것이 안전
    with ThreadPoolExecutor() as executor:
        results = dict(executor.map(fn, load, repeat(station_id_dict)))
        # if '0' in results.keys():
        results.pop('0','관광지와 무관한 대여소 제거')

    return results

def get_info(attraction_id): # POI033 서울역
    # 리스트 안에 원시값(숫자, 문자열 등 불변 객체)만 있다면 사실상 독립적인 리스트가 되고, 내부 요소 변경도 영향을 안 준다.
    # 여기서는 영향을 받아야하므로 얕은카피(.copy())하지 않음
    # 
    station_id_dict = {s.get('station_id'): s.get('station_name_en') for s in db.get_info_by_id('bike_station_info',attraction_id)}
    # [{'ST-10':'108. Seogyo-dong Intersection'},]
    result_data = []

    for n in range(5): # 4001 부터는 없음
    # for n in [2]: # 4001 부터는 없음
        # 한번에 1000개 까지 get(조회)
        url = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/bikeList/{n*1000 +1}/{(n+1)*1000}'
        data = utils.fetch(url).get('rentBikeStatus',False)

        # 데이터가 없는 page가 되면 loop 중단
        if not data:
            break
        
        # 1000개 api 데이터 중 적재할 데이터만 추출 : 스레드풀
        bike_station_info = concurrent_processing(parking_info, data.get('row'),station_id_dict)
        result_data.extend(list(bike_station_info.values()))
    
    return result_data

if __name__ == "__main__":
    result_bike_station_list = get_info("POI033") # POI033 서울역
    print(f'{result_bike_station_list=}')