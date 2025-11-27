from transformers import pipeline

# 1. Cấu hình Pipeline (Theo Mục VII.1)
# Lưu ý: Cần mapping label ID của PhoBERT sang POSITIVE/NEUTRAL/NEGATIVE
sentiment_pipeline = pipeline("sentiment-analysis", model="vinai/phobert-base-v2")

# 2. Danh sách Test Cases (Theo Mục VIII)
TEST_CASES = [
    {"text": "Hôm nay tôi rất vui", "expected": "POSITIVE"},
    {"text": "Món ăn này dỡ quá", "expected": "NEGATIVE"},
    {"text": "Thời tiết bình thường", "expected": "NEUTRAL"},
    # ... thêm đủ 10 câu từ Mục VIII
]

def run_test_cases():
    results = []
    pass_count = 0
    
    print(f"{'Câu Input':<30} | {'Thực tế':<10} | {'Mong đợi':<10} | {'Kết quả':<5}")
    print("-" * 65)

    for case in TEST_CASES:
        text = case["text"]
        expected = case["expected"]
        final_label = ""

        # Bước Tiền xử lý & Kiểm tra độ dài (Node E, F)
        if len(text) < 5:
            final_label = "ERROR"
        else:
            # Bước Phân loại (Node H)
            output = sentiment_pipeline(text)[0]
            score = output['score']
            label_id = output['label'] # Ví dụ: LABEL_0, LABEL_1
            
            # TODO: Cần mapping chính xác label_id sang POSITIVE, NEGATIVE, NEUTRAL
            # Ví dụ giả định mapping (cần kiểm tra lại với model cụ thể):
            label_map = {"LABEL_0": "NEGATIVE", "LABEL_1": "NEUTRAL", "LABEL_2": "POSITIVE"}
            predicted_label = label_map.get(label_id, "UNKNOWN")

            # Logic Score < 0.5 (Node I, J, K)
            if score < 0.5:
                final_label = "NEUTRAL"
            else:
                final_label = predicted_label
        
        # So sánh (Node L, M)
        status = "PASS" if final_label == expected else "expected"
        if status == "PASS":
            pass_count += 1
            
        print(f"{text:<30} | {final_label:<10} | {expected:<10} | {status:<5}")

    # Tính độ chính xác (Node N)
    accuracy = (pass_count / len(TEST_CASES)) * 100
    print("-" * 65)
    print(f"Độ chính xác: {accuracy:.2f}%")
    if accuracy >= 65:
        print("Đánh giá: ĐẠT yêu cầu (>= 65%)")
    else:
        print("Đánh giá: CHƯA ĐẠT yêu cầu (< 65%)")

# Để chạy thử, bạn cần bỏ comment dòng này khi đã cấu hình xong môi trường và mapping
run_test_cases()