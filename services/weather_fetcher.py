### 실시간 날씨 예측
# 원천부서 이원재(02-2133-4272)로 문의요청 2025.04.11 13:55 댓글
# 9월 중순에 api update 예정. 만약, 그 이후에도 느리면 기상청 api 허브에서 행정동/위치 고정시켜서 가져와야함.
# 날씨만 따로 api제공할 계획 없음(기상청 관할이기 때문)


import sys
sys.path.append('/Users/seSAC/src/nowinseoul/nowinseoul')
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os, utils
from dotenv import load_dotenv
from datetime import datetime
from models import db
from itertools import chain


load_dotenv()  # .env 파일의 환경변수 로드
API_KEY = os.getenv('API_KEY')

## 실시간 도시 데이터에서 날씨 예측정보 fetch
def mapping_id(attraction_name_ko):
        # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    try:
        url = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/citydata/1/50/{attraction_name_ko}'
        print(f'fetching url :{url}')

        city_data = utils.fetch(url).get('CITYDATA')
        # city_data 전체를 그대로 전달하면 데이터 크기가 커지고 전송 및 처리 비용이 증가합니다.
        # 필요한 컬럼만 추출해서 전달하면 DB 쓰기 시점에 불필요한 데이터 파싱/처리가 줄어듭니다.

        fcst_weather = city_data.get('WEATHER_STTS')[0].get('FCST24HOURS') # 날씨예측 목록

        # **item : item dict 언패킹
        return [  {'id': city_data.get('AREA_CD'), # POI033 서울역
                    **item} for item in fcst_weather]

        # map + lambda 조합은 lambda 함수 호출 오버헤드가 있으며,
        # 특히, 람다 내에서 x |= {...} 같은 복합 할당 연산은 추가 작업을 수행하기 때문에 더 무거울 수 있습니다
        # return list(map(lambda x: x |= {'id': city_data.get('AREA_CD')},fcst_weather))

  
    except Exception as e:
        print(f'error message : {e}')
        print(f"error url : {url}")
        return []  # [] 반환해 나중에 When flattened, it disappears.
    
# FCST24HOURS 날씨 예측 목록 생성 함수
def concurrent_processing(fn, load:list): # 전역변수보다 인수로 전달하는 것이 안전
    with ThreadPoolExecutor() as executor:
        # https://docs.python.org/ko/3/library/itertools.html#itertools.chain.from_iterable
        results = list(chain.from_iterable(executor.map(fn, load)))

        return results
@utils.execution_time
def fetch_weather():
    result_list = concurrent_processing(mapping_id,db.get_attraction_name_ko()) # 여기까지 21.3초 걸렸음
    db.insert_data('weather_raw', result_list)
    print(f'weather_raw {len(result_list)}개 데이터 insert 완료 {datetime.now().strftime('%Y%m%d%H%M%S')}')
    # weather_raw 1920(24*80)개 데이터 insert 완료 20250824224242
    # fetch_weather 함수 실행 시간: 30.6초
    return result_list

if __name__ == "__main__":
    fetch_weather()