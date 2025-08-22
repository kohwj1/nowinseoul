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

def fetch(url):
    # https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
    # 조건문 없이 예외를 활용하는 EAFP 스타일로 작성
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 상태 코드 오류 체크 200이면 pass 아니면 에러 발생
        data = response.json() # JSON 응답을 Python dict로 변환
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}, {response=}")
        data = {}
    # else: Try 구문에서 else는 요청 성공
    #     print("요청 성공:", response.status_code)

    # 내부적으로는 json.loads()를 호출해 JSON 문자열을 파싱합니다.
    # JSON이 아닌 응답에 호출하면 예외(requests.exceptions.JSONDecodeError)가 발생합니다.
        
    return data