import streamlit as st
from sent_clasfi import preprocess

def user_input():
    user_input = st.text_input('Enter your sentence:')
    
    return user_input

submit = st.button('Classify Sentiment')

if submit:
    
    st.write(f'Sentiment classification result for "{input}" is {preprocess(user_input)}')