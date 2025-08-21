### 데이터 ETL 및 DB반영, 캐싱 기능
# api_client에서 가져온 데이터를 DB 캐싱 테이블로 ETL 처리
# 데이터 정제, 저장, 오류처리 로직 등

import sys
sys.path.append('/Users/seSAC/src/nowinseoul/nowinseoul')
import models.db
from datetime import datetime

def realtime_pop_etl():
    conn = db.connect_db()
    cursor = conn.cursor()
    
    # extract
    cursor.execute('SELECT * FROM detail_raw')
    columns = [desc[0] for desc in cursor.description]
    columns.pop(columns.index('insert_dttm'))
    rows = [dict(r) for r in cursor.fetchall()]
    # transform 
    # load
    cursor.execute('DELETE FROM detail_cache')
    cursor.executemany(f'INSERT INTO detail_cache ({', '.join(columns)}) VALUES ({', '.join(map(lambda x: ':' + x, columns))})', rows)
    
    conn.commit()
    conn.close()
    print(f'realtime_pop_etl 수행 완료 {datetime.now.strftime("%Y%m%d%H%M%S")}')
