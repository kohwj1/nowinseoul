### 스케줄러
# 5분마다 detail_raw -> detail_cache etl

from apscheduler.schedulers.background import BackgroundScheduler
from models.realtime_pop_etl import realtime_pop_etl

scheduler = BackgroundScheduler()

# 5분마다 realtime_pop_etl 실행
scheduler.add_job(realtime_pop_etl, 'interval', minutes=1, id='realtime_pop_etl')
