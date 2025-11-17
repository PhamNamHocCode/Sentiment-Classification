"""
Preprocessing - Tiền xử lý văn bản tiếng Việt
"""
import re
from underthesea import word_tokenize

# Từ điển chuẩn hóa tiếng Việt (viết tắt, thiếu dấu, slang)
NORMALIZATION_DICT = {
    # Viết tắt phổ biến
    "rat": "rất", "r": "rất",
    "k": "không", "ko": "không", "hk": "không", "kg": "không",
    "vs": "với", "v": "với",
    "dc": "được", "đc": "được",
    "mn": "mọi người",
    "hnay": "hôm nay", "hqua": "hôm qua",
    "tối": "tốt", "tot": "tốt",
    "sp": "sản phẩm",
    "sv": "sinh viên",
    "gv": "giáo viên",
    "cx": "cũng",
    "nx": "nữa",
    "j": "gì", "ji": "gì",
    "ntn": "như thế nào",
    "sao": "sao",
    "tks": "cảm ơn", "tks": "thanks", "ty": "cảm ơn",
    "sr": "sorry", "xl": "xin lỗi",
    
    # Thiếu dấu
    "dỡ": "dở", "do": "dở",
    "xau": "xấu",
    "dep": "đẹp",
    "cham": "chậm",
    "nhanh": "nhanh",
    "hay": "hay",
    "te": "tệ",
    "tam": "tạm",
    "on": "ổn",
    "kha": "khá",
    "qua": "quá", "qá": "quá",
    "lam": "lắm",
    "binh": "bình",
    "thuong": "thường",
    "vui": "vui",
    "buon": "buồn",
    "met": "mệt",
    "moi": "mỏi",
    "tuyet": "tuyệt",
    "voi": "vời",
    
    # Slang tiếng Anh
    "good": "tốt", "gud": "tốt", "nice": "tốt",
    "bad": "tệ", "terrible": "tệ",
    "ok": "ổn", "okay": "ổn",
    "love": "yêu", "like": "thích",
    "hate": "ghét",
    "happy": "vui", "sad": "buồn",
    "great": "tuyệt", "awesome": "tuyệt",
    "poor": "kém", "worst": "tệ nhất",
    "best": "tốt nhất",
    
    # Viết tắt đặc biệt
    "bt": "bình thường", "bth": "bình thường",
    "tb": "trung bình",
    "kh": "khách hàng",
    "nv": "nhân viên",
    "vc": "việc",
    "ctv": "cộng tác viên",
    
    # Từ lóng teen
    "iu": "yêu",
    "uk": "ừ",
    "uhm": "ừ",
    "oke": "ok",
    "okie": "ok",
    "thik": "thích",
    "gheh": "ghét",
    "dth": "đáng thương",
    "bik": "biết",
    "biet": "biết",
    "chưa": "chưa",
    "chua": "chưa",
    "roi": "rồi",
    "nua": "nữa",
    "wa": "quá",
    "wá": "quá",
    "lun": "luôn",
    "hix": "buồn",
    "hehe": "vui",
    "hihi": "vui"
}


def normalize_text(text):
    """
    Chuẩn hóa văn bản tiếng Việt
    
    Args:
        text (str): Câu đầu vào
        
    Returns:
        str: Câu đã chuẩn hóa
    """
    if not text:
        return ""
    
    # Chuyển chữ thường
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
    
    Args:
        text (str): Câu đã chuẩn hóa
        
    Returns:
        str: Câu đã tách từ
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
    
    Args:
        text (str): Câu gốc từ người dùng
        
    Returns:
        str: Câu đã tiền xử lý sẵn sàng cho model
    """
    # Bước 1: Chuẩn hóa
    normalized = normalize_text(text)
    
    # Bước 2: Tách từ
    tokenized = tokenize_vietnamese(normalized)
    
    return tokenized
