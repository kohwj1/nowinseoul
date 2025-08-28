### 실시간 주변 도로 종합 현황
# 

# 서울시 api는 비동기 요청시 (aiohttp) xml로 답변이 옴 (llm은 aiohttp에 헤더가 없아서 그런거라는데..)
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from concurrent.futures import ThreadPoolExecutor
import os, utils
from dotenv import load_dotenv
from datetime import datetime
from models import db
from itertools import chain


load_dotenv()  # .env 파일의 환경변수 로드
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    print(f'.env 파일에서 API_KEY를 입력하세요')

## 실시간 도시 데이터에서 날씨 예측정보 fetch
def mapping_id(attraction_dict):
        # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    try:
        url = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/citydata/1/50/{attraction_dict.get('name_ko')}'
        # print(f'fetching url :{url}')

        city_data = utils.fetch(url).get('CITYDATA')
        # city_data 전체를 그대로 전달하면 데이터 크기가 커지고 전송 및 처리 비용이 증가합니다.
        # 필요한 컬럼만 추출해서 전달하면 DB 쓰기 시점에 불필요한 데이터 파싱/처리가 줄어듭니다.

        near_road = city_data.get('ROAD_TRAFFIC_STTS',{}).get('AVG_ROAD_DATA',{}) # 실시간 주변도로 평균 상황

        # **item : item dict 언패킹
        return [{'id': city_data.get('AREA_CD'), # POI033 서울역
                 'realtime_road' : near_road.get('ROAD_TRAFFIC_IDX',{}),
                 'realtime_road_dttm' : near_road.get('ROAD_TRAFFIC_TIME',{})}]

        # map + lambda 조합은 lambda 함수 호출 오버헤드가 있으며,
        # 특히, 람다 내에서 x |= {...} 같은 복합 할당 연산은 추가 작업을 수행하기 때문에 더 무거울 수 있습니다
        # return list(map(lambda x: x |= {'id': city_data.get('AREA_CD')},fcst_weather))

  
    except Exception as e:
        print(f'error message : {e}')
        print(f"error url : {url}")
        print(f'resolution message : {attraction_dict.get('name_ko')}의 날씨 정보를 제공하지 않습니다')
        return []  # [] 반환해 나중에 When flattened, it disappears.
    
# 주변도로 생성 함수
def concurrent_processing(fn, load:list): # 전역변수보다 인수로 전달하는 것이 안전
    with ThreadPoolExecutor() as executor:
        # https://docs.python.org/ko/3/library/itertools.html#itertools.chain.from_iterable
        results = list(chain.from_iterable(executor.map(fn, load)))

        return results
@utils.execution_time
def fetch_traffic():
    result_list = concurrent_processing(mapping_id,db.get_data('name_ko', 'attraction')) # 여기까지 21.3초 걸렸음
    print(f'{result_list[0]=}')
    db.update_traffic(result_list)
    print(f'detail_raw {len(result_list)}개 실시간 주변 도로 데이터 insert 완료 {datetime.now().strftime('%Y.%m.%d %H:%M:%S')}')
    # weather_raw 1920(24*80)개 데이터 insert 완료 20250824224242
    # fetch_traffic 함수 실행 시간: 30.6초
    return result_list

if __name__ == "__main__":
    fetch_traffic()