### 실시간 인구 예측
# 예측 AI모델을 통해, 향후 12시간의 실시간 인구를 예측
# - 실시간 단위의 날씨, 도로소통, 대중교통 등의 데이터를 활용하여 예측의 타당성 제고
# - Sequence to Sequence 아키텍처를 통해, 과거 12시간 데이터를 기반으로 향후 12시간 실시간 인구 예측
# - 5분 단위로 산출되는 실시간 인구를 기반으로 5분 단위 트렌드를 예측에 반영
# ※ 축제 등으로 인한 급격한 인구수 변화는 반영하지 못할 수 있음
# ※ 예측 인구수는 실제 인구수와 다를 수 있음
#
# An index that calculated the 4 stages of congestion into
# crowded, slightly crowded, moderate, and comfortable (ref.Seoul Real-Time Population Data API manual_eng.pdf)

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

## 실시간 인구밀도 데이터에서 도시ID - 인구밀도 매핑
def mapping_id(attraction_name_ko):
        # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    try:
        url = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/citydata_ppltn_eng/1/50/{attraction_name_ko}'
        # print(f'fetching url :{url}')

        city_data = utils.fetch(url).get('SeoulRtd.citydata_ppltn')[0]
        # city_data 전체를 그대로 전달하면 데이터 크기가 커지고 전송 및 처리 비용이 증가합니다.
        # 필요한 컬럼 2개만 추출해서 전달하면 DB 쓰기 시점에 불필요한 데이터 파싱/처리가 줄어듭니다.

        fcst_ppltn = city_data.get('FCST_PPLTN') # 인구밀도예측 목록

        # **item : item dict 언패킹
        return [{'id': city_data.get('AREA_CD'), # POI033 서울역
                 **item} for item in fcst_ppltn]

  
    except Exception as e:
        print(f'error message : {e}')
        print(f"error url : {url}")
        return []  # # [] 반환해 나중에 When flattened, it disappears.
    
# id - FCST_PPLTN 예측 목록 생성 함수
def concurrent_processing(fn, load:list): # 전역변수보다 인수로 전달하는 것이 안전
    with ThreadPoolExecutor() as executor:
        # https://docs.python.org/ko/3/library/itertools.html#itertools.chain.from_iterable
        results = list(chain.from_iterable(executor.map(fn, load)))

        return results

def fetch_density():
    result_list = concurrent_processing(mapping_id,db.get_data('name_ko', 'attraction'))
    db.insert_data('density_raw', result_list)
    print(f'density_raw {len(result_list)}개 데이터 insert 완료 {datetime.now().strftime('%Y%m%d%H%M%S')}')
    return result_list

if __name__ == "__main__":
    fetch_density()