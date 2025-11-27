"""
Preprocessing - Tiền xử lý
"""
import re
from underthesea import word_tokenize

# Từ điển chuẩn hóa tiếng Việt viết tắt, thiếu dấu
NORMALIZATION_DICT = {
    "rat": "rất",
    "k": "không",
    "ko": "không",
    "vs": "với",
    "dc": "được",
    "hnay": "hôm nay",
    "tot": "tốt",
    "do": "dở",
    "xau": "xấu",
    "dep": "đẹp",
    "te": "tệ",
    "on": "ổn",
    "qua": "quá",
    "lam": "lắm",
    "buon": "buồn",
    "met": "mệt",
    "good": "tốt",
    "hqua": "hôm qua",
    "den": "đến",
    "di": "đi",
    "roi": "rồi",
    "nua": "nữa",
    "thik": "thích",
    "iu": "yêu",
    "ok": "ổn",
    "wa": "quá",
    "lun": "luôn",
    "cx": "cũng",
    "nx": "nữa",
    "mn": "mọi người",
    "tks": "cảm ơn",
    "ty": "cảm ơn",
    "xl": "xin lỗi",
    "tam": "tạm"
}

# Từ điển keywords tích cực
POSITIVE_KEYWORDS = {
    "tốt", "hay", "đẹp", "vui", "thích", "yêu", "tuyệt", "xuất sắc",
    "hoàn hảo", "tuyệt vời", "hài lòng", "hạnh phúc", "cảm ơn", "cám ơn",
    "tích cực", "ok", "good", "nice", "love", "like", "ưng",
    "thích thú", "vừa ý", "ưng ý", "hợp lý", "bổ ích", "thành công",
    "vui vẻ", "sướng", "thoải mái", "dễ chịu", "dễ", "dễ dàng", "đơn giản",
    "dễ hiểu", "rõ ràng", "tốt lắm", "hay lắm"
}

# Từ điển keywords tiêu cực
NEGATIVE_KEYWORDS = {
    "xấu", "dở", "tệ", "buồn", "ghét", "mệt", "khó", "thất bại",
    "tồi tệ", "kinh khủng", "khủng khiếp", "chán", "nhàm chán",
    "không tốt", "không hay", "tệ hại", "xin lỗi", "tiếc", "đau",
    "đau khổ", "tồi", "kém", "thất vọng", "thảm hại", "cực",
    "tức", "giận", "bực", "bực mình", "phiền", "khó chịu", "tệ quá",
    "khó quá", "mệt mỏi", "căng thẳng", "stress", "áp lực", "khủng khiếp",
    "tồi", "dở ẹc", "dở tệ", "tệ hại", "kinh khủng"
}

# Từ điển keywords trung tính
NEUTRAL_KEYWORDS = {
    "bình thường", "thường", "tạm", "được", "cũng được", "tạm ổn",
    "ổn định", "ổn", "thông thường", "bình thường thôi", "không sao",
    "ngày mai", "hôm nay", "hôm qua", "đi", "học", "làm việc", "công việc"
}


def normalize_text(text):
    """
    Chuẩn hóa
    """
    if not text:
        return ""
    
    text = text.lower().strip()
    
    # Thay thế từ viết tắt, thiếu dấu bằng NORMALIZATION_DICT
    # Sử dụng word boundary \b để tránh thay thế nhầm
    for key, value in NORMALIZATION_DICT.items():
        pattern = r'\b' + re.escape(key) + r'\b'
        text = re.sub(pattern, value, text)
    
    return text


def tokenize_vietnamese(text):
    """
    Tách từ tiếng Việt sử dụng underthesea
    """
    try:
        tokenized = word_tokenize(text, format="text")
        return tokenized
    except Exception as e:
        print(f"Lỗi word_tokenize: {e} Sử dụng text gốc")
        return text


def calculate_rule_based_score(text):
    """
    Tính điểm sentiment dựa trên keywords (rule-based)
    Trả về: (sentiment, confidence)
    """
    text_lower = text.lower()
    
    pos_count = sum(1 for keyword in POSITIVE_KEYWORDS if keyword in text_lower)
    neg_count = sum(1 for keyword in NEGATIVE_KEYWORDS if keyword in text_lower)
    neu_count = sum(1 for keyword in NEUTRAL_KEYWORDS if keyword in text_lower)
    
    total = pos_count + neg_count + neu_count
    
    if total == 0:
        return None, 0.0
    
    # Tính confidence dựa trên tỷ lệ keyword match
    if pos_count > neg_count and pos_count > neu_count:
        confidence = pos_count / total
        return "POSITIVE", confidence
    elif neg_count > pos_count and neg_count > neu_count:
        confidence = neg_count / total
        return "NEGATIVE", confidence
    else:
        confidence = neu_count / total if neu_count > 0 else 0.3
        return "NEUTRAL", confidence


def preprocess(text):
    """
    Pipeline tiền xử lý
    """
    normalized = normalize_text(text)
    
    tokenized = tokenize_vietnamese(normalized)
    
    return tokenized
