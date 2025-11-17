"""
Preprocessing - Tiền xử lý văn bản tiếng Việt
"""
import re
from underthesea import word_tokenize

# Từ điển chuẩn hóa tiếng Việt (viết tắt, thiếu dấu, slang)
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
    "vui": "vui",
    "hay": "hay",
    "good": "tốt",
    "hqua": "hôm qua",
    "dang": "đang",
    "den": "đến",
    "di": "đi",
    "roi": "rồi",
    "chua": "chưa",
    "nua": "nữa",
    "thik": "thích",
    "ghét": "ghét",
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


def normalize_text(text):
    """
    Chuẩn hóa văn bản tiếng Việt
    """
    if not text:
        return ""
    
    text = text.lower().strip()
    
    # Thay thế từ viết tắt/thiếu dấu bằng từ điển
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


def preprocess(text):
    """
    Pipeline tiền xử lý đầy đủ
    """
    normalized = normalize_text(text)
    
    tokenized = tokenize_vietnamese(normalized)
    
    return tokenized
