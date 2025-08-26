import time # 타임 데코레이터
def execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execut_time = end_time - start_time
        print(f"{func.__name__} 함수 실행 시간: {round((execut_time)%60,1)}초")
        return result
    return wrapper

import requests
def fetch(url, max_retries=3) -> dict:
    # https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
    # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
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
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json;charset=UTF-8"
            }
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed for {url}: {e}")
    return {}

if __name__ == "__main__":
    url='http://openapi.seoul.go.kr:8088/46715879706a67793230514e72755a/json/citydata/1/50/보신각'
    fetch(url)