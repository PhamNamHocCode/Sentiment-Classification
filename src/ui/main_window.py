import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from src.core import database as db
from src.core import sentiment as nlp
from src.ui.test_dialog import TestCaseDialog

class SentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phân loại cảm xúc Tiếng Việt - PhoBERT")
        self.root.state("zoomed")
        self.root.resizable(True, True)
        
        # Biến trạng thái
        self.is_processing = False
        self.current_history_page = 0
        self.history_limit = 50
        
        # Tạo giao diện
        self._create_widgets()
        
        # Tải lịch sử ban đầu
        self.refresh_history()
        
    def _create_widgets(self):
        """Tạo các widget giao diện"""
        left_frame = ttk.Frame(self.root, padding="10")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5))
        
        # Header
        ttk.Label(left_frame, text="Phân loại cảm xúc Tiếng Việt", 
                 font=("Arial", 16, "bold")).pack(pady=(0, 10))
        ttk.Label(left_frame, text="Sử dụng PhoBERT Transformer", 
                 font=("Arial", 10)).pack(pady=(0, 20))
        
        # Nhập câu
        ttk.Label(left_frame, text="Nhập câu cần phân loại:", 
                 font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(left_frame, height=4, 
                                                     font=("Arial", 11), wrap=tk.WORD)
        self.input_text.pack(fill="x", pady=(0, 10))
        self.input_text.insert("1.0", "Ví dụ: Python khó quá")
        self.input_text.bind("<FocusIn>", self._clear_placeholder)
        
        # Nút phân loại
        self.classify_btn = ttk.Button(left_frame, text="Phân loại cảm xúc", 
                                       command=self._handle_classify)
        self.classify_btn.pack(fill="x", pady=(0, 20))
        
        # Loading
        self.loading_label = ttk.Label(left_frame, text="", 
                                       font=("Arial", 10), foreground="blue")
        self.loading_label.pack(pady=(0, 10))
        
        # Kết quả
        ttk.Label(left_frame, text="Kết quả phân loại:", 
                 font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.result_frame = ttk.Frame(left_frame, relief="solid", borderwidth=1)
        self.result_frame.pack(fill="both", expand=True)
        
        self.result_label = ttk.Label(self.result_frame, 
                                      text="Vui lòng nhập câu và nhấn nút phân loại",
                                      font=("Arial", 12), foreground="gray",
                                      wraplength=450, justify="center")
        self.result_label.pack(expand=True, pady=50)
        
        # Nút Test Cases
        ttk.Button(left_frame, text="Chạy 10 Test Cases", 
                  command=self._show_test_dialog).pack(fill="x", pady=(20, 0))
        
        # Lịch sử
        right_frame = ttk.Frame(self.root, padding="10")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10))
        
        # Header lịch sử
        header_frame = ttk.Frame(right_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(header_frame, text="Lịch sử phân loại", 
                 font=("Arial", 12, "bold")).pack(side="left")
        
        self.count_label = ttk.Label(header_frame, text="(0 bản ghi)", 
                                     font=("Arial", 9), foreground="gray")
        self.count_label.pack(side="left", padx=(5, 0))
        
        # Pagination status
        self.pagination_label = ttk.Label(right_frame, text="", 
                                         font=("Arial", 9), foreground="blue")
        self.pagination_label.pack(anchor="w", pady=(0, 5))
        columns = ("ID", "Thời gian", "Nội dung", "Cảm xúc")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=20)
        
        # Cấu hình cột
        self.tree.heading("ID", text="ID")
        self.tree.heading("Thời gian", text="Thời gian")
        self.tree.heading("Nội dung", text="Nội dung")
        self.tree.heading("Cảm xúc", text="Cảm xúc")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Thời gian", width=150, anchor="center")
        self.tree.column("Nội dung", width=300, anchor="w")
        self.tree.column("Cảm xúc", width=120, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Nút hành động
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text="Làm mới danh sách", 
                  command=self.refresh_history).pack(side="left", padx=(0, 5))
        
        self.load_more_btn = ttk.Button(button_frame, text="Tải thêm 50", 
                  command=self._load_more)
        self.load_more_btn.pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Xóa tất cả", 
                  command=self._clear_history).pack(side="left", padx=5)
        
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)
    
    def _clear_placeholder(self, event):
        """Xóa placeholder khi focus vào input"""
        if self.input_text.get("1.0", "end-1c") == "Ví dụ: Python khó quá":
            self.input_text.delete("1.0", "end")
    
    def _handle_classify(self):
        """Xử lý sự kiện nhấn nút phân loại"""
        if self.is_processing:
            return
        
        text = self.input_text.get("1.0", "end-1c").strip()
        
        if not text or text == "Ví dụ: Python khó quá":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập câu cần phân loại")
            return
        
        # Tắt button và hiển thị loading
        self.is_processing = True
        self.classify_btn.config(state="disabled")
        self.loading_label.config(text="Đang phân tích")
        self.result_label.config(text="Đang xử lý...", foreground="blue")
        
        # Chạy phân loại trong thread riêng
        thread = threading.Thread(target=self._classify_thread, args=(text,))
        thread.daemon = True
        thread.start()
    
    def _classify_thread(self, text):
        """Thread phân loại cảm xúc"""
        try:
            result = nlp.classify_sentiment(text)
            
            # Cập nhật UI từ main thread
            self.root.after(0, self._update_result, result)
            
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
    
    def _update_result(self, result):
        """Cập nhật kết quả lên UI"""
        self.is_processing = False
        self.classify_btn.config(state="normal")
        self.loading_label.config(text="")
        
        # Kiểm tra lỗi
        if result.get("error_message"):
            self.result_label.config(
                text=f"Lỗi: {result['error_message']}", 
                foreground="red"
            )
            return
        
        # Hiển thị kết quả
        sentiment = result['sentiment']
        score = result['score']
        
        if sentiment == "POSITIVE":
            emoji = "😄"
            color = "green"
        elif sentiment == "NEGATIVE":
            emoji = "😞"
            color = "red"
        else:
            emoji = "😐"
            color = "orange"
        
        result_text = f"{emoji} {sentiment}\n\n(Độ tin cậy: {score:.1%})"
        self.result_label.config(text=result_text, foreground=color, font=("Arial", 16, "bold"))
        
        # Lưu vào database
        try:
            db.save_sentiment(result['text'], sentiment)
            self.refresh_history()
        except Exception as e:
            print(f"Lỗi lưu database: {e}")
    
    def _show_error(self, error_msg):
        """Hiển thị lỗi"""
        self.is_processing = False
        self.classify_btn.config(state="normal")
        self.loading_label.config(text="")
        self.result_label.config(text=f"Lỗi: {error_msg}", foreground="red")
    
    def refresh_history(self):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Reset về trang đầu
        self.current_history_page = 0
        
        # Tải dữ liệu mới
        try:
            history = db.get_history(limit=self.history_limit, offset=0)
            total_count = db.get_total_count()
            
            self.count_label.config(text=f"({total_count} bản ghi)")
            
            # Cập nhật pagination status
            loaded_count = min(self.history_limit, total_count)
            remaining = total_count - loaded_count
            if remaining > 0:
                self.pagination_label.config(text=f"Hiển thị {loaded_count} mới nhất (còn {remaining} bản ghi cũ hơn)")
                self.load_more_btn.config(state="normal")
            else:
                self.pagination_label.config(text=f"Hiển thị tất cả {loaded_count} bản ghi")
                self.load_more_btn.config(state="disabled")
            
            for record in history:
                sentiment = record['sentiment']
                
                # Định dạng hiển thị
                if sentiment == "POSITIVE":
                    tag = "positive"
                elif sentiment == "NEGATIVE":
                    tag = "negative"
                else:
                    tag = "neutral"
                
                self.tree.insert("", "end", values=(
                    record['id'],
                    record['timestamp'],
                    record['text'][:50] + "..." if len(record['text']) > 50 else record['text'],
                    sentiment
                ), tags=(tag,))
            
            # Định dạng tag màu
            self.tree.tag_configure("positive", foreground="green")
            self.tree.tag_configure("negative", foreground="red")
            self.tree.tag_configure("neutral", foreground="blue")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải lịch sử: {e}")
    
    def _load_more(self):
        """Tải thêm 50 bản ghi"""
        self.current_history_page += 1
        offset = self.current_history_page * self.history_limit
        
        try:
            history = db.get_history(limit=self.history_limit, offset=offset)
            total_count = db.get_total_count()
            
            if not history:
                messagebox.showinfo("Thông báo", "Không còn dữ liệu để tải")
                self.current_history_page -= 1
                self.load_more_btn.config(state="disabled")
                return
            
            for record in history:
                sentiment = record['sentiment']
                
                if sentiment == "POSITIVE":
                    tag = "positive"
                elif sentiment == "NEGATIVE":
                    tag = "negative"
                else:
                    tag = "neutral"
                
                self.tree.insert("", "end", values=(
                    record['id'],
                    record['timestamp'],
                    record['text'][:50] + "..." if len(record['text']) > 50 else record['text'],
                    sentiment
                ), tags=(tag,))
            
            # Cập nhật pagination status
            loaded_count = min((self.current_history_page + 1) * self.history_limit, total_count)
            remaining = total_count - loaded_count
            if remaining > 0:
                self.pagination_label.config(text=f"Đã tải {loaded_count}/{total_count} bản ghi (còn {remaining} bản ghi)")
                self.load_more_btn.config(state="normal")
            else:
                self.pagination_label.config(text=f"Đã tải tất cả {total_count} bản ghi")
                self.load_more_btn.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải thêm: {e}")
    
    def _clear_history(self):
        """Xóa toàn bộ lịch sử"""
        confirm = messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn xóa toàn bộ lịch sử?\n\nHành động này không thể hoàn tác",
            icon="warning"
        )
        
        if not confirm:
            return
        
        try:
            db.clear_history()
            self.refresh_history()
            self.result_label.config(
                text="Vui lòng nhập câu và nhấn nút phân loại",
                foreground="gray",
                font=("Arial", 12)
            )
            messagebox.showinfo("Thành công", "Đã xóa toàn bộ lịch sử")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa lịch sử: {e}")
    
    def _show_test_dialog(self):
        """Hiển thị dialog test cases"""
        TestCaseDialog(self.root, self.refresh_history)
