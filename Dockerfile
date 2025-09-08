## Dockerfile

# 사용할 베이스 이미지 (Python 3.13.5 버전을 사용)
# 도커 허브에서 파이썬 이미지 찾기: https://hub.docker.com/_/python
FROM python:3.13-slim

# 컨테이너의 작업 디렉터리를 /app으로 (임의 설정)
WORKDIR /app

# apt update & upgrade in ubuntu only
# 패키지 업데이트 및 venv 기능 설치
# RUN apt update && apt upgrade -y 

# 로컬의 requirements.txt 파일을 컨테이너의 /app 디렉터리로 복사
COPY requirements.txt .

# requirements.txt에 명시된 모든 파이썬 패키지 설치 (venv 없이 시스템 pip 사용)
# venv 없이 시스템 pip 사용해 이미지 경량화
RUN pip install --no-cache-dir -r requirements.txt

# 로컬의 모든 파일을 컨테이너의 /app 디렉터리로 복사
COPY . .

# Entrypoint 스크립트 복사
COPY docker-entrypoint.sh .

# 일반 사용자 sesac 생성 (static dir, unix socket file 접근 권한을 위해 UID/GID 고정)
# 컨테이너 내에서 root가 아닌 다른 사용자로 프로세스를 실행하는 것은 보안 모범사례
# Dockerfile에서 adduser 로 sesac 같은 일반 사용자 생성(www-data uid:gid on ubuntu로 고정)
# adduser 명령에서 --gecos 옵션을 지정하지 않으면, 터미널에서 직접 이름이나 추가 정보를 입력하라는 프롬프트가 나올 수 있음.
# 스크립트 자동화 시에는 정보를 입력하지 않고 기본값으로 바로 생성할 때 --gecos ""를 사용해 이를 방지.
RUN adduser --uid 1001 --disabled-password --gecos "" --ingroup www-data sesac && chown -R sesac:www-data /app

# chown 으로 앱 디렉토리 권한도 해당 유저 소유로 변경

# USER sesac 으로 권한 변경 후 일반사용자로 컨테이너 실행하면
USER sesac

# Entrypoint 지정/설정
ENTRYPOINT ["./docker-entrypoint.sh"]

# Setting environment variables
# If your application uses environment variables,
# you can set environment variables in your Docker build using the ENV instruction.
# ENV FLASK_APP=hello

# Exposed ports
# This instruction isn't required,
# but it is a good practice and helps tools and team members understand what this application is doing.
# EXPOSE 8000

# 앱 실행
# CMD ["gunicorn", "-w", "2", "--bind", "0.0.0.0:8000","app:app"]