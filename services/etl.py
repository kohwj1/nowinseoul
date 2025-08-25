### 데이터 ETL 및 DB반영, 캐싱 기능
# api_client에서 가져온 1시간 간격 데이터를 DB 캐싱 테이블로 ETL 처리
# 데이터 정제, 저장, 오류처리 로직 등

import sys
sys.path.append('/Users/seSAC/src/nowinseoul/nowinseoul')
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
    cursor.executemany(f"""INSERT INTO {domain}_cache ({', '.join(columns)}, insert_dttm)
                                             VALUES ({', '.join(map(lambda x: ':' + x, columns))}, {datetime.now().strftime("%Y%m%d%H%M%S")})""", rows)
    
    conn.commit()
    conn.close()
    print(f'{domain}_raw -> {domain}_cache etl 수행 완료 {datetime.now().strftime("%Y%m%d%H%M%S")}')

if __name__ == "__main__":
    domain_type = ['detail', 'weather','density']
    guidance = f"""raw_to_cache_etl('detail') 처럼 작성하세요.
        domain에는 {'/'.join(domain_type)}가 있습니다"""

    try:
        domain = sys.argv[1]
        print(f'Is {domain=} in domain_type? {domain in domain_type}')
    else:
        raise KeyError(guidance)

    raw_to_cache_etl(domain)

