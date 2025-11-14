# Tên file: sentiment.py
import streamlit as st
from transformers import pipeline
import re

# --- Cấu hình NLP (Theo Mục VII.1) ---

# 1. Định nghĩa model.
# Chúng ta dùng model đã được fine-tune từ 'phobert-base' cho 3 nhãn cảm xúc
# (positive, negative, neutral), phù hợp với yêu cầu đồ án.
MODEL_NAME = "wonrax/phobert-base-vietnamese-sentiment"

# 2. Ánh xạ nhãn từ model về nhãn yêu cầu của đồ án (Mục III.1)
LABEL_MAP = {
    "POS": "POSITIVE",
    "NEG": "NEGATIVE",
    "NEU": "NEUTRAL"
}

# 3. Từ điển chuẩn hóa (Xử lý Mục VII.1 & Test Case 4, 2)
TEXT_NORM_DICT = {
    "rat": "rất",
    "dỡ": "dở"
    # (Có thể thêm các từ khác nếu cần)
}

# --- Tải Model (Cache) ---

@st.cache_resource
def load_model():
    """
    Tải pipeline và cache lại.
    Điều này giúp ứng dụng không cần tải lại model mỗi lần người dùng nhấn nút.
    (Đáp ứng Tiêu chí 1: Ứng dụng khởi động nhanh)
    """
    print("Đang tải model NLP... (Chỉ chạy 1 lần)")
    try:
        nlp_pipeline = pipeline('sentiment-analysis', model=MODEL_NAME)
        print("Tải model thành công!")
        return nlp_pipeline
    except Exception as e:
        print(f"Lỗi nghiêm trọng khi tải model: {e}")
        st.error(f"Không thể tải model NLP. Vui lòng kiểm tra kết nối mạng hoặc tên model: {MODEL_NAME}")
        return None

# --- Hàm Xử lý ---

def preprocess_text(text):
    """
    Chuẩn hóa văn bản đơn giản (Mục VII.1, Bước 1).
    Xử lý các trường hợp viết tắt, thiếu dấu cơ bản.
    """
    text = text.lower()
    
    # Dùng regex để thay thế từ đơn lẻ (ví dụ: "rat" chứ không phải "rate")
    for key, value in TEXT_NORM_DICT.items():
        text = re.sub(r'\b' + re.escape(key) + r'\b', value, text)
        
    # (Tùy chọn: Dùng underthesea.word_tokenize(text, format="text") nếu cần)
    return text


def classify_sentiment(text):
    """
    Hàm phân loại cảm xúc chính, sử dụng pipeline.
    (Triển khai Mục VII.1, Bước 2 & 3)
    """
    # Lấy pipeline đã cache
    nlp_pipeline = load_model()
    
    if nlp_pipeline is None:
        return {
            "text": text,
            "sentiment": "LỖI MODEL"
        }

    # 1. Tiền xử lý (Mục VII.1, Bước 1)
    processed_text = preprocess_text(text)

    # 2. Phân loại cảm xúc (Mục VII.1, Bước 2)
    # Pipeline trả về một list, chúng ta lấy phần tử đầu tiên
    result = nlp_pipeline(processed_text)[0]
    
    score = result['score']
    label = result['label'] # (VD: 'POS', 'NEG', 'NEU')

    # 3. Hợp nhất & Xử lý lỗi (Mục VII.1, Bước 3)
    
    # Yêu cầu: Nếu xác suất < 0.5, trả về NEUTRAL
    if score < 0.5:
        final_sentiment = "NEUTRAL"
    else:
        # Ánh xạ nhãn của model sang nhãn đồ án
        final_sentiment = LABEL_MAP.get(label, "NEUTRAL")

    # Yêu cầu đầu ra là một dictionary (Mục III.2)
    return {
        "text": text, # Trả về text gốc của người dùng
        "sentiment": final_sentiment
    }