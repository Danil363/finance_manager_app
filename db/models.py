import sys
from pathlib import Path
from typing import Optional

# Добавляем папку `program/` в пути Python
sys.path.append(str(Path(__file__).parent.parent))  # Поднимаемся на уровень выше

from db.config import *  
from datetime import date


conn = connect_to_db()

def get_data_by_period(conn, date_from: date, date_to: date):
    query = """
        SELECT * FROM transactions
        WHERE date >= %s AND date <= %s
        ORDER BY date;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (date_from, date_to))
            results = cur.fetchall()
            return results
        
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []
    
def get_data_by_type(conn, date_from: date, date_to: date, type: str):
    query = """
        SELECT * FROM transactions
        WHERE date >= %s AND date <= %s AND type = %s
        ORDER BY date;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (date_from, date_to, type))
            results = cur.fetchall()
            return results
        
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []
    
def add_record(conn, type: str, date: date, category: str, description: Optional[str] = None, amount: float = 0.0):
    query = """
        INSERT INTO transactions (type, date, category, description, amount)
        VALUES (%s, %s, %s, %s, %s);
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (type, date, category, description, amount))
        conn.commit()
    except Exception as e:
        print(f"Ошибка добавления записи: {e}")
        conn.rollback()

def delete_record(conn, id):
    query = """
        DELETE FROM transactions
        WHERE id = %s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (id,))
        conn.commit()
    except Exception as e:
        print(f"Ошибка удаления записи: {e}")
        conn.rollback()
    

def update_record(conn, record_id: int, type_: str, date_, category: str, description: str, amount: float):
    query = """
        UPDATE transactions
        SET type = %s,
            date = %s,
            category = %s,
            description = %s,
            amount = %s
        WHERE id = %s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (type_, date_, category, description, amount, record_id))
        conn.commit()
    except Exception as e:
        print(f"Ошибка обновления записи: {e}")
        conn.rollback()
        raise


def get_exp_data(conn, date_from: date, date_to: date):
    query = """
        SELECT transactions.category, SUM(amount) FROM transactions

        WHERE date >= %s AND date <= %s    AND type = 'expense'
		GROUP BY category
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (date_from, date_to))
            
            rows = cur.fetchall()
            results = {row[0]: row[1] for row in rows}
            return results
        
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []
    

def get_inc_data(conn, date_from: date, date_to: date):
    query = """
        SELECT transactions.category, SUM(amount) FROM transactions

        WHERE date >= %s AND date <= %s    AND type = 'income'
		GROUP BY category
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (date_from, date_to))
            
            rows = cur.fetchall()
            results = {row[0]: row[1] for row in rows}
            return results
        
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []
    

def get_max_exp(conn, date_from: date, date_to: date):
    query = """
        SELECT transactions.category, SUM(amount) FROM transactions

        WHERE date >= %s AND date <= %s    AND type = 'expense'
		GROUP BY category
        ORDER BY SUM(amount) DESC
		LIMIT 1
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (date_from, date_to))
            
            
            result =  cur.fetchall()
            return result if result != [] else [("", '')]
        
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []
    
def get_min_exp(conn, date_from: date, date_to: date):
    query = """
        SELECT transactions.category, SUM(amount) FROM transactions

        WHERE date >= %s AND date <= %s    AND type = 'expense'
		GROUP BY category
        ORDER BY SUM(amount) 
		LIMIT 1
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (date_from, date_to))
            
            
            result =  cur.fetchall()
            return result if result != [] else [("", '')]
        
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []
    
def get_max_inc(conn, date_from: date, date_to: date):
    query = """
        SELECT transactions.category, SUM(amount) FROM transactions

        WHERE date >= %s AND date <= %s    AND type = 'income'
		GROUP BY category
        ORDER BY SUM(amount) DESC
		LIMIT 1
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (date_from, date_to))
            
            
            result =  cur.fetchall()
            return result if result != [] else [("", '')]
        
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []
    
def get_min_inc(conn, date_from: date, date_to: date):
    query = """
        SELECT transactions.category, SUM(amount) FROM transactions

        WHERE date >= %s AND date <= %s    AND type = 'income'
		GROUP BY category
        ORDER BY SUM(amount) 
		LIMIT 1
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (date_from, date_to))
            
            
            result =  cur.fetchall()
            return result if result != [] else [("", '')]
        
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []
    

def get_sum_exp(conn, date_from: date, date_to: date):
    query = """
        SELECT  transactions.type, SUM(amount) FROM transactions

        WHERE date >= %s AND date <= %s    AND type = 'expense'
		GROUP BY type

    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (date_from, date_to))
            
            
            result =  cur.fetchall()

            return result if result != [] else [("", '')]
        
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []
   

def get_sum_inc(conn, date_from: date, date_to: date):
    query = """
        SELECT  transactions.type, SUM(amount) FROM transactions

        WHERE date >= %s AND date <= %s    AND type = 'income'
		GROUP BY type

    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (date_from, date_to))
            
            
            result =  cur.fetchall()
            return result if result != [] else [("", '')]
        
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []
   