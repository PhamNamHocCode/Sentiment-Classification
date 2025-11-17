"""
Sentiment Analysis - Phân loại cảm xúc tiếng Việt sử dụng PhoBERT
"""
from transformers import pipeline
from src.core.preprocessing import preprocess

# Cấu hình model
MODEL_NAME = "wonrax/phobert-base-vietnamese-sentiment"

# Mapping nhãn model -> nhãn yêu cầu
LABEL_MAP = {
    "POS": "POSITIVE",
    "NEG": "NEGATIVE", 
    "NEU": "NEUTRAL"
}

# Cache model toàn cục
_nlp_pipeline = None


def load_model():
    """
    Tải PhoBERT pipeline và cache lại
    
    Returns:
        pipeline: Hugging Face sentiment-analysis pipeline
    """
    global _nlp_pipeline
    
    if _nlp_pipeline is not None:
        return _nlp_pipeline
    
    try:
        print("Đang tải PhoBERT model")
        _nlp_pipeline = pipeline('sentiment-analysis', model=MODEL_NAME)
        print("Tải model thành công")
        return _nlp_pipeline
    except Exception as e:
        print(f"Lỗi tải model: {e}")
        return None


def classify_sentiment(text):
    """
    Phân loại cảm xúc từ câu tiếng Việt
    
    Args:
        text (str): Câu gốc từ người dùng
        
    Returns:
        dict: {
            "text": str,
            "sentiment": str (POSITIVE/NEUTRAL/NEGATIVE),
            "score": float (0-1),
            "error_message": str hoặc None
        }
    """
    # Validation 1: Kiểm tra độ dài
    if not text or len(text.strip()) < 5:
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": "Câu không hợp lệ (yêu cầu ≥ 5 ký tự)"
        }
    
    # Validation 2: Phải chứa ký tự chữ
    if not any(c.isalpha() for c in text):
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": "Câu không hợp lệ (phải chứa ký tự chữ)"
        }
    
    # Giới hạn độ dài tối đa 200 ký tự
    if len(text) > 200:
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": "Câu quá dài (tối đa 200 ký tự)"
        }
    
    # Load model
    nlp_pipeline = load_model()
    if nlp_pipeline is None:
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": "Lỗi tải model NLP"
        }
    
    try:
        # Bước 1: Tiền xử lý
        processed_text = preprocess(text)
        
        # Bước 2: Phân loại qua pipeline
        result = nlp_pipeline(processed_text)[0]
        
        score = result['score']
        label = result['label']
        
        # Bước 3: Ánh xạ nhãn và xử lý ngưỡng
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
        print(f"Lỗi phân loại: {e}")
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": f"Lỗi xử lý: {str(e)}"
        }
