import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# 页面设置
st.set_page_config(page_title="康复分析平台", layout="wide")

# 多语言切换
lang = st.sidebar.selectbox("언어 선택 / 选择语言", ["한국어", "中文", "English"])

texts = {
    "한국어": {"title": "🏥 디지털 헬스케어 분석 플랫폼", "upload_data": "데이터 파일 업로드 (CSV)", "upload_media": "이미지/비디오 업로드"},
    "中文": {"title": "🏥 数字医疗分析平台", "upload_data": "上传数据文件 (CSV)", "upload_media": "上传图像/视频"},
    "English": {"title": "🏥 Digital Health Analysis Platform", "upload_data": "Upload Data (CSV)", "upload_media": "Upload Image/Video"}
}

st.title(texts[lang]["title"])

# 第一部分：数据分析
st.header("1. Data Analysis")
data_file = st.file_uploader(texts[lang]["upload_data"], type=['csv'])
if data_file:
    df = pd.read_csv(data_file)
    st.write(df.head())
    st.line_chart(df.select_dtypes(include=[np.number])) # 自动绘制数值折线图

# 第二部分：影像分析
st.header("2. Media Analysis")
media_file = st.file_uploader(texts[lang]["upload_media"], type=['jpg', 'png', 'mp4'])
if media_file:
    if media_file.type.startswith('image'):
        image = Image.open(media_file)
        st.image(image, caption='Uploaded Image')
        st.info("AI 正在分析影像特征... (이미지 분석 중)")
    else:
        st.video(media_file)
        st.info("AI 正在分析步态视频... (비디오 분석 중)")
