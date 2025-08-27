### 실시간 인구밀도 현황
# 통신데이터를 바탕으로 전체 인구를 추정하여 사용자에게 제공되기까지 15분 소요
# - 예) 10시 10분~10시 15분에 집계된 데이터는 전체 인구 추정 과정을 거쳐 10시 30분에 사용자에게 제공
# 
# 단위시간(5분) 동안 여러 기지국을 방문할 경우 중복 집계
# 예를 들어, 어떤 사람이 다음 그림처럼 14시 12분에 A기지국 영역에서 B기지국 영역으로 이동하였을 때,
# 14시 10분 ~ 14시 15분까지 5분의 단위 시간동안 A기지국(14:10~14:12)과 B기지국(14:12~14:15)에서 모두 집계되므로,
# 동일한 사람이지만 2명으로 중복 집계
#
# An index that calculated the 4 stages of congestion into
# crowded, slightly crowded, moderate, and comfortable (ref.Seoul Real-Time Population Data API manual_eng.pdf)

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from concurrent.futures import ThreadPoolExecutor
import os, utils
from dotenv import load_dotenv
from datetime import datetime
from models import db

load_dotenv()  # .env 파일의 환경변수 로드
API_KEY = os.getenv('API_KEY')

## 실시간 인구밀도 데이터에서 도시ID - 인구밀도 매핑
def mapping_id(attraction_dict):
        # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    try:
        url = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/citydata_ppltn_eng/1/50/{attraction_dict.get('name_ko')}'
        print(f'fetching url :{url}')

        city_data = utils.fetch(url).get('SeoulRtd.citydata_ppltn')[0]
        # city_data 전체를 그대로 전달하면 데이터 크기가 커지고 전송 및 처리 비용이 증가합니다.
        # 21개 속성중에서 필요한 컬럼 2개만 추출해서 전달하면 DB 쓰기 시점에 불필요한 데이터 파싱/처리가 줄어듭니다.

        # return (
        #     ('id', city_data.get('AREA_CD')), # POI008
        #     ('AREA_CONGEST_LVL', city_data.get('AREA_CONGEST_LVL')), # 인구밀도혼잡도 레벨
        #     ('PPLTN_TIME' , city_data.get('PPLTN_TIME')), # 실시간 인구 데이터 업데이트 시간
        # )
        return (
            ('id', city_data.get('AREA_CD')), # POI008
            ('AREA_CONGEST_LVL', city_data.get('AREA_CONGEST_LVL')), # 인구밀도혼잡도 레벨
            ('PPLTN_TIME' , city_data.get('PPLTN_TIME')), # 실시간 인구 데이터 업데이트 시간
        )
  
    except Exception as e:
        print(f'error message : {e}')
        print(f"error url : {url}")
        return '0'  # '0' 반환해 나중에 set.discard('0')으로 제거
    
# id - area_congestion_lvl 목록 생성 함수
def concurrent_processing(fn, load:list): # 전역변수보다 인수로 전달하는 것이 안전
    with ThreadPoolExecutor() as executor:
        # '0'(error 값) 중복 제거
        results_set = set(executor.map(fn, load))
        # '0'(error 값) 제거
        results_set.discard('0')
        # [dict,dict,dict] 형태로 변환
        results = list(map(dict, results_set))

        return results
@utils.execution_time
def fetch_realtime_pop():
    result_list = concurrent_processing(mapping_id,db.get_data('name_ko', 'attraction'))
    db.insert_data('detail_raw', result_list)
    print(f'detail_raw {len(result_list)}개 데이터 insert 완료 {datetime.now().strftime('%Y%m%d%H%M%S')}')
    return result_list

if __name__ == "__main__":
    fetch_realtime_pop()