# Đồ án: Trợ lý phân loại cảm xúc tiếng Việt

Một ứng dụng Streamlit đơn giản cho phép người dùng nhập vào một câu tiếng Việt và nhận về kết quả phân loại cảm xúc (Tích cực, Tiêu cực, Trung tính). Ứng dụng được phát triển cho đồ án môn học.

![Hình ảnh demo ứng dụng] (Bạn nên chụp ảnh màn hình ứng dụng của mình và thêm vào đây)

## 1. Tính năng chính

* **Giao diện trực quan:** Xây dựng bằng Streamlit, chia làm 2 cột rõ ràng.
* **Phân loại cảm xúc:** Người dùng nhập câu và nhấn nút. Kết quả (Tích cực, Tiêu cực, Trung tính) cùng độ tin cậy sẽ được hiển thị.
* **Tiền xử lý:** Văn bản đầu vào được chuẩn hóa (chuyển chữ thường, sửa lỗi gõ tắt qua từ điển) và tokenized bằng `underthesea` trước khi đưa vào model.
* **Lịch sử phân loại:** 50 lần phân loại gần nhất được lưu trữ trong CSDL SQLite và hiển thị trên giao diện.
* **Quản lý lịch sử:** Người dùng có thể xóa toàn bộ lịch sử phân loại.

## 2. Công nghệ sử dụng

* **Ngôn ngữ:** Python 3.9+
* **Giao diện:** Streamlit
* **NLP Model:** `wonrax/phobert-base-vietnamese-sentiment` (từ Hugging Face Transformers)
* **Tiền xử lý:** `underthesea` (cho word tokenization)
* **Database:** `sqlite3` (lưu trữ lịch sử)
* **Data:** `pandas` (dùng để hiển thị lịch sử)

## 3. Cài đặt và Chạy dự án

### Yêu cầu
* Python 3.9+
* Pip và Venv

### Hướng dẫn cài đặt

1.  **Clone repository:**
    ```bash
    git clone https://github.com/PhamNamHocCode/Sentiment-Classification.git
    ```

2.  **(Khuyến khích) Tạo môi trường ảo:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Trên Windows dùng: venv\Scripts\activate
    ```

3.  **Cài đặt các thư viện cần thiết:**
    (Hãy chắc chắn bạn đã tạo tệp `requirements.txt` đầy đủ)
    ```bash
    pip install -r requirements.txt
    ```

### Hướng dẫn sử dụng

Chạy ứng dụng Streamlit bằng câu lệnh sau trong terminal:

```bash
streamlit run app.py