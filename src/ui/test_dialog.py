import tkinter as tk
from tkinter import ttk, messagebox
import threading
from src.core import sentiment as nlp


class TestCaseDialog:
    """Dialog chạy và hiển thị kết quả 10 test cases"""
    
    TEST_CASES = [
        ("Hôm nay tôi rất vui", "POSITIVE"),
        ("Món ăn này dỡ quá", "NEGATIVE"),
        ("Thời tiết bình thường", "NEUTRAL"),
        ("Rat vui hom nay", "POSITIVE"),
        ("Công việc ổn định", "NEUTRAL"),
        ("Phim này hay lắm", "POSITIVE"),
        ("Tôi buồn vì thất bại", "NEGATIVE"),
        ("Ngày mai đi học", "NEUTRAL"),
        ("Cảm ơn bạn rất nhiều", "POSITIVE"),
        ("Mệt mỏi quá hôm nay", "NEGATIVE")
    ]
    
    def __init__(self, parent, refresh_callback):
        self.parent = parent
        self.refresh_callback = refresh_callback
        self.is_running = False
        self.results = []
        
        # Tạo cửa sổ dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Chạy 10 Test Cases")
        self.dialog.geometry("900x600")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Tạo các widget trong dialog"""
        # Header
        header_frame = ttk.Frame(self.dialog, padding="10")
        header_frame.pack(fill="x")
        
        ttk.Label(header_frame, text="Kiểm tra độ chính xác với 10 Test Cases", 
                 font=("Arial", 14, "bold")).pack()
        ttk.Label(header_frame, text="Yêu cầu: ≥ 65% (≥ 6.5/10 đúng)", 
                 font=("Arial", 10), foreground="gray").pack()
        
        # Progress frame
        progress_frame = ttk.Frame(self.dialog, padding="10")
        progress_frame.pack(fill="x")
        
        self.progress_label = ttk.Label(progress_frame, text="Nhấn 'Bắt đầu' để chạy test", 
                                       font=("Arial", 10))
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=800, mode='determinate')
        self.progress_bar.pack(pady=(5, 0))
        
        # Treeview kết quả
        tree_frame = ttk.Frame(self.dialog, padding="10")
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("STT", "Đầu vào", "Mong đợi", "Thực tế", "Tin cậy", "Kết quả")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("STT", text="STT")
        self.tree.heading("Đầu vào", text="Đầu vào")
        self.tree.heading("Mong đợi", text="Mong đợi")
        self.tree.heading("Thực tế", text="Thực tế")
        self.tree.heading("Tin cậy", text="Tin cậy")
        self.tree.heading("Kết quả", text="Kết quả")
        
        self.tree.column("STT", width=50, anchor="center")
        self.tree.column("Đầu vào", width=250, anchor="w")
        self.tree.column("Mong đợi", width=100, anchor="center")
        self.tree.column("Thực tế", width=100, anchor="center")
        self.tree.column("Tin cậy", width=80, anchor="center")
        self.tree.column("Kết quả", width=80, anchor="center")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Tag colors
        self.tree.tag_configure("pass", foreground="green")
        self.tree.tag_configure("fail", foreground="red")
        
        # Summary frame
        summary_frame = ttk.Frame(self.dialog, padding="10")
        summary_frame.pack(fill="x")
        
        self.summary_label = ttk.Label(summary_frame, text="", 
                                       font=("Arial", 12, "bold"))
        self.summary_label.pack()
        
        # Button frame
        button_frame = ttk.Frame(self.dialog, padding="10")
        button_frame.pack(fill="x")
        
        self.start_btn = ttk.Button(button_frame, text="🚀 Bắt đầu", 
                                    command=self._start_test)
        self.start_btn.pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Đóng", 
                  command=self.dialog.destroy).pack(side="right", padx=5)
    
    def _start_test(self):
        """Bắt đầu chạy test cases"""
        if self.is_running:
            return
        
        # Reset
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.results = []
        self.progress_bar['value'] = 0
        self.summary_label.config(text="")
        self.start_btn.config(state="disabled")
        self.is_running = True
        
        # Chạy test trong thread
        thread = threading.Thread(target=self._run_tests)
        thread.daemon = True
        thread.start()
    
    def _run_tests(self):
        """Chạy test cases trong thread"""
        try:
            for i, (text, expected) in enumerate(self.TEST_CASES):
                # Update progress
                self.dialog.after(0, self.progress_label.config, 
                                 {"text": f"Đang test case {i+1}/10: {text[:30]}..."})
                
                # Phân loại
                result = nlp.classify_sentiment(text)
                actual = result['sentiment']
                score = result.get('score', 0.0)
                
                is_correct = (actual == expected)
                
                # Lưu kết quả
                self.results.append({
                    "stt": i + 1,
                    "input": text,
                    "expected": expected,
                    "actual": actual,
                    "score": score,
                    "correct": is_correct
                })
                
                # Update UI
                self.dialog.after(0, self._update_tree_row, i + 1, text, expected, actual, score, is_correct)
                self.dialog.after(0, self.progress_bar.config, {"value": (i + 1) * 10})
            
            # Hoàn thành
            self.dialog.after(0, self._finish_test)
            
        except Exception as e:
            self.dialog.after(0, messagebox.showerror, "Lỗi", f"Lỗi khi chạy test: {e}")
            self.dialog.after(0, self._reset_ui)
    
    def _update_tree_row(self, stt, input_text, expected, actual, score, is_correct):
        """Cập nhật một dòng kết quả vào tree"""
        tag = "pass" if is_correct else "fail"
        result_text = "✓ Đúng" if is_correct else "✗ Sai"
        
        self.tree.insert("", "end", values=(
            stt,
            input_text,
            expected,
            actual,
            f"{score:.1%}",
            result_text
        ), tags=(tag,))
    
    def _finish_test(self):
        """Kết thúc test và hiển thị tổng kết"""
        correct_count = sum(1 for r in self.results if r['correct'])
        accuracy = correct_count / 10
        
        summary_text = f"Kết quả: {correct_count}/10 đúng - Độ chính xác: {accuracy:.1%}"
        
        if accuracy >= 0.65:
            summary_text += " ✅ ĐẠT YÊU CẦU"
            color = "green"
        else:
            summary_text += " ❌ CHƯA ĐẠT"
            color = "red"
        
        self.summary_label.config(text=summary_text, foreground=color)
        self.progress_label.config(text="Hoàn thành")
        
        self._reset_ui()
        
        # Refresh main window nếu có callback
        if self.refresh_callback:
            self.refresh_callback()
    
    def _reset_ui(self):
        """Reset trạng thái UI"""
        self.is_running = False
        self.start_btn.config(state="normal")
