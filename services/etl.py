### 데이터 ETL 및 DB반영, 캐싱 기능
# api_client에서 가져온 1시간 간격 데이터를 DB 캐싱 테이블로 ETL 처리
# 데이터 정제, 저장, 오류처리 로직 등

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models import db
from datetime import datetime

def raw_to_cache_etl(domain):
    conn = db.connect_db()
    cursor = conn.cursor()
    
    # extract
    cursor.execute(f'SELECT * FROM {domain}_raw')
    columns = [desc[0] for desc in cursor.description]
    columns.pop(columns.index('insert_dttm'))
    rows = [dict(r) for r in cursor.fetchall()]
    # transform 
    # load
    cursor.execute(f'DELETE FROM {domain}_cache')
    cursor.executemany(f"""INSERT INTO {domain}_cache ({', '.join(columns)})
                                             VALUES ({', '.join(map(lambda x: ':' + x, columns))})""", rows)
    
    conn.commit()
    conn.close()
    print(f'{domain}_raw -> {domain}_cache etl 수행 완료 {datetime.now().strftime("%Y%m%d%H%M%S")}')

if __name__ == "__main__":
    domain_type = ['detail', 'weather','density']
    guidance = f"""python etl.py detail 이렇게 작성하세요.
        domain에는 detail / weather / density 가 있습니다
        """

    args = [ i for i in sys.argv if i ]

    if len(args) == 1:
        print(guidance)
        print('지금은 detail, weather, density 모두 etl 됩니다')
        for d in domain_type:
            raw_to_cache_etl(d)
    elif len(args) == 2:    
        raw_to_cache_etl( args[1] )
    else:
        print(guidance)
        sys.exit()
