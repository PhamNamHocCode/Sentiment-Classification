import streamlit as st
from transformers import pipeline
import re
from underthesea import word_tokenize
import sys

# Cấu hình NLP
MODEL_NAME = "wonrax/phobert-base-vietnamese-sentiment"
LABEL_MAP = {
    "POS": "POSITIVE",
    "NEG": "NEGATIVE",
    "NEU": "NEUTRAL"
}
PREPROCESSING_DICT = {
    "rat": "rất", 
    "dỡ": "dở", 
    "bt": "bình thường", 
    "ok": "tốt",
    "good": "tốt", "gud": "tốt", 
    "k": "không", "ko": "không",
    "bth": "bình thường", 
    "dc": "được", "đc": "được", 
    "vs": "với",
    "mn": "mọi người", 
    "hnay": "hôm nay", 
    "qá": "quá", 
    "xau": "xấu",
    "hk": "không", 
    "thik": "thích", 
    "dep": "đẹp", 
    "sp": "sản phẩm",
    "cham": "chậm"
}

# Tải Model
#Tải pipeline và cache lại
@st.cache_resource
def load_model():
    print("Đang tải model . . .")
    try:
        nlp_pipeline = pipeline('sentiment-analysis', model=MODEL_NAME)
        print("Tải model thành công")
        return nlp_pipeline
    except Exception as e:
        print(f"Lỗi khi tải model: {e}")
        st.error(f"Không thể tải model: {MODEL_NAME}")
        return None

# Hàm Xử lý
#Chuẩn hóa văn bản
def preprocess(text):
    text = text.lower()
    
    for key, value in PREPROCESSING_DICT.items():
        text = re.sub(r'\b' + re.escape(key) + r'\b', value, text)
        
    try:
        text = word_tokenize(text, format="text")
    except Exception as e:
        print(f"Lỗi khi word_tokenize: {e}. Sử dụng văn bản gốc đã chuẩn hóa.", file=sys.stderr)
        pass
    
    return text

# Phân loại cảm xúc
def classify_sentiment(text):
    # 1. Kiểm tra độ dài
    if not text or len(text.strip()) < 5:
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": "Câu không hợp lệ (yêu cầu ≥ 5 ký tự)."
        }
    
    # 2. Kiểm tra chỉ chứa số, ký tự đặc biệt
    # Kiểm tra xem có bất kỳ ký tự chữ (alphabet) nào không
    if not any(c.isalpha() for c in text):
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": "Câu không hợp lệ (phải chứa ký tự chữ)."
        }

    # Lấy pipeline đã cache
    nlp_pipeline = load_model()
    
    if nlp_pipeline is None:
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": "Lỗi: Không thể tải được Model NLP."
        }

    # 1. Tiền xử lý
    processed_text = preprocess(text)

    try:
        # 2. Phân loại cảm xúc
        result = nlp_pipeline(processed_text)[0]
        
        score = result['score']
        label = result['label']

        if score < 0.5:
            final_sentiment = "NEUTRAL"
        else:
            final_sentiment = LABEL_MAP.get(label, "NEUTRAL")

        return {
            "text": text,
            "sentiment": final_sentiment,
            "score": score,
            "error_message": None
        }
    except Exception as e:
        print(f"Lỗi khi phân loại pipeline: {e}", file=sys.stderr)
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": f"Lỗi khi xử lý: {e}"
        }