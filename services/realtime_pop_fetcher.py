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

import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests, os
from dotenv import load_dotenv
from datetime import datetime
import sys
sys.path.append('/Users/seSAC/src/nowinseoul/nowinseoul')
from models import db

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

## 2. 실시간 인구밀도 데이터에서 도시ID - 인구밀도 매핑
def mapping_id(attraction_name_ko):
        # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    try:
        url = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/citydata_ppltn_eng/1/50/{attraction_name_ko}'
        # print(f'fetching url :{url}')

        city_data = fetch(url).get('SeoulRtd.citydata_ppltn')[0]

        area_code = city_data.get('AREA_CD') # POI008
        area_congestion_level = city_data.get('AREA_CONGEST_LVL') # 인구밀도혼잡도 레벨

        return {'id': area_code, 'realtime_pop': area_congestion_level}
  
    except Exception as e:
        print(f'error message : {e}')
        print(f"error url : {url}")
        return []  # [] 반환해 나중에 필터링 예정
    
# id - area_congestion_lvl 목록 생성 함수
def concurrent_processing(fn, load:list): # 전역변수보다 인수로 전달하는 것이 안전
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fn, load))

        return results

def fetch_realtime_pop():
    result_list = concurrent_processing(mapping_id,db.get_attraction_name())
    db.insert_congestion_lvl(result_list)
    print(f'detail_raw {len(result_list)}개 데이터 insert 완료 {datetime.now().strftime('%Y%m%d%H%M%S')}')
    return result_list

if __name__ == "__main__":
    fetch_realtime_pop()