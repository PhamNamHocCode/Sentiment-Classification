# 🎭 Sentiment Classification - Phân loại Cảm xúc Tiếng Việt

> Ứng dụng phân loại cảm xúc (tích cực, trung tính, tiêu cực) từ văn bản tiếng Việt sử dụng PhoBERT Transformer

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Model](https://img.shields.io/badge/model-PhoBERT-orange.svg)](https://huggingface.co/wonrax/phobert-base-vietnamese-sentiment)
[![Accuracy](https://img.shields.io/badge/accuracy-%E2%89%A586.7%25-brightgreen.svg)](docs/test_results.md)

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [Cài đặt](#-cài-đặt)
- [Sử dụng](#-sử-dụng)
- [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
- [Test Cases](#-test-cases)
- [Đóng góp](#-đóng-góp)
- [Giấy phép](#-giấy-phép)

## 🎯 Giới thiệu

**Sentiment Classification** là ứng dụng desktop phân loại cảm xúc tiếng Việt được xây dựng với Python và Tkinter, tích hợp PhoBERT Transformer để phân tích cảm xúc từ văn bản tiếng Việt

### Đặc điểm nổi bật

- 🤖 **PhoBERT Transformer**: Model pre-trained đặc thù cho tiếng Việt
- 📊 **3 nhãn cảm xúc**: POSITIVE, NEUTRAL, NEGATIVE
- 🔤 **Xử lý văn bản linh hoạt**: Hỗ trợ viết tắt, thiếu dấu, slang
- 💾 **Lưu lịch sử cục bộ**: SQLite database với parameterized queries
- 🧪 **Test suite tích hợp**: 10 test cases với độ chính xác ≥65%
- 🎨 **Giao diện thân thiện**: Tkinter GUI với threading cho xử lý không đồng bộ

## ✨ Tính năng

### 1. Phân loại Cảm xúc

Nhập câu tiếng Việt tự do và nhận kết quả phân loại ngay lập tức

**Hỗ trợ:**
- ✅ Câu tiếng Việt chuẩn: "Hôm nay tôi rất vui"
- ✅ Viết tắt: "Rat vui hom nay", "k thik sp nay"
- ✅ Thiếu dấu: "Cham qua", "dep lam"
- ✅ Slang: "sp này ok", "gud", "nice"
- ✅ Độ tin cậy: Hiển thị confidence score (0-100%)

**Kết quả:**
```json
{
  "text": "Hôm nay tôi rất vui",
  "sentiment": "POSITIVE",
  "score": 0.95
}
```

### 2. Lịch sử Phân loại

- 📜 **Lưu trữ tự động**: Mỗi phân loại được lưu vào SQLite
- 🕐 **Timestamp**: Ghi lại thời gian phân loại chính xác
- 📋 **Hiển thị 50 mục**: Danh sách 50 bản ghi mới nhất
- 📥 **Tải thêm**: Nút "Tải thêm 50" để xem lịch sử cũ hơn
- 🔄 **Làm mới**: Cập nhật danh sách real-time
- 🗑️ **Xóa lịch sử**: Xóa toàn bộ với xác nhận

### 3. Test Cases Tự động

- 🧪 **10 test cases**: Kiểm tra độ chính xác model
- 📊 **Báo cáo chi tiết**: Bảng kết quả với từng case
- ✅ **Yêu cầu ≥65%**: Đánh giá đạt/không đạt
- 📈 **Confidence score**: Hiển thị độ tin cậy mỗi prediction

### 4. Tiền xử lý Văn bản

- 🔤 **Chuẩn hóa**: Lowercase, normalize spacing
- 📖 **Từ điển lớn**: 100+ từ viết tắt/slang/thiếu dấu
- 🔧 **Word tokenization**: Underthesea tokenizer
- 🎯 **Tối ưu cho PhoBERT**: Format phù hợp model input

## 🛠️ Công nghệ sử dụng

| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| **Python** | 3.8+ | Ngôn ngữ lập trình |
| **Tkinter** | Built-in | Giao diện người dùng |
| **PyTorch** | 2.0+ | Deep learning framework |
| **Transformers** | 4.30+ | Hugging Face pipeline |
| **PhoBERT** | phobert-base | Model phân loại cảm xúc |
| **underthesea** | 1.3.5+ | Tokenization tiếng Việt |
| **SQLite3** | Built-in | Cơ sở dữ liệu |

## 📦 Cài đặt

### Yêu cầu hệ thống

- Python 3.8 hoặc cao hơn
- Windows 10/11, macOS 10.15+, hoặc Linux
- 2GB RAM khả dụng (cho PhoBERT model)
- Kết nối internet (lần đầu tải model)

### Hướng dẫn cài đặt

**1. Clone repository**

```bash
git clone https://github.com/yourusername/sentiment-classification.git
cd sentiment-classification
```

**2. Tạo môi trường ảo (khuyến nghị)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Cài đặt dependencies**

```bash
pip install -r requirements.txt
```

**Lưu ý:** Lần đầu chạy sẽ tự động tải PhoBERT model (~1GB) từ Hugging Face

**4. Chạy ứng dụng**

```bash
python app.py
```

## 🚀 Sử dụng

### Khởi động ứng dụng

```bash
python app.py
```

### Giao diện chính

```
┌───────────────────────────────────────────────────────────────┐
│  📝 BÊN TRÁI: Input                   📊 BÊN PHẢI: Lịch sử   │
├───────────────────────────────────────────────────────────────┤
│                                                                 │
│  Nhập câu:                            ID | Thời gian | Câu   │
│  ┌─────────────────────────┐          ──────────────────────── │
│  │ Hôm nay tôi rất vui     │          1  | 14:30:25  | Hôm..│
│  └─────────────────────────┘          2  | 14:29:10  | Món..│
│  [🔍 Phân loại cảm xúc]               3  | 14:28:05  | Thời│
│                                                                 │
│  Kết quả:                             [🔄 Làm mới DS]         │
│  ┌─────────────────────────┐          [📥 Tải thêm 50]       │
│  │   😄 POSITIVE            │          [🗑️ Xóa lịch sử]      │
│  │   (Tin cậy: 95%)        │                                  │
│  └─────────────────────────┘                                  │
│                                                                 │
│  [🧪 Chạy 10 Test Cases]                                      │
└───────────────────────────────────────────────────────────────┘
```

### Ví dụ sử dụng

**Ví dụ 1: Phân loại câu chuẩn**
```
Input:  "Hôm nay tôi rất vui"
Output: 😄 POSITIVE (Tin cậy: 95.2%)
```

**Ví dụ 2: Viết tắt + thiếu dấu**
```
Input:  "Rat vui hom nay"
Output: 😄 POSITIVE (Tin cậy: 92.1%)
→ Đã chuẩn hóa: "Rất vui hôm nay"
```

**Ví dụ 3: Slang tiếng Anh**
```
Input:  "Sp nay gud lam"
Output: 😄 POSITIVE (Tin cậy: 88.5%)
→ Đã chuẩn hóa: "Sản phẩm này tốt lắm"
```

**Ví dụ 4: Câu trung tính**
```
Input:  "Thời tiết bình thường"
Output: 😐 NEUTRAL (Tin cậy: 78.3%)
```

**Ví dụ 5: Câu tiêu cực**
```
Input:  "Mệt mỏi quá hôm nay"
Output: 😞 NEGATIVE (Tin cậy: 91.7%)
```

## 🏗️ Kiến trúc hệ thống

### Cấu trúc thư mục

```
Sentiment-Classification/
├── app.py                          # Entry point
├── src/
│   ├── __init__.py
│   ├── core/                       # Business logic
│   │   ├── database.py             # SQLite operations
│   │   ├── sentiment.py            # PhoBERT classification
│   │   └── preprocessing.py        # Text normalization
│   └── ui/                         # User interface
│       ├── main_window.py          # Tkinter main window
│       └── test_dialog.py          # Test cases dialog
├── requirements.txt                # Dependencies
├── sentiment.db                    # SQLite database (auto-gen)
├── app_streamlit_backup.py         # Streamlit version backup
└── README.md                       # Documentation
```

### Pipeline xử lý

```
┌─────────────────────────────────────────────────┐
│ 1. INPUT VALIDATION                             │
│    - Kiểm tra độ dài (≥5 ký tự)                │
│    - Kiểm tra chứa chữ cái                     │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ 2. PREPROCESSING                                │
│    - Normalize: lowercase, spacing              │
│    - Dictionary: viết tắt → từ đầy đủ          │
│    - Tokenization: underthesea                  │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ 3. PHOBERT CLASSIFICATION                       │
│    - Pipeline: sentiment-analysis               │
│    - Model: wonrax/phobert-base-vietnamese      │
│    - Output: label + confidence score           │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ 4. POST-PROCESSING                              │
│    - Threshold: score < 0.5 → NEUTRAL          │
│    - Mapping: POS/NEG/NEU → POSITIVE/etc       │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ 5. SAVE & DISPLAY                               │
│    - Save to SQLite                             │
│    - Update UI (main thread)                    │
└─────────────────────────────────────────────────┘
```

### Database Schema

```sql
CREATE TABLE sentiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    sentiment TEXT NOT NULL,  -- POSITIVE/NEUTRAL/NEGATIVE
    timestamp TEXT NOT NULL   -- YYYY-MM-DD HH:MM:SS
);
```

### Threading Model

```
┌──────────────────────────────────────────┐
│ MAIN THREAD (Tkinter UI)                 │
│  - Render GUI                            │
│  - Handle events                         │
│  - Update display                        │
└────────────┬─────────────────────────────┘
             │
             ├─> WORKER THREAD 1
             │   - PhoBERT classification
             │   - Long-running task
             │
             └─> WORKER THREAD 2
                 - Test cases execution
                 - Parallel processing
```

## 🧪 Test Cases

### 10 Test Cases chuẩn

| STT | Đầu vào | Mong đợi | Mô tả |
|-----|---------|----------|-------|
| 1 | Hôm nay tôi rất vui | POSITIVE | Câu chuẩn tích cực |
| 2 | Món ăn này dỡ quá | NEGATIVE | Câu chuẩn tiêu cực |
| 3 | Thời tiết bình thường | NEUTRAL | Câu trung tính |
| 4 | Rat vui hom nay | POSITIVE | Viết tắt + thiếu dấu |
| 5 | Công việc ổn định | NEUTRAL | Trung tính |
| 6 | Phim này hay lắm | POSITIVE | Tích cực |
| 7 | Tôi buồn vì thất bại | NEGATIVE | Tiêu cực rõ ràng |
| 8 | Ngày mai đi học | NEUTRAL | Câu phát biểu |
| 9 | Cảm ơn bạn rất nhiều | POSITIVE | Lời cảm ơn |
| 10 | Mệt mỏi quá hôm nay | NEGATIVE | Tiêu cực |

### Chạy test

1. Mở ứng dụng
2. Click nút "🧪 Chạy 10 Test Cases"
3. Xem kết quả trong dialog

**Kết quả mong đợi:**
```
✅ Passed: ≥6.5/10 cases
✅ Accuracy: ≥65%
✅ ĐẠT YÊU CẦU
```

## 🔒 Bảo mật

### SQL Injection Prevention

```python
# ❌ Không an toàn
cursor.execute(f"INSERT INTO sentiments VALUES ('{text}')")

# ✅ An toàn - Parameterized queries
cursor.execute("INSERT INTO sentiments VALUES (?, ?, ?)", (text, sentiment, timestamp))
```

### Thread Safety

```python
# ✅ Cập nhật UI từ main thread
self.root.after(0, self._update_result, result)
```

## 📝 Đóng góp

Mọi đóng góp đều được hoan nghênh

1. Fork repository
2. Tạo branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📄 Giấy phép

Dự án này được tạo cho mục đích học tập (Seminar chuyên đề)

## 👥 Tác giả

**Sinh viên thực hiện**
- Họ tên: [Tên của bạn]
- MSSV: [Mã số sinh viên]
- Lớp: [Mã lớp]
- Trường: Đại học Sài Gòn (SGU)

**Giảng viên hướng dẫn**
- [Tên giảng viên]

## 📞 Liên hệ

- 📧 Email: [your.email@example.com]
- 🐙 GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Lời cảm ơn

- [Hugging Face Transformers](https://huggingface.co/transformers/) - Pipeline framework
- [PhoBERT](https://github.com/VinAIResearch/PhoBERT) - Vietnamese pre-trained model
- [Underthesea](https://github.com/undertheseanlp/underthesea) - Vietnamese NLP toolkit
- [wonrax/phobert-base-vietnamese-sentiment](https://huggingface.co/wonrax/phobert-base-vietnamese-sentiment) - Fine-tuned sentiment model

---

<p align="center">
  Made with ❤️ for Vietnamese NLP<br>
  ⭐ Star this repo if you find it helpful
</p>
