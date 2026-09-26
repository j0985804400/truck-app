import streamlit as st
import os
import json
try:
    from PIL import Image
    import google.generativeai as genai
except ImportError:
    pass 

def init_state():
    st.session_state['truck_l'] = 820
    st.session_state['truck_w'] = 243
    
    if 'reset_count' not in st.session_state:
        st.session_state['reset_count'] = 0
    
    st.session_state['items'] = [
        {"name": "📦 快速大箱 (約同 DPS2/IOS大)", "l": 100, "w": 95, "qty": 0, "priority": False, "required": False, "type": "quick"},
        {"name": "📦 快速中箱 (約同 UCU/ETTN)", "l": 80, "w": 75, "qty": 0, "priority": False, "required": False, "type": "quick"},
        {"name": "📦 快速小箱 (約同 EX2/WET)", "l": 65, "w": 60, "qty": 0, "priority": False, "required": False, "type": "quick"},
        
        {"name": "333", "l": 150, "w": 150, "qty": 0, "priority": True, "required": False, "type": "regular"},
        {"name": "LAM", "l": 75, "w": 116, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "EX2", "l": 60, "w": 67, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "EP2", "l": 119, "w": 67, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "WET", "l": 62, "w": 78, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "WET長箱", "l": 102, "w": 52, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "ETTN", "l": 65, "w": 95, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "DPS2", "l": 80, "w": 126, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "DPS2小", "l": 53, "w": 104, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "UCU", "l": 61, "w": 106, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "ICP", "l": 82, "w": 82, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "APC", "l": 63, "w": 63, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "IOS大", "l": 122, "w": 80, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "IOS小", "l": 102, "w": 80, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "爐管方型", "l": 70, "w": 70, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "BJM", "l": 66, "w": 125, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "辛巳大", "l": 76, "w": 56, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "辛巳小", "l": 70, "w": 46, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "SDRM", "l": 67, "w": 56, "qty": 0, "priority": False, "required": False, "type": "regular"},
        {"name": "CUP", "l": 90, "w": 56, "qty": 0, "priority": False, "required": False, "type": "regular"}
    ]

if 'items' not in st.session_state:
    init_state()

def add_temp_item():
    st.session_state['items'].append({"name": "臨時新增", "l": 50, "w": 50, "qty": 1, "priority": False, "required": False, "type": "temp"})

def reset_all():
    st.session_state['reset_count'] += 1
    for item in st.session_state['items']:
        item['qty'] = 0
        item['required'] = False

st.set_page_config(page_title="貨車裝箱防爆計算器", layout="centered")
st.title("📦 貨車裝箱防爆計算器")

st.markdown(f"<p style='color: gray; margin-bottom: 5px;'>🚚 目前車斗規格：長 {st.session_state['truck_l']} cm × 寬 {st.session_state['truck_w']} cm</p>", unsafe_allow_html=True)

r_id = st.session_state.get('reset_count', 0)
truck_area = st.session_state['truck_l'] * st.session_state['truck_w']

# ==========================================
# 📸 現場拍照與相簿上傳 AI 自動估算區
# ==========================================
st.markdown("---")
st.subheader("🤖 AI 視覺自動抓帳 (Beta)")

with st.expander("⚙️ 設定 AI 金鑰"):
    api_key = st.text_input("輸入 Gemini API Key", type="password")

upload_photo = st.file_uploader("📂 從相簿選取照片 (支援 jpg, png)", type=['jpg', 'jpeg', 'png'])
st.markdown("<p style='text-align: center; color: gray;'>或</p>", unsafe_allow_html=True)
camera_photo = st.camera_input("📸 開啟相機直接拍")

photo_to_use = upload_photo if upload_photo else camera_photo

if photo_to_use:
    if not
