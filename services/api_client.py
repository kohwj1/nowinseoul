### OpenAPI로 실시간 데이터 수집 매니저
# OpenAPI에서 실시간 데이터 수집(5분 주기 호출로 분리)
# 외부 API 호출 관련 함수 및 예외 처리 등 집합

# https://docs.python.org/3/library/concurrent.futures.html
from concurrent.futures import ThreadPoolExecutor

import requests, os
from dotenv import load_dotenv

load_dotenv()  # .env 파일의 환경변수 로드

API_KEY = os.getenv('API_KEY')
attractions = ['강남 MICE 관광특구'
,'동대문 관광특구'
,'명동 관광특구'
,'이태원 관광특구'
,'잠실 관광특구']
# ,'종로·청계 관광특구'
# ,'홍대 관광특구'
# ,'경복궁'
# ,'광화문·덕수궁'
# ,'보신각'
# ,'서울 암사동 유적'
# ,'창덕궁·종묘'
# ,'건대입구역'
# ,'고속터미널역'
# ,'삼각지역'
# ,'서울식물원·마곡나루역'
# ,'서울역'
# ,'신논현역·논현역'
# ,'신림역'
# ,'신촌·이대역'
# ,'역삼역'
# ,'왕십리역'
# ,'용산역'
# ,'합정역'
# ,'혜화역'
# ,'가락시장'
# ,'가로수길'
# ,'광장(전통)시장'
# ,'노량진'
# ,'덕수궁길·정동길'
# ,'북촌한옥마을'
# ,'서촌'
# ,'성수카페거리'
# ,'압구정로데오거리'
# ,'여의도'
# ,'연남동'
# ,'영등포 타임스퀘어'
# ,'용리단길'
# ,'이태원 앤틱가구거리'
# ,'인사동'
# ,'청담동 명품거리'
# ,'청량리 제기동 일대 전통시장'
# ,'해방촌·경리단길'
# ,'DDP(동대문디자인플라자)'
# ,'DMC(디지털미디어시티)'
# ,'강서한강공원'
# ,'고척돔'
# ,'광나루한강공원'
# ,'광화문광장'
# ,'국립중앙박물관·용산가족공원'
# ,'난지한강공원'
# ,'남산공원'
# ,'노들섬'
# ,'뚝섬한강공원'
# ,'망원한강공원'
# ,'반포한강공원'
# ,'북서울꿈의숲'
# ,'서리풀공원·몽마르뜨공원'
# ,'서울광장'
# ,'서울대공원'
# ,'서울숲공원'
# ,'아차산'
# ,'양화한강공원'
# ,'어린이대공원'
# ,'여의도한강공원'
# ,'월드컵공원'
# ,'응봉산'
# ,'이촌한강공원'
# ,'잠실종합운동장'
# ,'잠실한강공원'
# ,'잠원한강공원'
# ,'청계산'
# ,'청와대'
# ,'북창동 먹자골목'
# ,'남대문시장'
# ,'익선동'
# ,'잠실롯데타워 일대'
# ,'송리단길·호수단길'
# ,'신촌 스타광장'
# ,'보라매공원'
# ,'서대문독립공원'
# ,'여의서로'
# ,'올림픽공원'
# ,'홍제폭포']

urls = [f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/citydata/1/5/{attr}' for attr in attractions]

def fetch(url):
    response = requests.get(url)
    return response.text

# If max_workers is None or not given, it will default to os.process_cpu_count(){실제 사용 가능한 CPU 수}.
def concurrent_processing(urls, max_workers=None):
    results = []
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch, urls))

    return results

# 실행
responses = concurrent_processing(urls)
print(f"Total responses: {responses}")