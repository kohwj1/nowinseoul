### 기상청 apihub(https://apihub.kma.go.kr/)를 활용하여 
# nx : 예보지점의 X 좌표값 = 동네예보 격자 번호(동서방향)
# ny : 예보지점의 Y 좌표값 = 동네예보 격자 번호(남북방향)

# fetch가 주된 작업이면 스레드 관리 오버헤드가 성능 저하를 일으킬 수 있기 때문에 비동기로만 작업

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import os,utils,aiohttp,asyncio
from dotenv import load_dotenv
from models import db
from itertools import chain


load_dotenv()  # .env 파일의 환경변수 로드
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
if not WEATHER_API_KEY:
    print(f'.env 파일에서 WEATHER_API_KEY를 입력하세요')

# I/O 바운드 작업은 비동기 처리
async def fetch_url(session, url):
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.text()

## 1. 기상청 api 데이터에서 임의 위·경도 → 인근 동네예보 격자 번호 변환 (lat,lng -> nx,ny)
async def mapping_xy(attraction_dict, session):
        # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    try:
        url = f'https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-dfs_xy_lonlat?lat={attraction_dict.get('lat')}&lon={attraction_dict.get('lng')}&authKey={WEATHER_API_KEY}'
        # print(f'fetching url : {url}')
        text = await fetch_url(session, url)

        # 간단한 문자열 처리이므로 동기 처리로 변경: 오버헤드 최소화
        nx, ny = text.replace(' ','').split('\n')[2].split(',')[2:4]

        return [{'id':attraction_dict.get('id'), 'nx':nx, 'ny':ny}]
    except Exception as e:
        print(f'error message : {e}')
        print(f"error url : {url}")

        return []  # [] 반환해 When flattened, it disappears.



## 1. 기상청 api 데이터에서 임의 위·경도 → 인근 동네예보 격자 번호 변환 (lat,lng -> nx,ny)
@utils.async_execution_time
async def main():
    attraction_list = db.get_data('id,lat,lng', 'attraction')
    async with aiohttp.ClientSession() as session:
        tasks = [mapping_xy(d, session) for d in attraction_list]
        results = await asyncio.gather(*tasks)
        # https://docs.python.org/ko/3/library/itertools.html#itertools.chain.from_iterable
        flattened = list(chain.from_iterable(results))

    db.update_xy(flattened)

if __name__ == "__main__":
    ## 1. 기상청 api 데이터에서 임의 위·경도 → 인근 동네예보 격자 번호 변환 (lat,lng -> nx,ny)
    asyncio.run(main())