#!/bin/bash
## docker-entrypoint.sh
set -e

# unix socket file이 충돌하므로 파일이 있으면 지워야함
if [ -e $SOCKET_PATH ]; then
    rm $SOCKET_PATH
fi

# 환경변수 DB_PATH 가 설정돼 있지 않을 때 기본 경로(./instance/nowinseoul.db)를 지정
# 경로 자체는 일반적으로 민감정보에 해당하지 않습니다.
# 예를 들어 데이터베이스 파일 위치를 알려주는 것 자체만으론 보안 위험이 작습니다.
# 보안상 중요한 것은 실제 비밀번호, API 키, 인증서, 토큰과 같은 ‘비밀’ 정보이며, 이를 환경변수나 이미지에 하드코딩하면 심각한 노출 위험이 됩니다.
DB_PATH="${DB_PATH}"

# instance 폴더가 없으면 생성
mkdir -p "$(dirname "$DB_PATH")"

# DB 파일 존재하지 않으면 init_db.py 실행
if [ ! -f "$DB_PATH" ]; then
  echo "[ENTRYPOINT] Database not found at $DB_PATH. Initializing..."
  python init_app.py
else
  echo "[ENTRYPOINT] Database found at $DB_PATH. Skipping initialization."
fi

# 앱 실행 (gunicorn 추천)
# https://flask.palletsprojects.com/en/latest/deploying/ : deployment to product = WEBserver<nginx>(WSGI<gunicorn>)
# https://flask.palletsprojects.com/en/stable/deploying/gunicorn/
# Gunicorn은 Python WSGI 서버로, Flask 같은 웹 애플리케이션을 프로덕션 환경에서 효율적으로 실행하기 위해 설계된 서버
# API 서버가 ‘동시에 많은 요청’을 받아야 하거나, 대용량 I/O 서버(채팅, 실시간 등)가 필요하다면
# gevent나 eventlet 워커 타입과 그 패턴을 실제로 적용해야하지만 우리는 둘 다 아니니까 워커만
# You can bind to all external IPs on a non-privileged port using the -b 0.0.0.0 option.
# Don’t do this when using a reverse proxy setup, otherwise it will be possible to bypass the proxy.
# EC2 t3.small은 vCPU 2개, RAM 2G 제공으로 -w(워커 2개) -b(바인딩 포트 8000) app:app <- app.py에서 app=Flask(__name__)으로 사용
echo "[ENTRYPOINT] Starting Gunicorn..."
# TCP 소켓 통신일 경우
# exec gunicorn -w 2 --bind 0.0.0.0:8000 app:app

# UNIX 소켓 통신일 경우, --bind unix:/path
# 소유자와 그룹에 읽기/쓰기 권한이 주어지고(OS default 권한 마스크에 따름),다른 사용자에게는 권한이 부여되지 않음
# --umask 007[octal] 적용하면 => 666-007 = 660[octal](ref.https://docs.gunicorn.org/en/stable/settings.html#umask) 
exec gunicorn -w 2 --umask 007 --bind unix:$SOCKET_PATH app:app