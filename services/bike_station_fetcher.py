### 따릉이 대여소 현황

import sys
sys.path.append('/Users/seSAC/src/nowinseoul/nowinseoul')
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os, utils
from dotenv import load_dotenv
from models import db
from itertools import repeat

load_dotenv()  # .env 파일의 환경변수 로드
API_KEY = os.getenv('API_KEY')


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
    # [{'id': 'POI007', 'station_id': 'ST-10','station_name_en': '108. Seogyo-dong Intersection'},]
    result_data = []

    for n in range(5): # 4001 부터는 없음
    # for n in [2]: # 4001 부터는 없음
        # 한번에 1000개 까지 get(조회)
        url = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/bikeList/{n*1000 +1}/{(n+1)*1000}'
        data = utils.fetch(url).get('rentBikeStatus',False)

        # 데이터가 없는 page가 되면 loop 중단
        if not data:
            break
        
        # api 데이터 중 적재할 데이터만 추출
        station_id_dict = {s.get('station_id'): s.get('station_name_en') for s in station_info_list}
        bike_station_info = concurrent_processing(parking_info, data.get('row'),station_id_dict)
        result_data += list(bike_station_info.values())
    
    return result_data

if __name__ == "__main__":
    print(get_info("POI033")) # POI033 서울역