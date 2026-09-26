import streamlit as st
import os
import json
import base64
import requests
from PIL import Image

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

with st.expander("⚙️ 設定 AI 金鑰 (必填)"):
    api_key = st.text_input("輸入全新的 Gemini API Key", type="password")
    st.markdown("[按此免費申請新的 Google Gemini API Key](https://aistudio.google.com/app/apikey)")

upload_photo = st.file_uploader("📂 從相簿選取照片 (支援 jpg, png)", type=['jpg', 'jpeg', 'png'])
st.markdown("<p style='text-align: center; color: gray;'>或</p>", unsafe_allow_html=True)
camera_photo = st.camera_input("📸 開啟相機直接拍")

photo_to_use = upload_photo if upload_photo else camera_photo

if photo_to_use:
    if not api_key:
        st.warning("⚠️ 請先在上方設定新的 API Key，才能啟用 AI 自動辨識功能。")
    else:
        if st.button("✨ 讓 AI 幫我算幾箱！", type="primary", use_container_width=True):
            with st.spinner("AI 正在用極速辨識紙箱數量中..."):
                try:
                    # 圖片轉 base64
                    img_bytes = photo_to_use.getvalue()
                    base64_image = base64.b64encode(img_bytes).decode('utf-8')
                    
                    # 【關鍵修正】：使用 -latest 指定最新的模型版本
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
                    headers = {'Content-Type': 'application/json'}
                    prompt = "你是一個專業的物流理貨員。請看這張照片，幫我計算畫面中的紙箱或貨箱數量，並將它們大約分類為「大箱」、「中箱」、「小箱」。請嚴格只回傳以下 JSON 格式，不要包含任何其他文字或標記符號：{\"大箱\": 數量, \"中箱\": 數量, \"小箱\": 數量}"
                    
                    payload = {
                        "contents": [{
                            "parts": [
                                {"text": prompt},
                                {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}}
                            ]
                        }]
                    }
                    
                    response = requests.post(url, headers=headers, json=payload)
                    response_data = response.json()
                    
                    if 'error' in response_data:
                        st.error(f"API 錯誤: {response_data['error']['message']}")
                    else:
                        result_text = response_data['candidates'][0]['content']['parts'][0]['text']
                        result_text = result_text.replace("```json", "").replace("```", "").strip()
                        
                        if not result_text.startswith("{"):
                            start_idx = result_text.find("{")
                            end_idx = result_text.rfind("}") + 1
                            result_text = result_text[start_idx:end_idx]
                            
                        ai_counts = json.loads(result_text)
                        
                        for item in st.session_state['items']:
                            if item['type'] == 'quick':
                                if "大箱" in item['name']:
                                    item['qty'] = ai_counts.get("大箱", 0)
                                elif "中箱" in item['name']:
                                    item['qty'] = ai_counts.get("中箱", 0)
                                elif "小箱" in item['name']:
                                    item['qty'] = ai_counts.get("小箱", 0)
                                    
                        st.success("✅ AI 辨識完成！數字已自動填入下方的「急件快速估算區」！")
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"辨識失敗，請重試。錯誤細節: {e}")

# ==========================================
# ⚡ 急件快速粗估區
# ==========================================
st.markdown("---")
st.subheader("⚡ 急件快速估算 (不挑品名)")
for i, item in enumerate(st.session_state['items']):
    if item['type'] == 'quick':
        st.markdown(f"**{item['name']}**")
        item['qty'] = st.number_input("數量", value=item['qty'], min_value=0, step=1, key=f'qty_{i}_v{r_id}', label_visibility="collapsed")
        st.markdown("<hr style='margin: 4px 0px; border: none; border-top: 1px solid #222;'>", unsafe_allow_html=True)

quick_area = sum(item['l'] * item['w'] * item['qty'] for item in st.session_state['items'] if item['type'] == 'quick')
quick_pct = (quick_area / truck_area) * 100 if truck_area > 0 else 0
st.info(f"⚡ **快速估算佔用**：{quick_pct:.1f}%  (面積：{quick_area:,} cm²)")
st.progress(min(quick_pct / 100, 1.0))

# ==========================================
# 📥 精確品名設定區
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📥 精確品名與數量設定")
for i, item in enumerate(st.session_state['items']):
    if item['type'] != 'quick':
        pri_text = "⭐ " if item.get("priority") else ""
        label = f"{pri_text}**{item['name']}** *({item['l']}x{item['w']})*  🔒必要"
        item['required'] = st.checkbox(label, value=item.get('required', False), key=f'req_{i}_v{r_id}')
        
        item['qty'] = st.number_input("數量", value=item['qty'], min_value=0, step=1, key=f'qty_{i}_v{r_id}', label_visibility="collapsed")
        
        if item["type"] == "temp":
            with st.expander("✏️ 調整臨時貨物"):
                item['name'] = st.text_input("品名", value=item['name'], key=f'edit_name_{i}_v{r_id}')
                c1, c2 = st.columns(2)
                item['l'] = c1.number_input("長(cm)", value=item['l'], min_value=1, step=5, key=f'edit_l_{i}_v{r_id}')
                item['w'] = c2.number_input("寬(cm)", value=item['w'], min_value=1, step=5, key=f'edit_w_{i}_v{r_id}')
                item['priority'] = st.checkbox("⭐ 優先放車頭", value=item['priority'], key=f'edit_pri_{i}_v{r_id}')
                
        st.markdown("<hr style='margin: 4px 0px; border: none; border-top: 1px solid #222;'>", unsafe_allow_html=True)

st.button("➕ 新增臨時貨物", on_click=add_temp_item, use_container_width=True)

regular_area = sum(item['l'] * item['w'] * item['qty'] for item in st.session_state['items'] if item['type'] != 'quick')
regular_pct = (regular_area / truck_area) * 100 if truck_area > 0 else 0
st.info(f"📍 **精確品名佔用**：{regular_pct:.1f}%  (面積：{regular_area:,} cm²)")
st.progress(min(regular_pct / 100, 1.0))

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 一鍵清空數量", type="secondary", use_container_width=True):
    reset_all()
    st.rerun()

# ==========================================
# 📊 總和裝載狀態與超載建議 (置底)
# ==========================================
st.markdown("---")
st.subheader("📊 總和裝載狀態與超載建議")

total_item_area = quick_area + regular_area
total_pct = (total_item_area / truck_area) * 100 if truck_area > 0 else 0

if total_pct > 100:
    excess_area = total_item_area - truck_area
    st.error(f"🚨 **整車面積超載！** 目前總計超出約 **{excess_area:,} cm²** 空間！")
    
    st.markdown("### 💡 建議留車不上車清單：")
    
    disposable_items = []
    for item in st.session_state['items']:
        if item['qty'] > 0 and not item.get('required', False):
            disposable_items.append({
                'name': item['name'],
                'single_area': item['l'] * item['w'],
                'max_qty': item['qty'],
                'priority': item['priority']
            })
            
    disposable_items.sort(key=lambda x: (x['priority'], -x['single_area']))
    
    found_solution = False
    temp_excess = excess_area
    
    for item in disposable_items:
        if item['single_area'] > 0:
            needed_drop = -(-temp_excess // item['single_area']) 
            drop_qty = min(needed_drop, item['max_qty'])
            
            if drop_qty > 0:
                star = " ⭐(雖優先但非必要)" if item['priority'] else ""
                st.warning(f"👉 建議拿掉 **{item['name']}** × {drop_qty} 件 (可清出 {item['single_area'] * drop_qty:,} cm²){star}")
                temp_excess -= item['single_area'] * drop_qty
                found_solution = True
                if temp_excess <= 0:
                    break
                    
    if temp_excess > 0:
        if found_solution:
            st.error(f"⚠️ 拿掉上述非必要貨物後，仍超載 {temp_excess:,} cm²。請檢視「必要」貨物與「快速估算」區的數量！")
        else:
            st.error("⚠️ 目前車上全都是「🔒必要貨物」，無法提供留車建議。請直接分車或協調必要清單！")

elif total_pct > 85:
    st.warning(f"⚠️ **整車非常極限！** 總面積佔用 {total_pct:.1f}% (接近滿載，注意縫隙)")
elif total_pct > 0:
    st.info(f"🟢 **整車空間安全**：總面積佔用 {total_pct:.1f}%，可順利出車！")
else:
    st.info("🟢 **尚未使用**：目前佔用 0.0%")

if total_pct > 0:
    st.progress(min(total_pct / 100, 1.0))

if total_item_area > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 目前已選貨物總計")
    total_pieces = 0
    for item in st.session_state['items']:
        if item['qty'] > 0:
            item_total_area = item['l'] * item['w'] * item['qty']
            req_mark = " 🔒" if item.get('required') else ""
            st.write(f"- **{item['name']}{req_mark}**：{item['qty']} 件 (佔地 {item_total_area:,} cm²)")
            total_pieces += item['qty']
    st.markdown(f"**總計件數**：{total_pieces} 件 | **總佔用面積**：{total_item_area:,} cm²")
