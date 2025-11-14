# Sentiment-Classification

## Mô tả
Ứng dụng phân loại cảm xúc tiếng Việt sử dụng mô hình PhoBERT và giao diện Streamlit. Ứng dụng cho phép người dùng nhập câu tiếng Việt và nhận kết quả phân loại cảm xúc (Tích cực, Tiêu cực, Trung tính). Lịch sử phân loại cũng được lưu trữ và hiển thị trong giao diện.

## Cài đặt
1. Cài đặt Python (phiên bản >= 3.8).
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
   Hoặc cài đặt thủ công:
   ```bash
   pip install transformers torch
   pip install streamlit pandas underthesea
   ```

## Cách chạy ứng dụng
1. Chạy ứng dụng bằng lệnh:
   ```bash
   streamlit run app.py
   ```
2. Mở trình duyệt và truy cập địa chỉ được cung cấp (thường là `http://localhost:8501`).

## Cách sử dụng
1. Nhập câu tiếng Việt vào ô nhập liệu.
2. Nhấn nút "Phân loại cảm xúc" để xem kết quả.
3. Xem lịch sử phân loại ở cột bên phải.

## Cấu trúc thư mục
- `app.py`: File chính để chạy ứng dụng.
- `sentiment.py`: Xử lý logic phân loại cảm xúc.
- `local_model/`: Chứa các file liên quan đến mô hình PhoBERT.
- `README.md`: Hướng dẫn sử dụng ứng dụng.

## Ghi chú
- Đảm bảo kết nối Internet để tải model PhoBERT khi chạy lần đầu.
- Nếu gặp lỗi, kiểm tra lại các thư viện đã được cài đặt đúng chưa.