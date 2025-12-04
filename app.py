import streamlit as st
import google.generativeai as genai
from PIL import Image

# 設定網頁標題
st.title("👨‍⚕️ 放射科 AI 助理")

# 側邊欄：輸入 API Key
api_key = st.sidebar.text_input("輸入 Google API Key", type="password")

# 圖片上傳區
uploaded_file = st.file_uploader("上傳 X光/CT/MRI 影像", type=["jpg", "png", "jpeg"])

# 文字輸入區
prompt = st.text_area("輸入指令 (例如：請描述這張圖的異常處)", value="請以放射科醫師的角度，條列式描述這張影像的發現。")

# 按鈕
if st.button("開始分析"):
    if not api_key:
        st.error("⚠️ 請先在左側輸入 API Key")
    elif not uploaded_file:
        st.warning("⚠️ 請上傳一張圖片")
    else:
        try:
            # 設定 AI
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 處理圖片
            image = Image.open(uploaded_file)
            st.image(image, caption='已上傳的影像', use_column_width=True)
            
            with st.spinner('AI 正在判讀影像中...'):
                response = model.generate_content([prompt, image])
                
            st.success("分析完成！")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"發生錯誤：{e}")
