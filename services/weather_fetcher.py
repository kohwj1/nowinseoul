### 단기예보
# 원천부서 이원재(02-2133-4272)로 문의요청 2025.04.11 13:55 댓글
# 9월 중순에 api update 예정. 만약, 그 이후에도 느리면 기상청 api 허브에서 행정동/위치 고정시켜서 가져와야함.
# 날씨만 따로 api제공할 계획 없음(기상청 관할이기 때문)
#
# 기상청 apihub에서 가져옴 https://apihub.kma.go.kr/ -> 예특보탭 -> 단기예보 
# 보유기간	2008년 10월 30일 17:00KST(시행일 기준) ~ 현재
# 생산주기	2시부터 3시간 간격(일 8회) : 2 5 8 11 14 17 20 23

import sys
sys.path.append('/Users/seSAC/src/nowinseoul/nowinseoul')
from concurrent.futures import ThreadPoolExecutor
import os, utils
from dotenv import load_dotenv
from datetime import datetime
from models import db
from itertools import chain
from collections import defaultdict
import asyncio, aiohttp


load_dotenv()  # .env 파일의 환경변수 로드
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


# 비동기 fetch 함수
async def fetch_weather_async(session, url, nx, ny):
    """비동기로 날씨 데이터를 가져오는 함수"""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                fcst_list = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
                return {'nx': nx, 'ny': ny, 'data': fcst_list}
            else:
                print(f"HTTP {response.status} error for nx={nx}, ny={ny}")
                return {'nx': nx, 'ny': ny, 'data': []}
    except Exception as e:
        print(f'Fetch error for nx={nx}, ny={ny}: {e}')
        return {'nx': nx, 'ny': ny, 'data': []}

# 단일 시간대 그룹을 처리하는 함수 (스레드풀에서 실행)
def process_time_group(time_group_data):
    """각 시간대별 데이터를 처리하는 함수 (스레드에서 실행)"""
    time_key, items, nx, ny = time_group_data
    
    # 기본 결과 구조
    result = {
        "nx": nx,
        "ny": ny,
        "fcstDate": time_key
    }
    
    # POP, TMP 값 추출 (함수형 방식)
    target_categories = {"POP", "TMP"}
    category_data = {
        item["category"]: item["fcstValue"] 
        for item in items 
        if item["category"] in target_categories
    }
    result.update(category_data)
    
    # 결과 반환 (POP이나 TMP 중 하나라도 있으면 반환)
    return result if category_data else None

# fetch 데이터 chunk
def group_by_time_key_with_coords(fcst_list, nx, ny):
    """fcstDate + fcstTime을 키로 하여 데이터를 그룹화하고 좌표 정보 포함"""
    groups = defaultdict(list)
    
    # 그룹화
    for item in fcst_list:
        groups[f"{item['fcstDate']}{item['fcstTime']}"].append(item)
    
    # (time_key, list_of_items, nx, ny) 형태로 변환하고 시간순 정렬
    return [(time_key, items, nx, ny) for time_key, items in sorted(groups.items())]

def process_location_data(location_data):
    """단일 지역의 날씨 데이터를 처리하는 함수"""
    nx = location_data['nx']
    ny = location_data['ny']
    fcst_list = location_data['data']
    
    if not fcst_list:
        print(f'nx={nx}, ny={ny}는 날씨 예측정보를 제공하지 않습니다')
        return []
    
    # fcstDate + fcstTime으로 그룹화하고 좌표 정보 포함
    time_groups = group_by_time_key_with_coords(fcst_list, nx, ny)
    
    # ThreadPoolExecutor를 사용하여 각 시간대별로 병렬 처리
    with ThreadPoolExecutor() as executor:
        # 각 시간대 그룹을 병렬로 처리
        results = list(executor.map(process_time_group, time_groups))
    
    # None이 아닌 결과만 필터링하고 반환
    return [result for result in results if result is not None]

@utils.async_execution_time
async def make_weather_dataset():
    """메인 함수: 비동기 fetch + 스레드풀 처리"""
    
    # 좌표 데이터 가져오기 (frozenset으로 중복 제거)
    xy_id_map = defaultdict(list)
    for d in db.get_data('id,nx,ny', 'attraction'):
        xy_id_map[f"{d.get('nx')}_{d.get('ny')}"].append(d.get('id'))

    xy_list = list(xy_id_map.keys())
    print(f"처리할 지역 수: {len(xy_list)}")
    
    # 현재 시간 기반으로 base_date, base_time 계산
    now_date, now_time = datetime.now().strftime("%Y%m%d,%H").split(',')
    base_time = f"{(int(now_time)//3)*3-1:0>2}00"
    
    # 비동기로 모든 지역의 날씨 데이터 fetch
    async with aiohttp.ClientSession() as session:
        fetch_tasks = []
        
        for xy in xy_list:
            nx, ny = xy.split('_')
            url = (f'https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getVilageFcst'
                   f'?pageNo=1&numOfRows=144&dataType=JSON'
                   f'&base_date={now_date}&base_time={base_time}'
                   f'&nx={nx}&ny={ny}&authKey={WEATHER_API_KEY}')
            
            task = fetch_weather_async(session, url, nx, ny)
            fetch_tasks.append(task)
        
        print(f"비동기 fetch 시작 - {len(fetch_tasks)}개 지역")
        # 모든 fetch 작업을 동시에 실행
        fetch_results = await asyncio.gather(*fetch_tasks)
    
    print("비동기 fetch 완료, 데이터 처리 시작")
    
    # 스레드풀을 사용하여 각 지역의 데이터를 병렬 처리
    with ThreadPoolExecutor() as executor:
        # 각 지역의 데이터를 병렬로 처리
        processing_results = list(executor.map(process_location_data, fetch_results))
    
    # 모든 결과를 하나의 리스트로 평면화
    final_results = list(chain.from_iterable(processing_results))
    
    print(f'처리 완료: {len(final_results)}개 날씨 예측 데이터')
    print(f'완료 시간: {datetime.now().strftime("%Y.%m.%d %H:%M:%S")}')
    
    ## 기상청 api + 비동기-쓰레드풀 사용
    ## 처리 완료: 216(12*18)개 날씨 예측 데이터
    ## make_weather_dataset 함수 실행 시간: 0.4597초
    # 서울 도시데이터 api + 쓰레드풀 사용
    # weather_raw 1920(24*80)개 데이터 insert 완료 20250824224242
    # fetch_weather 함수 실행 시간: 30.6초

    insert_data = [
        {**d, 'id': id_}
        for d in final_results
        for id_ in xy_id_map.get(f"{d.get('nx')}_{d.get('ny')}", [])
    ]

    db.insert_data('weather_raw', insert_data)
    return final_results


if __name__ == "__main__":
    # 비동기 실행
    result = asyncio.run(make_weather_dataset())
    print(f"최종 결과 샘플: {result[0]=}")