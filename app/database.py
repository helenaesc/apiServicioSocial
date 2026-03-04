import mysql.connector
from mysql.connector import Error
from .config import DB_CONFIG

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def fetch_all(sql, params=None):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or [])
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def fetch_one(sql, params=None):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or [])
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

def execute_tx(statements_fn):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        result = statements_fn(conn, cur)
        conn.commit()
        return result
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()