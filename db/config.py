import psycopg2

DB_SETTINGS = {
    "dbname": "FinanceTracker",
    "user": "postgres", 
    "password": "1111", 
    "host": "localhost",
    "port": 5432,
}

def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        return conn
    except Exception as e:
        print(f"[!] Ошибка подключения к базе данных: {e}")
        return None, None
