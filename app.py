import streamlit as st
import database as db
import sentiment as nlp

# KHỞI TẠO
# 1. Khởi tạo CSDL
try:
    db.init_db()
except Exception as e:
    st.error(f"Lỗi khi khởi tạo CSDL: {e}")
    st.stop()

# 2. Cấu hình trang
st.set_page_config(page_title="Phân loại cảm xúc", layout="wide")

# 3. Tải model NLP
with st.spinner("Đang tải model PhoBERT..."):
    if not nlp.load_model():
        st.error("Không thể tải model NLP. Ứng dụng không thể tiếp tục.")
        st.stop()
        
# GIAO DIỆN
st.title("Phân loại Cảm xúc Tiếng Việt")
st.caption("Sử dụng PhoBERT và Streamlit")

# Bố cục giao diện
col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.subheader("Nhập câu cần phân loại:")
    
    # Ô nhập văn bản
    user_input = st.text_input("Nhập câu tiếng Việt...", label_visibility="collapsed", placeholder="Ví dụ: Món ăn này dở quá")
    
    # Nút phân loại
    submit_button = st.button("Phân loại cảm xúc")
    
    st.divider()
    
    st.subheader("Kết quả phân loại:")
    result_placeholder = st.empty()
    # Hiển thị thông báo mặc định
    result_placeholder.info("Vui lòng nhập một câu và nhấn nút phân loại.")


# Cột Lịch sử phân loại
with col2:
    st.subheader("Lịch sử phân loại (50 mục mới nhất)")
    
    delete_button = st.button("Xóa toàn bộ lịch sử")
    
    history_placeholder = st.empty()
    
    def display_history():
        """
        Tải và hiển thị lịch sử từ CSDL lên placeholder.
        """
        try:
            history_df = db.load_history() 
            if not history_df.empty:
                history_df.columns = ["Thời gian", "Nội dung", "Cảm xúc"]
                history_placeholder.dataframe(history_df, use_container_width=True)
            else:
                history_placeholder.info("Chưa có lịch sử phân loại.")
        except Exception as e:
            history_placeholder.error(f"Lỗi khi tải lịch sử: {e}")

    display_history()


# Backend

# Xử lý Logic khi nhấn nút
if submit_button:
    text_to_process = user_input.strip()
    
    # 1. Gọi hàm NLP
    try:
        result_dict = nlp.classify_sentiment(text_to_process)
        
        # 2. Lấy thông tin từ kết quả
        error_msg = result_dict.get('error_message')
        
        # 3. Xử lý lỗi validation
        if error_msg:
            result_placeholder.warning(f"⚠️ {error_msg}")
        
        # 4. Xử lý phân loại thành công
        else:
            sentiment = result_dict['sentiment']
            score = result_dict['score']
            
            display_text = f"Kết quả: **{sentiment}** (Độ tin cậy: {score:.2%})"
            
            if sentiment == "POSITIVE":
                result_placeholder.success(f'{display_text} 😄')
            elif sentiment == "NEGATIVE":
                result_placeholder.error(f'{display_text} 😞')
            else:
                result_placeholder.info(f'{display_text} 😐')

            db.save_sentiment(result_dict['text'], sentiment)
            
            display_history()

    except Exception as e:
        result_placeholder.error(f"Lỗi hệ thống: {e}")
        print(f"Lỗi hệ thống khi gọi classify_sentiment: {e}")
        
if delete_button:
    try:
        db.clear_history() # 1. Gọi hàm CSDL
        display_history()  # 2. Cập nhật lại bảng lịch sử
        
        # 3. Thông báo thành công (có thể thay bằng st.toast)
        st.toast("Đã xóa toàn bộ lịch sử phân loại thành công!") 
        
        # Xóa luôn kết quả đang hiển thị ở cột 1
        result_placeholder.info("Vui lòng nhập một câu và nhấn nút phân loại.") 
        
    except Exception as e:
        st.error(f"Lỗi khi xóa lịch sử: {e}")