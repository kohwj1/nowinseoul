import time # 타임 데코레이터
def execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execut_time = end_time - start_time
        print(f"{func.__name__} 함수 실행 시간: {round((execut_time)%60,9)}초")
        return result
    return wrapper

import requests, time
def fetch(url, max_retries=3) -> dict:
    # https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
    # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    for attempt in range(max_retries):
        try:
            response = requests.get(url) # 손실데이터가 많아져서 안씀 : 타임아웃을 4초로 설정 3.51s 쯤 걸려서
            response.raise_for_status()  # HTTP 상태 코드 오류 체크 200이면 pass 아니면 에러 발생
            # print(f'{response=}\n{response.text=}')
            data = response.json() # JSON 응답을 Python dict로 변환
    # 내부적으로는 json.loads()를 호출해 JSON 문자열을 파싱합니다.
    # JSON이 아닌 응답에 호출하면 예외(requests.exceptions.JSONDecodeError)가 발생합니다.
            
            return data
        except Exception as err:
            print(f"Attempt {attempt+1}/{max_retries} - Unexpected {err=}, {type(err)=}, {url=}")
    # else: Try 구문에서 else는 요청 성공
    #     print("요청 성공:", response.status_code)

        # 재시도 전에 지연 시간(backoff)을 줍니다. <- 이러면 페이지 뜨는 속도가 느려지기에 안함
        # 지수적 백오프(Exponential Backoff)를 적용해 재시도 횟수가 늘수록 지연 시간도 길어집니다.
        # 재시도 횟수가 증가할수록 대기 시간을 길게 가져가므로, 서버에 연속적인 부하를 주지 않고 스스로 회복할 시간을 줍니다.
        # if attempt < max_retries - 1:
        #     wait_time = 2 ** attempt  # 1, 2, 4초 순으로 지연
        #     print(f"Waiting for {wait_time} seconds before retrying...")
        #     time.sleep(wait_time)

    # 재시도 모두 실패한 경우 빈 딕셔너리 반환
    return {}


import time
import functools
def async_execution_time(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} 함수 실행 시간: {end - start:.4f}초")
        return result
    return wrapper


async def async_fetch(session, url, max_retries=3):
    for attempt in range(max_retries):
        try:
            # 서울시 api 업데이트로인해 header 추가하지 않아도 됨
            # headers = {
            #     "Accept": "application/json",
            #     "Content-Type": "application/json;charset=UTF-8"
            # }
            # async with session.get(url, headers=headers) as response:
            async with session.get(url) as response:
                print(f'fetching url : {url}')
                response.raise_for_status()
                data = await response.json()
                # print(f'ok fetch data :{data=}')
                return data
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed for {url=}: {e=}")

    return {}

if __name__ == "__main__":
    url='http://openapi.seoul.go.kr:8088/46715879706a67793230514e72755a/json/citydata/1/50/보신각'
    fetch(url)