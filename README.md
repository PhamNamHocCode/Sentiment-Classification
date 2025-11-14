# Đồ án: Trợ lý phân loại cảm xúc tiếng Việt (Vietnamese Sentiment Assistant)

Một ứng dụng "Trợ lý phân loại cảm xúc tiếng Việt" được phát triển cho đồ án môn học. Ứng dụng cho phép người dùng nhập vào một câu tiếng Việt và trả về kết quả phân loại cảm xúc (Tích cực, Trung tính, Tiêu cực) sử dụng mô hình Transformer (PhoBERT).

## 1. Tính năng chính

* **Nhập liệu:** Người dùng nhập một câu tiếng Việt tự do qua giao diện Streamlit.
* **Phân loại cảm xúc:** Ứng dụng sử dụng mô hình `vinai/phobert-base-v2` từ Hugging Face để phân loại cảm xúc thành 3 nhãn:
    * `POSITIVE` (Tích cực)
    * `NEUTRAL` (Trung tính)
    * `NEGATIVE` (Tiêu cực)
* **Lưu trữ cục bộ:** Toàn bộ lịch sử phân loại (bao gồm câu nhập vào, nhãn cảm xúc, và thời gian) được lưu trữ trong một cơ sở dữ liệu **SQLite** cục bộ
* **Hiển thị kết quả:** Giao diện hiển thị ngay lập tức kết quả phân loại và danh sách lịch sử 50 lần phân loại gần nhất.

## 2. Công nghệ sử dụng

* **Ngôn ngữ:** Python
* **Giao diện:** Streamlit 
* **NLP Model:** `vinai/phobert-base-v2` (Hugging Face Transformers)
* **Tiền xử lý:** `underthesea` (cho word tokenization)
* **Database:** `sqlite3` (Thư viện chuẩn của Python)

## 3. Cài đặt và Chạy dự án

### Yêu cầu
* Python 3.8+

### Hướng dẫn cài đặt

1.  **Clone repository:**
    ```bash
    git clone https://github.com/PhamNamHocCode/Sentiment-Classification.git
    cd [TEN_THU_MUC]
    ```

2.  **(Khuyến khích) Tạo môi trường ảo:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Trên Windows dùng: venv\Scripts\activate
    ```

3.  **Cài đặt các thư viện cần thiết:**
    ```bash
    pip install -r requirements.txt
    ```

### Hướng dẫn sử dụng

Chạy ứng dụng Streamlit bằng câu lệnh sau:

```bash
streamlit run app.py