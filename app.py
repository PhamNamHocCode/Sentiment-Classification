import tkinter as tk
from tkinter import messagebox
import sys
import os

# Thêm thư mục gốc vào Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core import database as db
from src.core import sentiment as nlp
from src.ui.main_window import SentimentApp


def main():
    # Khởi tạo database
    try:
        db.init_db()
        print("Khởi tạo database thành công")
    except Exception as e:
        print(f"Lỗi khởi tạo database: {e}")
        messagebox.showerror("Lỗi", f"Không thể khởi tạo database: {e}")
        return
    
    # Tải model PhoBERT
    print("Đang tải PhoBERT model")
    try:
        nlp.load_model()
        print("Tải model thành công")
    except Exception as e:
        print(f"Lỗi tải model: {e}")
        messagebox.showerror("Lỗi", f"Không thể tải model PhoBERT: {e}\n\nVui lòng kiểm tra kết nối internet")
        return
    
    # Khởi chạy Tkinter
    root = tk.Tk()
    app = SentimentApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
