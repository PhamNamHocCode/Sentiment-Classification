import streamlit as st
import database as db
import sentiment as nlp
import pandas as pd
import altair as alt

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
        st.error("Không thể tải model. Ứng dụng không thể tiếp tục.")
        st.stop()
        
# GIAO DIỆN
st.title("Phân loại Cảm xúc Tiếng Việt")
st.caption("Sử dụng PhoBERT và Streamlit")

# Bố cục giao diện
col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.subheader("Nhập câu cần phân loại:")
    
    # Form nhập câu
    with st.form(key="sentiment_form", clear_on_submit=False):
        # Ô nhập văn bản
        user_input = st.text_input(
            "Nhập câu tiếng Việt...", 
            label_visibility="collapsed", 
            placeholder="Ví dụ: Streamlit chạy chậm quá",
            key="text_input"
        )
        # Nút submit
        submit_button = st.form_submit_button("Phân loại cảm xúc", use_container_width=True)
    
    st.divider()
    
    st.subheader("Kết quả phân loại:")
    result_placeholder = st.empty()
    
    if not submit_button:
        result_placeholder.info("Vui lòng nhập một câu và nhấn nút phân loại.")

    # TEST CASE
    with st.expander("Chạy 10 Test Case"):
        st.info("Kiểm tra nhanh độ chính xác của model với 10 case.")
        run_test_cases_button = st.button("Chạy Test Cases")


# Cột Lịch sử phân loại
with col2:
    st.subheader("Lịch sử phân loại (50 mục mới nhất)")
    
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        delete_button = st.button("Xóa toàn bộ lịch sử", use_container_width=True)
    
    download_placeholder = btn_col2.empty()

    history_placeholder = st.empty()
    chart_placeholder = st.empty()

    # Tải và hiển thị lịch sử
    def display_history():
        try:
            history_df = db.load_history() 
            if not history_df.empty:
                # DATAFRAME
                if 'id' in history_df.columns:
                    display_df = history_df[["timestamp", "text", "sentiment"]].copy()
                else:
                    display_df = history_df.copy()
                    
                display_df.columns = ["Thời gian", "Nội dung", "Cảm xúc"]
                history_placeholder.dataframe(display_df, use_container_width=True)
                
                # PIE CHART
                sentiment_counts = display_df['Cảm xúc'].value_counts().reset_index()
                sentiment_counts.columns = ['Cảm xúc', 'Số lượng']
                
                pie_chart = alt.Chart(sentiment_counts).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta("Số lượng:Q", stack=True),
                    color=alt.Color("Cảm xúc:N", 
                        scale=alt.Scale(
                            domain=['POSITIVE', 'NEUTRAL', 'NEGATIVE'],
                            range=['#28a745', '#ffc107', '#dc3545']
                        ),
                        legend=alt.Legend(title="Cảm xúc")
                    ),
                    tooltip=["Cảm xúc:N", "Số lượng:Q"]
                ).properties(
                    title="Phân bố Cảm xúc",
                    width=300,
                    height=300
                )
                chart_placeholder.altair_chart(pie_chart, use_container_width=True)

                @st.cache_data
                def convert_df_to_csv(df):
                    return df.to_csv(index=False).encode('utf-8-sig')  # utf-8-sig để Excel đọc được tiếng Việt

                csv_data = convert_df_to_csv(display_df)
                
                download_placeholder.download_button(
                    label="Tải lịch sử (CSV)",
                    data=csv_data,
                    file_name="sentiment_history.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key=f"download_csv_{len(display_df)}"
                )
                
            else:
                history_placeholder.info("Chưa có lịch sử phân loại.")
                chart_placeholder.empty()
                download_placeholder.empty()

        except Exception as e:
            history_placeholder.error(f"Lỗi khi tải lịch sử: {e}")
            import traceback
            print(traceback.format_exc())

    # Hiển thị lịch sử ban đầu
    display_history()


# Backend

# Xử lý Logic khi nhấn nút phân loại
if submit_button:
    text_to_process = user_input.strip()
    
    # 1. Gọi hàm NLP
    try:
        result_dict = nlp.classify_sentiment(text_to_process)
        
        # 2. Lấy thông tin từ kết quả
        error_msg = result_dict.get('error_message')
        
        # 3. Xử lý lỗi validation
        if error_msg:
            result_placeholder.warning(f"Lỗi {error_msg}")
        
        # 4. Xử lý phân loại thành công
        else:
            sentiment = result_dict['sentiment']
            score = result_dict['score']
            
            display_text = f"Kết quả: **{sentiment}**"
            
            if sentiment == "POSITIVE":
                result_placeholder.success(f'{display_text} 😄 --- [Độ tin cậy: {score:.2%}]')
            elif sentiment == "NEGATIVE":
                result_placeholder.error(f'{display_text} 😞 --- [Độ tin cậy: {score:.2%}]')
            else:
                result_placeholder.info(f'{display_text} 😐 --- [Độ tin cậy: {score:.2%}]')

            # Lưu vào DB
            db.save_sentiment(result_dict['text'], sentiment)
            
            # Cập nhật lại lịch sử
            display_history()

    except Exception as e:
        result_placeholder.error(f"Lỗi hệ thống: {e}")
        print(f"Lỗi hệ thống khi gọi classify_sentiment: {e}")
        import traceback
        print(traceback.format_exc())

        
# Xử lý Logic khi nhấn nút Test Cases
if run_test_cases_button:
    test_cases = [
        ("Hôm nay tôi rất vui", "POSITIVE"),
        ("Món ăn này dỡ quá", "NEGATIVE"),
        ("Thời tiết bình thường", "NEUTRAL"),
        ("Rat vui hom nay", "POSITIVE"),
        ("Công việc ổn định", "NEUTRAL"),
        ("Phim này hay lắm", "POSITIVE"),
        ("Tôi buồn vì thất bại", "NEGATIVE"),
        ("Ngày mai đi học", "NEUTRAL"),
        ("Cảm ơn bạn rất nhiều", "POSITIVE"),
        ("Mệt mỏi quá hôm nay", "NEGATIVE")
    ]
    
    results = []
    correct_count = 0
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner("Đang chạy 10 Test Case..."):
        for i, (text, expected) in enumerate(test_cases):
            status_text.text(f"Đang test case {i+1}/10: {text[:30]}...")
            
            result_dict = nlp.classify_sentiment(text)
            actual = result_dict['sentiment']
            score = result_dict.get('score', 0.0)
            
            is_correct = (actual == expected)
            if is_correct:
                correct_count += 1
                
            results.append({
                "STT": i + 1,
                "Đầu vào": text,
                "Mong đợi": expected,
                "Thực tế": actual,
                "Tin cậy": f"{score:.1%}",
                "Kết quả": "Đúng" if is_correct else "Sai"
            })
            
            # Update progress
            progress_bar.progress((i + 1) / 10)
    
    status_text.empty()
    progress_bar.empty()
    
    # Hiển thị kết quả
    st.subheader(f"Kết quả Test Case: {correct_count}/10 đúng")
    
    result_df = pd.DataFrame(results)
    st.dataframe(result_df, use_container_width=True)
    
    # Đánh giá
    accuracy = (correct_count / 10)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Độ chính xác", f"{accuracy:.0%}")
    with col_b:
        st.metric("Số câu đúng", f"{correct_count}/10")
    with col_c:
        if accuracy >= 0.65:
            st.success("ĐẠT YÊU CẦU (≥65%)")
        else:
            st.error("CHƯA ĐẠT (≥65%)")


# Xử lý nút xóa lịch sử
if delete_button:
    try:
        db.clear_history()
        
        # Thông báo thành công
        st.toast("Đã xóa toàn bộ lịch sử phân loại!")
        
        # Xóa kết quả hiển thị ở cột 1
        result_placeholder.info("Vui lòng nhập một câu và nhấn nút phân loại.")
        
        # Cập nhật lại UI
        st.rerun()
        
    except Exception as e:
        st.error(f"Lỗi khi xóa lịch sử: {e}")