# 🎭 Phân loại Cảm xúc Tiếng Việt

Ứng dụng phân loại cảm xúc văn bản tiếng Việt sử dụng PhoBERT Transformer

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Model](https://img.shields.io/badge/model-PhoBERT-orange.svg)](https://huggingface.co/wonrax/phobert-base-vietnamese-sentiment)
[![Accuracy](https://img.shields.io/badge/accuracy->85%25-brightgreen.svg)](#test-cases)

## 📋 Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Công nghệ](#công-nghệ)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [Kiến trúc](#kiến-trúc)
- [Test Cases](#test-cases)

## Giới thiệu

Ứng dụng desktop phân loại cảm xúc tiếng Việt sử dụng **Hybrid Approach**: kết hợp PhoBERT Transformer và Rule-based Sentiment Analysis. Nhận câu tiếng Việt và trả về nhãn cảm xúc: POSITIVE, NEUTRAL, NEGATIVE

### Đặc điểm

- **Hybrid Model**: PhoBERT + Rule-based keywords (>85% accuracy)
- **3 từ điển keywords**: 40+ POSITIVE, 35+ NEGATIVE, 16 NEUTRAL
- Xử lý viết tắt, thiếu dấu, slang (40+ từ)
- Lưu lịch sử SQLite với parameterized queries
- 10 test cases tích hợp (đạt >85% accuracy)
- Giao diện Tkinter với threading

## Tính năng

### Phân loại cảm xúc

Nhập câu tiếng Việt và nhận kết quả phân loại

Hỗ trợ:
- Câu chuẩn: "Hôm nay tôi rất vui"
- Thiếu dấu: "dep lam"
- Viết tắt: "sp ok", "gud"

Kết quả:
```json
{
  "text": "Hôm nay tôi rất vui",
  "sentiment": "POSITIVE"
}
```

### Lịch sử

- Lưu tự động vào SQLite
- Hiển thị 50 bản ghi mới nhất
- Nút "Tải thêm 50"
- Làm mới và xóa lịch sử

### Test Cases

- 10 test cases tích hợp
- Báo cáo chi tiết
- Yêu cầu ≥65% accuracy

### Tiền xử lý & Rule-based

- **3 từ điển keywords**:
  - POSITIVE: 40+ từ (tốt, hay, đẹp, vui, dễ, dễ dàng, tuyệt...)
  - NEGATIVE: 35+ từ (khó, khó quá, xấu, dở, tệ, buồn, thất bại...)
  - NEUTRAL: 16 từ (bình thường, tạm, ổn định...)
- Chuẩn hóa: lowercase, spacing
- Từ điển 40 từ viết tắt, không dấu
- Tokenization với underthesea
- **Rule-based scoring** với confidence calculation

## Công nghệ

| Công nghệ | Phiên bản | Mô tả |
|-----------|-----------|-------|
| Python | 3.8+ | Ngôn ngữ chính |
| Tkinter | Built-in | Giao diện |
| PyTorch | 2.0+ | Deep learning |
| Transformers | 4.30+ | Hugging Face |
| PhoBERT | wonrax/phobert-base-vietnamese-sentiment | Model sentiment |
| underthesea | 1.3.5+ | Tokenization |
| SQLite3 | Built-in | Database |

## Cài đặt

### Yêu cầu

- Python 3.8+
- 2GB RAM (cho PhoBERT)
- Kết nối internet (lần đầu)

### Cài đặt

```bash
# Clone repository
git clone <repo-url>
cd sentiment-classification

# Cài dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python app.py
```

Lần đầu chạy sẽ tải PhoBERT model (~1GB)

## Sử dụng

### Khởi động

```bash
python app.py
```

### Ví dụ

**Câu chuẩn**
```
Input:  "Hôm nay tôi rất vui"
Output: 😄 POSITIVE
```

**Viết tắt**
```
Input:  "Rat vui hom nay"
Output: 😄 POSITIVE
```

**Slang**
```
Input:  "Sp nay gud lam"
Output: 😄 POSITIVE
```

**Trung tính**
```
Input:  "Thời tiết bình thường"
Output: 😐 NEUTRAL
```

**Tiêu cực**
```
Input:  "Mệt mỏi quá hôm nay"
Output: 😞 NEGATIVE
```

## Kiến trúc

### Cấu trúc

```
Sentiment-Classification/
├── app.py
├── src/
│   ├── core/
│   │   ├── database.py
│   │   ├── sentiment.py
│   │   └── preprocessing.py
│   └── ui/
│       ├── main_window.py
│       └── test_dialog.py
├── requirements.txt
└── sentiment.db
```

### Pipeline

```
Input → Validation → Rule-based Score → Preprocessing → PhoBERT → Hybrid Combine → Save & Display
```

Chi tiết:
1. **Validation**: kiểm tra độ dài ≥5 ký tự, ≤50 ký tự
2. **Rule-based Score**: đếm keywords và tính confidence
3. **Preprocessing**: normalize + tokenize
4. **PhoBERT**: sentiment-analysis pipeline
5. **Hybrid Combine**:
   - Ưu tiên rule-based nếu confidence > 0.6
   - Dùng model nếu score > 0.7
   - Weighted average (60% rule + 40% model) khi conflict
   - Fallback NEUTRAL nếu không confident
6. **Save**: SQLite với parameterized queries

### Hybrid Approach

**Tại sao kết hợp Rule-based + Model?**

PhoBERT model đạt ~65% accuracy vì:
- Training data từ reviews (sản phẩm, phim)
- Không hiểu context kỹ thuật (VD: "Python khó quá")
- Bị bias với từ "quá" (thường đi với positive)

**Giải pháp Hybrid**:
```python
# Rule-based catch: "khó", "khó quá" → NEGATIVE
# Model catch: "tuyệt vời", "xuất sắc" → POSITIVE
# Combine: Tăng accuracy lên >85%
```

**Ưu tiên**:
1. Rule-based confidence > 0.6 → Chính xác với keywords rõ ràng
2. Model score > 0.7 → Tin model khi confident
3. Weighted combine → Cân bằng khi conflict

### Database

```sql
CREATE TABLE sentiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    sentiment TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
```

### Threading

- Main thread: Tkinter UI
- Worker threads: PhoBERT classification, test cases
- Thread-safe UI update với `root.after()`

## Test Cases

### 10 test cases

| STT | Đầu vào | Mong đợi |
|-----|---------|----------|
| 1 | Hôm nay tôi rất vui | POSITIVE |
| 2 | Món ăn này dỡ quá* | NEGATIVE |
| 3 | Thời tiết bình thường | NEUTRAL |
| 4 | Rat vui hom nay | POSITIVE |
| 5 | Công việc ổn định | NEUTRAL |
| 6 | Phim này hay lắm | POSITIVE |
| 7 | Tôi buồn vì thất bại | NEGATIVE |
| 8 | Ngày mai đi học | NEUTRAL |
| 9 | Cảm ơn bạn rất nhiều | POSITIVE |
| 10 | Mệt mỏi quá hôm nay | NEGATIVE |

**Ghi chú**: *Test case 2 cố ý viết sai "dỡ" thay vì "dở" để kiểm tra khả năng xử lý typo của model.

### Chạy test

1. Mở ứng dụng
2. Click "Chạy 10 Test Cases"
3. Xem kết quả

Kết quả:
- **Yêu cầu**: ≥6.5/10 đúng (≥65% accuracy)
- **Đạt được**: >8.5/10 đúng (>85% accuracy) với Hybrid approach

### Ví dụ cải thiện

| Câu | Model only | Hybrid | Đúng |
|-----|-----------|--------|------|
| Python khó quá | POSITIVE ❌ | NEGATIVE ✅ | ✅ |
| Python dễ quá | NEUTRAL ❌ | POSITIVE ✅ | ✅ |
| Món ăn này dở quá | NEGATIVE ✅ | NEGATIVE ✅ | ✅ |
| Hôm nay tôi rất vui | POSITIVE ✅ | POSITIVE ✅ | ✅ |

## Bảo mật

### SQL Injection Prevention

```python
# Sử dụng parameterized queries
cursor.execute("INSERT INTO sentiments VALUES (?, ?, ?)", 
               (text, sentiment, timestamp))
```

### Thread Safety

```python
# Cập nhật UI từ main thread
self.root.after(0, self._update_result, result)
```

---

**Seminar chuyên đề - Đại học Sài Gòn (SGU)**
