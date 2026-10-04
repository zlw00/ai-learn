import streamlit as st

fruit = st.selectbox("请选择水果", ["苹果", "香蕉", "橙子"])
st.write("你选的是：", fruit)
