### 스케줄러
# 5분마다 실시간 인구밀도 en api -> detail_raw
# 5분마다 detail_raw -> detail_cache etl

# pip install apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
import sys, time
sys.path.append('/Users/seSAC/src/nowinseoul/nowinseoul')
from services.realtime_pop_etl import realtime_pop_etl
from services.realtime_pop_fetcher import fetch_realtime_pop

scheduler = BackgroundScheduler()

# 5분마다 fetch_realtime_pop 실행
scheduler.add_job(fetch_realtime_pop, 'interval', minutes=1, id='fetch_realtime_pop')

# 5분마다 realtime_pop_etl 실행
scheduler.add_job(realtime_pop_etl, 'interval', minutes=1, id='realtime_pop_etl')

scheduler.start()  # 스케줄러 시작

print("Scheduler started")

try:
    while True:
        time.sleep(1)  # 프로그램 종료 방지, 스케줄러는 백그라운드에서 계속 작업
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler stopped")