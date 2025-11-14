import streamlit as st
import database as db
import sentiment as nlp

# Khởi tạo 
db.init_db()

st.set_page_config(page_title="Phân loại ảm xúc", layout="wide")
st.title("Phân loại cảm xúc")
st.caption("Sử dụng PhoBERT và Streamlit")

#  Bố cục giao diện
col1, col2 = st.columns([0.6, 0.4])
with col1:
    st.subheader("Nhập câu cần phân loại:")
    
    user_input = st.text_input("Nhập câu tiếng Việt...", label_visibility="collapsed")
    
    submit_button = st.button("Phân loại cảm xúc")
    
    st.divider()
    
    st.subheader("Kết quả phân loại:")
    result_placeholder = st.empty()
    result_placeholder.info("Vui lòng nhập một câu và nhấn nút phân loại.")


# Lịch sử phân loại 
with col2:
    st.subheader("Lịch sử phân loại (50 mục mới nhất)")
    
    history_placeholder = st.empty()
    
    def display_history():
        """Tải và hiển thị lịch sử từ CSDL lên placeholder"""
        history_df = db.load_history()
        if not history_df.empty:
            # Đổi tên cột cho thân thiện với người dùng
            history_df.columns = ["Thời gian", "Nội dung", "Cảm xúc"]
            history_placeholder.dataframe(history_df, use_container_width=True)
        else:
            history_placeholder.info("Chưa có lịch sử phân loại.")

    display_history()


#  Xử lý Logic khi nhấn nút 
if submit_button:
    # 1. Validate đầu vào
    text_to_process = user_input.strip()
    
    if len(text_to_process) < 5:
        result_placeholder.error("Câu không hợp lệ! Yêu cầu nhập ít nhất 5 ký tự.")
    
    else:
        # 2. Gọi NLP
        try:
            result_dict = nlp.classify_sentiment(text_to_process)
            sentiment = result_dict.get("sentiment", "LỖI")

            # 3. Hiển thị kết quả
            if sentiment == "POSITIVE":
                result_placeholder.success(f'Kết quả: TÍCH CỰC (POSITIVE) 😄')
            elif sentiment == "NEGATIVE":
                result_placeholder.error(f'Kết quả: TIÊU CỰC (NEGATIVE) 😞')
            else:
                result_placeholder.info(f'Kết quả: TRUNG TÍNH (NEUTRAL) 😐')

            # 4. Lưu vào CSDL
            db.save_sentiment(text_to_process, sentiment)
            
            # 5. Cập nhật lại bảng lịch sử
            display_history()

        except Exception as e:
            result_placeholder.error(f"Đã xảy ra lỗi trong quá trình xử lý: {e}")