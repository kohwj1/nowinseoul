### 실시간 날씨 예측
# 원천부서 이원재(02-2133-4272)로 문의요청 2025.04.11 13:55 댓글
# 9월 중순에 api update 예정. 만약, 그 이후에도 느리면 기상청 api 허브에서 행정동/위치 고정시켜서 가져와야함.
# 날씨만 따로 api제공할 계획 없음(기상청 관할이기 때문)
#
# 기상청 apihub에서 가져옴 https://apihub.kma.go.kr/ -> 예특보탭 -> 단기예보 


import sys
sys.path.append('/Users/seSAC/src/nowinseoul/nowinseoul')
import asyncio,aiohttp
from concurrent.futures import ThreadPoolExecutor
import os, utils
from dotenv import load_dotenv
from datetime import datetime
from models import db
from itertools import chain,repeat


load_dotenv()  # .env 파일의 환경변수 로드
API_KEY = os.getenv('API_KEY')

def parking_info(api_data, station_id_dict):
    try:
        station_id = api_data.get("stationId") # 'ST-10'
        if station_id in station_id_dict:
            return[{'SBIKE_SPOT_NM' : station_id_dict.get(station_id), # station_name_ko(대여소 영어 이름)
                     'SBIKE_PARKING_CNT' : api_data.get('parkingBikeTotCnt'),
                     'SBIKE_X' : api_data.get('stationLatitude'),
                     'SBIKE_Y' : api_data.get('stationLongitude')
            }]
    
    except:
        print(f'Exception in parking_info: {e}')
        ## https://docs.python.org/ko/3.13/library/stdtypes.html#dict
        # 키워드 인자가 제공되면, 키워드 인자와 해당 값이 위치 인자로부터 만들어진 딕셔너리에 추가됩니다.
        # 추가되는 키가 이미 존재하면, 키워드 인자에서 온 값이 위치 인자에게서 온 값을 대체합니다.
        # 즉, 관광지와 관련없는 대여소라면'0'으로 (dict(results)의 키 중복제거 속성 활용하여) 제거
    return []

async def fetch_and_filter(session, url, station_id_dict):
        obj = await utils.async_fetch(session, url)
        fetch_data = obj.get('rentBikeStatus', {}).get('row', [])

        # 스레드풀을 사용하여 각 지역의 데이터를 병렬 처리
        with ThreadPoolExecutor() as executor:
            # 각 지역의 데이터를 병렬로 처리
            processed_results = list(executor.map(parking_info, fetch_data, repeat(station_id_dict)))

            fltten_results = list(chain.from_iterable(processed_results))
            return fltten_results


@utils.async_execution_time
async def get_info(attraction_id, my_locale): # POI033 서울역
    # 리스트 안에 원시값(숫자, 문자열 등 불변 객체)만 있다면 사실상 독립적인 리스트가 되고, 내부 요소 변경도 영향을 안 준다.
    # 여기서는 영향을 받아야하므로 얕은카피(.copy())하지 않음
    
    station_id_dict = { s.get('station_id'): s.get('station_name_'+my_locale)
                               for s in db.get_info_by_id('bike_station_info',attraction_id) }
    # [{'ST-10':'108. Seogyo-dong Intersection'},]
    result_data = []

    # 한번에 1000개 까지 get(조회) for n in [2]: # 4001 부터는 없음
    urls = [f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/bikeList/{n*500 +1}/{(n+1)*500}' for n in range(20)]
    # async with aiohttp.ClientSession(headers={"Accept": "application/json"}) as session:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_filter(session, url, station_id_dict) for url in urls]
        results = await asyncio.gather(*tasks)
        # 각 fetch마다 이미 필터된 목록이 오므로 평탄화 : chain.from_iterable는 1차원만 낮춰줌
        # 모든 결과를 하나의 리스트로 평면화
        return list(chain.from_iterable(results))
    
    
if __name__ == "__main__":
    result_bike_station_list = asyncio.run(get_info("POI033",'en')) # POI033 서울역
    print(f'처리 완료: {len(result_bike_station_list)}개 대여소 데이터')
    print(f'완료 시간: {datetime.now().strftime("%Y.%m.%d %H:%M:%S")}')
    if result_bike_station_list:
        print(f'{result_bike_station_list[0]=}')
    else:
        print('Nothing near Attraction')