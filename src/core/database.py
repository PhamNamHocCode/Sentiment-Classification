import sqlite3
from datetime import datetime

DB_FILE = "sentiment.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Khởi tạo bảng sentiments nếu chưa tồn tại"""
    conn = get_connection()
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
        print(f"Lỗi khởi tạo database: {e}")
        raise
    finally:
        conn.close()


def save_sentiment(text, sentiment):
    """
    Lưu kết quả phân loại vào database
    Sử dụng parameterized queries để ko bị SQL injection
    """
    conn = get_connection()
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "INSERT INTO sentiments (text, sentiment, timestamp) VALUES (?, ?, ?)",
            (text, sentiment, timestamp)
        )
        conn.commit()
    except Exception as e:
        print(f"Lỗi lưu vào database: {e}")
        raise
    finally:
        conn.close()


def get_history(limit=50, offset=0):
    """
    Lấy lịch sử phân loại từ database
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            "SELECT id, text, sentiment, timestamp FROM sentiments ORDER BY id DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Lỗi tải lịch sử: {e}")
        return []
    finally:
        conn.close()


def get_total_count():
    """Đếm tổng số bản ghi trong database"""
    conn = get_connection()
    try:
        cursor = conn.execute("SELECT COUNT(*) FROM sentiments")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print(f"Lỗi đếm bản ghi: {e}")
        return 0
    finally:
        conn.close()


def clear_history():
    """Xóa toàn bộ lịch sử"""
    conn = get_connection()
    try:
        conn.execute("DELETE FROM sentiments")
        conn.commit()
    except Exception as e:
        print(f"Lỗi xóa lịch sử: {e}")
        raise
    finally:
        conn.close()


def get_sentiment_stats():
    """
    Thống kê số lượng từng loại cảm xúc
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            "SELECT sentiment, COUNT(*) as count FROM sentiments GROUP BY sentiment"
        )
        rows = cursor.fetchall()
        stats = {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
        for row in rows:
            stats[row["sentiment"]] = row["count"]
        return stats
    except Exception as e:
        print(f"Lỗi thống kê: {e}")
        return {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
    finally:
        conn.close()
