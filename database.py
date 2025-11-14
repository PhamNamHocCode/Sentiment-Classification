import sqlite3 as sqlite
import pandas as pd
from datetime import datetime

DB_FILE = "sentiment_history.db"

"""Tạo kết nối đến CSDL SQLite."""
def get_db_connection():
    conn = sqlite.connect(DB_FILE)
    conn.row_factory = sqlite.Row
    return conn

"""Khởi tạo bảng sentiments nếu chưa tồn tại."""
def init_db():
    conn = get_db_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sentiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Lỗi khi khởi tạo DB: {e}")
    finally:
        conn.close()
"""
    Lưu kết quả phân loại vào CSDL
    Sử dụng parameterized queries (?) để chống SQL Injection
"""
def save_sentiment(text, sentiment):
    
    conn = get_db_connection()
    try:
        timestamp = datetime.now().isoformat()
        conn.execute(
            "INSERT INTO sentiments (text, sentiment, timestamp) VALUES (?, ?, ?)",
            (text, sentiment, timestamp)
        )
        conn.commit()
    except Exception as e:
        print(f"Lỗi khi lưu vào DB: {e}")
    finally:
        conn.close()
        
"""
    Tải 50 bản ghi mới nhất từ CSDL
    Trả về một Pandas DataFrame để Streamlit dễ dàng hiển thị
"""
def load_history():
    
    conn = get_db_connection()
    try:
        # Yêu cầu: Giới hạn 50 bản ghi mới nhất
        query = "SELECT timestamp, text, sentiment FROM sentiments ORDER BY timestamp DESC LIMIT 50"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Lỗi khi tải lịch sử: {e}")
        return pd.DataFrame(columns=["timestamp", "text", "sentiment"]) # Trả về DF rỗng nếu lỗi
    finally:
        conn.close()