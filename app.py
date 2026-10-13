import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 🔑 金鑰設定區 
# ==========================================
MY_GEMINI_KEY = "AQ.Ab8RN6JpDclBIxIRRuYny_dYSngkswnu8Nxs_kBsaVhW8PauBA"

st.set_page_config(page_title="購物雷達", page_icon="🛍️", layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {padding-top: 1rem; padding-bottom: 0rem;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🛍️ 行動購物雷達")

market_options = {
    "🇹🇼 台灣": "台灣", "🇯🇵 日本": "日本", "🇰🇷 韓國": "韓國", 
    "🇨🇳 中國": "中國", "🇭🇰 香港": "香港", "🇲🇴 澳門": "澳門",
    "🇻🇳 越南": "越南", "🇹🇭 泰國": "泰國", "🇺🇸 美國": "美國", 
    "🇸🇬 新加坡": "新加坡", "🇲🇾 馬來西亞": "馬來西亞", "🌏 其他": "其他國際地區"
}

if 'ai_valuation' not in st.session_state: st.session_state['ai_valuation'] = None
if 'camera_key' not in st.session_state: st.session_state['camera_key'] = 0

def clear_all():
    st.session_state['ai_valuation'] = None
    st.session_state['camera_key'] += 1 

# ======== 【主畫面：掃貨與精算】 ========
col_left, col_right = st.columns([1, 1.2])

with col_left:
    selected_market = st.selectbox("📍 當前地點：", list(market_options.keys()))
    
    # 保留雙軌並行：自由切換「即時相機拍照」或「上傳相簿檔案」
    input_method = st.radio("選擇圖片來源：", ["📸 即時相機拍照", "📁 從相簿/檔案上傳"], horizontal=True)
    
    target_image = None
    
    if "相機" in input_method:
        st.caption("💡 提示：若畫面預設為前鏡頭，請點擊相機上的「翻轉」圖示切換後鏡頭。")
        target_image = st.camera_input("拍照", key=f"camera_{st.session_state['camera_key']}", label_visibility="collapsed")
    else:
        target_image = st.file_uploader("選擇相片檔案", type=["jpg", "jpeg", "png", "webp"], key=f"uploader_{st.session_state['camera_key']}")

    if target_image is not None:
        if st.button("🤖 啟動閃電估價", use_container_width=True, type="primary"):
            if len(MY_GEMINI_KEY) < 20:
                st.error("請確認 API Key！")
            else:
                st.toast("📸 正在為您連線比價...", icon="🚀")
                with st.spinner("AI 跨國查價中..."):
                    try:
                        genai.configure(api_key=MY_GEMINI_KEY)
                        model_ai = genai.GenerativeModel('gemini-3.5-flash-lite')
                        
                        img = Image.open(target_image)
                        img.thumbnail((800, 800)) 
                        
                        # 回歸純粹的估價提示詞，並保留強制的換行排版規定
                        prompt = f"""
                        這是一張在【{selected_market}】拍下的商品照片。
                        請化身為專業的購物與比價達人，提供精準的估價與購買評估。
                        
                        【排版與內容最高原則】：
                        1. 全繁體中文回答，金額一律用阿拉伯數字。
                        2. 每一項【必須獨立一行】開頭，並空一行，絕對不准全部擠在同一行！
                        
                        請嚴格按照以下固定格式回覆：
                        
                        🏷️ 名稱：[商品中文名稱與核心特徵]
                        
                        💰 市價：[台灣一般零售台幣價格]
                        
                        📉 行情：[當地合理價換算之台幣金額]
                        
                        📈 建議：[是否建議入手？盤子價或划算？並簡述理由]
                        """
                        
                        config = genai.types.GenerationConfig(temperature=0.2)
                        response = model_ai.generate_content([prompt, img], generation_config=config)
                        
                        st.session_state['ai_valuation'] = response.text
                        
                    except Exception as e: 
                        st.error(f"連線擁塞請稍後再試：{e}")

with col_right:
    if st.session_state['ai_valuation']:
        st.success("✨ 估價完成！")
        with st.container(border=True):
            st.markdown(st.session_state['ai_valuation'])
        
        st.write("")
        st.button("🧹 拍下一件", use_container_width=True, on_click=clear_all)
    elif target_image is None:
        st.info("👈 請在左側選擇拍照或上傳相片。")
