import sqlite3
from dotenv import load_dotenv

load_dotenv()  # .env 파일의 환경변수 로드

DATABASE = 'DATABASE'

# db에 접속하는 함수를 작성하시오.
def connect_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# 테이블 생성함수 작성하시오.
def create_table():
    conn =  connect_db()
    cur = conn.cursor()
    
    
    conn.commit()
    conn.close()
    
# 데이터 삽입 함수
def insert_user(name, age):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    
    conn.commit()
    conn.close()
    
# 데이터 조회 함수
def get_users():
    conn = connect_db()
    cur = conn.cursor()
    
    #  여기에 구현할것
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()  # 모든거 다
    
    conn.commit()
    conn.close()
    
    return rows  # 가져온 사용자 반환

def get_user_by_name(name):
    conn = connect_db()
    cur = conn.cursor()
    
    #  여기에 구현할것
    cur.execute('SELECT * FROM users WHERE name = ?', (name,))
    user = cur.fetchone()  # 사용자 한명만
    
    conn.commit()
    conn.close()
    
    return user

# 데이터 수정 함수
def update_user_age(name, new_age):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute('UPDATE users SET age=? WHERE name=?', (new_age, name))
    
    conn.commit()
    conn.close()
    
def delete_user_by_name(name):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM users WHERE name=?', (name,))
    
    conn.commit()
    conn.close()
    
def delete_user_by_age(age):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM users WHERE age=?', (age,))
    
    conn.commit()
    conn.close()
    
def delete_user_by_id(id):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM users WHERE id=?', (id,))
    
    conn.commit()
    conn.close()