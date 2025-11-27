from transformers import pipeline
from src.core.preprocessing import preprocess, calculate_rule_based_score

# Model: https://huggingface.co/wonrax/phobert-base-vietnamese-sentiment
MODEL_NAME = "wonrax/phobert-base-vietnamese-sentiment"

LABEL_MAP = {
    "POS": "POSITIVE",
    "NEG": "NEGATIVE", 
    "NEU": "NEUTRAL"
}

nlp_pipeline = None

def load_model():
    """
    Tải model PhoBERT
    """
    global nlp_pipeline
    
    if nlp_pipeline is not None:
        return nlp_pipeline
    
    try:
        print("Đang tải PhoBERT model")
        nlp_pipeline = pipeline('sentiment-analysis', model=MODEL_NAME)
        print("Tải model thành công")
        return nlp_pipeline
    except Exception as e:
        print(f"Lỗi tải model: {e}")
        return None

def classify_sentiment(text):
    # Validation 1: Kiểm tra độ dài
    if not text or len(text.strip()) < 5:
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": "Câu không hợp lệ (yêu cầu ≥ 5 ký tự)"
        }
    
    # Validation 2: Phải chứa ký tự chữ
    if not any(word.isalpha() for word in text):
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": "Câu không hợp lệ (phải chứa ký tự chữ)"
        }
    
    # Giới hạn độ dài tối đa 50 ký tự
    if len(text) > 50:
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": "Câu quá dài (tối đa 50 ký tự)"
        }
    
    # Load model
    nlp_pipeline = load_model()
    if nlp_pipeline is None:
        return {
            "text": text,
            "sentiment": None,
            "score": 0.0,
            "error_message": "Lỗi tải model"
        }
    
    try:
        # Bước 1: Tính rule-based score
        rule_sentiment, rule_confidence = calculate_rule_based_score(text)
        
        # Bước 2: Tiền xử lý
        processed_text = preprocess(text)
        
        # Bước 3: Phân loại qua pipeline
        result = nlp_pipeline(processed_text)[0]
        
        model_score = result['score']
        model_label = result['label']
        model_sentiment = LABEL_MAP.get(model_label, "NEUTRAL")
        
        # Bước 4: Kết hợp model + rule-based Hybrid
        # Ưu tiên rule-based nếu có confidence cao
        if rule_sentiment and rule_confidence > 0.6:
            final_sentiment = rule_sentiment
            final_score = rule_confidence
        # Nếu model confident >0.7 thì dùng model
        elif model_score > 0.7:
            final_sentiment = model_sentiment
            final_score = model_score
        # Kết hợp khi cả 2 đêu không chắc chắn
        elif rule_sentiment:
            # Khi cả 2 có cùng quan điểm
            if rule_sentiment == model_sentiment:
                final_sentiment = rule_sentiment
                final_score = (rule_confidence * 0.6 + model_score * 0.4)
            else:
                # Ưu tiên rule-based khi có xung đột
                final_sentiment = rule_sentiment
                final_score = rule_confidence * 0.8
        else:
            # Trường hợp không tìm thấy keywords nào rule_sentiment = None nên sẽ phân loại theo model
            if model_score < 0.5:
                # Nếu model cũng không chắc chắn thì chọn NEUTRAL
                final_sentiment = "NEUTRAL"
            else:
                # Model chắc chắn thì dùng kết quả model
                final_sentiment = model_sentiment
            final_score = model_score
        
        return {
            "text": text,
            "sentiment": final_sentiment,
            "score": final_score,
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
