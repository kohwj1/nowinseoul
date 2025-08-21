### 현행 운영하는 따릉이 대여소 정보
# 매일 0시에 전체 대여소 정보를 불러옴
# "RENT_ID": "ST-827",
# "RENT_ID_NM": "1308. 안암로터리 버스정류장 앞",
# "STA_LAT": "37.58259201",
# "STA_LONG": "127.02897644",

# pip install googletrans
# https://pypi.org/project/googletrans/
import asyncio
from googletrans import Translator
from concurrent.futures import ThreadPoolExecutor
import requests, os
from dotenv import load_dotenv
from time import time
import sys
sys.path.append('/Users/seSAC/src/nowinseoul/nowinseoul')
from models import db
from itertools import repeat


load_dotenv()  # .env 파일의 환경변수 로드
API_KEY = os.getenv('API_KEY')
BIKE_STATION_ATTR = ['RENT_ID','RENT_NO','STA_LAT','STA_LONG','RENT_ID_NM']


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

def mapping_station_id(station_info: dict):
    # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    try:
        

# 필요한 속성만 가져오는 함수 from api
# station_info from api
# station_no_list from db
def subset_station_info(station_info: dict, station_no_list:list):
    key = station_info.get('RENT_ID_NM','0')  # key가 없으면 '0'
    station_no = station_info.get('RENT_NO')

    # station_no(PK)가 있는 레코드 = station_id가 없는 레코드(null)
    if station_no in station_no_list:
        
        return station_id, {"RENT_ID" : station_info.get("RENT_ID", '')}
    # station_no(PK)가 없는 레코드 = 추가된 대여소
    else:
        value = {attr: station_info.get(attr, '') for attr in BIKE_STATION_ATTR}
        
        return key, value

    '''# 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    try:
        key = station_info['RENT_ID_NM']  # key가 없으면 KeyError 발생
        value = {attr: station_info.get(attr, '') for attr in BIKE_STATION_ATTR}
        return key, value
    except KeyError:
        print(f"Missing key in station_info: {station_info}")
        return '0',None  # None 반환해 나중에 필터링 예정
    '''
# bike_station_info 생성 함수
def concurrent_processing(fn, load:list, station_no_list:list): # 전역변수보다 인수로 전달하는 것이 안전
    with ThreadPoolExecutor() as executor:
        results = dict(executor.map(fn, load, repeat(station_no_list)))
        if '0' in results.keys():
            results.pop('0')

    return results

# 한국어 대여소 이름 -> 영어 대여소 이름
async def translate_ko_to_en(bike_station_info):
# 이 번역 라이브러리가 한 번의 API 호출 또는 처리로 여러 문장을 번역하는 bulk 번역 기능을 사용한다
    async with Translator() as translator:
        translations = await translator.translate(list(bike_station_info.keys()), dest='en')
        for translation in translations:
            # print(f"{translation.origin}  ->  {translation.text}")
            bike_station_info[translation.origin]["RENT_ID_NM_EN"] = translation.text
    return bike_station_info

def main():
    # station_id만 필요한 station_no
    # 리스트 안에 원시값(숫자, 문자열 등 불변 객체)만 있다면 사실상 독립적인 리스트가 되고, 내부 요소 변경도 영향을 안 준다.
    # 여기서는 영향을 받아야하므로 얕은카피(.copy())하지 않음
    station_no_list = db.get_null_station_id()

    # for n in range(5): # 4001 부터는 없음
    for n in [3]: # 4001 부터는 없음
        # 한번에 1000개 까지 get(조회)
        url = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/tbCycleStationInfo/{n*1000 +1}/{(n+1)*1000}'
        print(url)
        data = fetch(url).get('stationInfo',False)

        # 데이터가 없는 page가 되면 loop 중단
        if not data:
            break
        
        # api 데이터 중 적재할 데이터만 추출
        bike_station_info = concurrent_processing(subset_station_info, data.get('row'),station_no_list)
        # bike_station_info = {"1308. 안암로터리 버스정류장 앞" : {"RENT_ID": "ST-827","RENT_ID_NM": "1308. 안암로터리 버스정류장 앞","STA_LAT": "37.58259201","STA_LONG": "127.02897644"}}
        print(len(bike_station_info))

        station_id = []
        new_station = []
        for k,v in bike_station_info :
            if '.' in k:
                new_station.append(k,v)
            else:
                station_id.append(k,v)

        

        # 한국어로된 대여소명을 영문으로 번역하여 bike_station_info 추가
        start = time()
        asyncio.run(translate_ko_to_en(bike_station_info))
        end = time()
        print(f"after adding en_name 실행 시간: {round(end - start)} 초 ",len(bike_station_info))
        # 1000개 : 5분 27초, 178개 : 56초 > 3_178개 : 17분 17초 예상

        # db에 적재
        db.insert_bike_station_info(list(bike_station_info.values()))
        print(f"{n*1000 +1} ~ {(n+1)*1000} 범위의 대여소 정보 적재 완료")

if __name__ == "__main__":
    main()