import sqlite3


def init():
  """테이블 생성"""
  conn = sqlite3.connect('db.sqlite')
  c = conn.cursor()
  c.execute('''
      CREATE TABLE IF NOT EXISTS config (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL
      )
  ''')
  conn.commit()
  conn.close()


def store_config(key, value):
    """데이터 등록 또는 수정"""
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('''
        INSERT INTO config (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    ''', (key, value))
    conn.commit()
    conn.close()


def fetch_config(key):
    """데이터 조회"""
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('SELECT value FROM config WHERE key = ?', (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
