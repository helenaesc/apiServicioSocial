import time
import os
import mysql.connector
from .config import DB_CONFIG


def _is_production():
    return (os.getenv("FLASK_ENV") or "").strip().lower() == "production"


def get_conn():
    retries = 10
    delay = 3
    last_error = None

    for i in range(retries):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            if not _is_production():
                print("✅ Conectado a la base de datos")
            return conn
        except Exception as e:
            last_error = e
            if not _is_production():
                print(f"❌ Intento {i+1} fallido: {e}")
            time.sleep(delay)

    raise Exception("No se pudo conectar a la base de datos") from last_error


def fetch_all(sql, params=None):
    conn = get_conn()
    cur = None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or [])
        return cur.fetchall()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def fetch_one(sql, params=None):
    conn = get_conn()
    cur = None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or [])
        return cur.fetchone()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def execute_tx(statements_fn):
    conn = get_conn()
    cur = None
    try:
        cur = conn.cursor(dictionary=True)
        result = statements_fn(conn, cur)
        conn.commit()
        return result
    except Exception:
        conn.rollback()
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()