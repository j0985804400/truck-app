import streamlit as st
import os

def init_state():
    st.session_state['truck_l'] = 820
    st.session_state['truck_w'] = 243
    
    if 'reset_count' not in st.session_state:
        st.session_state['reset_count'] = 0
    
    st.session_state['items'] = [
        {"name": "333", "l": 150, "w": 150, "qty": 0, "priority": True, "type": "regular"},
        {"name": "LAM", "l": 1, "w": 1, "qty": 0, "priority": False, "type": "regular"},
        {"name": "EX2", "l": 60, "w": 67, "qty": 0, "priority": False, "type": "regular"},
        {"name": "WET", "l": 62, "w": 78, "qty": 0, "priority": False, "type": "regular"},
        {"name": "WET長箱", "l": 102, "w": 52, "qty": 0, "priority": False, "type": "regular"},
        {"name": "ETTN", "l": 65, "w": 95, "qty": 0, "priority": False, "type": "regular"},
        {"name": "DPS2", "l": 80, "w": 126, "qty": 0, "priority": False, "type": "regular"},
        {"name": "UCU", "l": 61, "w": 106, "qty": 0, "priority": False, "type": "regular"},
        {"name": "ICP", "l": 1, "w": 1, "qty": 0, "priority": False, "type": "regular"},
        {"name": "APC", "l": 1, "w": 1, "qty": 0, "priority": False, "type": "regular"},
        {"name": "IOS大", "l": 122, "w": 80, "qty": 0, "priority": False, "type": "regular"},
        {"name": "IOS小", "l": 102, "w": 80, "qty": 0, "priority": False, "type": "regular"},
        {"name": "爐管方型", "l": 70, "w": 70, "qty": 0, "priority": False, "type": "regular"},
        {"name": "辛巳大", "l": 76, "w": 56, "qty": 0, "priority": False, "type": "regular"},
        {"name": "辛巳小", "l": 70, "w": 46, "qty": 0, "priority": False, "type": "regular"},
        {"name": "SDRM", "l": 67, "w": 56, "qty": 0, "priority": False, "type": "regular"},
        {"name": "CUP", "l": 90, "w": 56, "qty": 0, "priority": False, "type": "regular"},
        {"name": "CUP SOD", "l": 80, "w": 50, "qty": 0, "priority": False, "type": "regular"}
    ]

if 'items' not in st.session_state:
    init_state()

def add_temp_item():
    st.session_state['items'].append({"name": "臨時新增", "l": 50, "w": 50, "qty": 1, "priority": False, "type": "temp"})

def reset_all():
    st.session_state['reset_count'] += 1
    for item in st.session_state['items']:
        item['qty'] = 0

st.set_page_config(page_title="貨車裝箱防爆計算器", layout="centered")
st.title("📦 貨車裝箱防爆計算器")

st.markdown(f"<p style='color: gray; margin-bottom: 5px;'>🚚 目前車斗規格：長 {st.session_state['truck_l']} cm × 寬 {st.session_state['truck_w']} cm</p>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📥 貨物數量設定")

r_id = st.session_state.get('reset_count', 0)

for i, item in enumerate(st.session_state['items']):
    col_info, col_qty = st.columns([6.2, 3.8])
    
    with col_info:
        pri_text = "⭐ " if item["priority"] else ""
        st.markdown(f"<div style='margin-top: 8px; font-size: 0.95em;'><b>{pri_text}{item['name']}</b> <span style='font-size:0.75em; color:gray;'>({item['l']}x{item['w']})</span></div>", unsafe_allow_html=True)
    
    with col_qty:
        item['qty'] = st.number_input(
            "數量", 
            value=item['qty'], 
            min_value=0, 
            step=1, 
            key=f'qty_{i}_v{r_id}', 
            label_visibility="collapsed"
        )
    
    if item["type"] == "temp":
        with st.expander("✏️ 調整臨時貨物設定"):
            item['name'] = st.text_input("品名", value=item['name'], key=f'edit_name_{i}_v{r_id}')
            c1, c2 = st.columns(2)
            item['l'] = c1.number_input("長(cm)", value=item['l'], min_value=1, step=5, key=f'edit_l_{i}_v{r_id}')
            item['w'] = c2.number_input("寬(cm)", value=item['w'], min_value=1, step=5, key=f'edit_w_{i}_v{r_id}')
            item['priority'] = st.checkbox("⭐ 優先放車頭", value=item['priority'], key=f'edit_pri_{i}_v{r_id}')
            
    st.markdown("<hr style='margin: 1px 0px; border: none; border-top: 1px solid #222;'>", unsafe_allow_html=True)

st.button("➕ 新增臨時貨物", on_click=add_temp_item, use_container_width=True)
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔄 一鍵清空數量", type="secondary", use_container_width=True):
    reset_all()
    st.rerun()

# === 即時面積防爆防線 (移至下方) ===
st.markdown("---")
st.subheader("📊 即時空間佔用評估")

truck_area = st.session_state['truck_l'] * st.session_state['truck_w']
total_item_area = sum(item['l'] * item['w'] * item['qty'] for item in st.session_state['items'])
usage_pct = (total_item_area / truck_area) * 100 if truck_area > 0 else 0

if usage_pct > 100:
    st.error(f"🚨 **面積超載！** 目前總面積佔用達 {usage_pct:.1f}% (超越車斗極限)")
elif usage_pct > 85:
    st.warning(f"⚠️ **非常極限！** 面積佔用 {usage_pct:.1f}% (接近滿載)")
elif usage_pct > 0:
    st.info(f"🟢 **面積初估安全**：目前佔用 {usage_pct:.1f}%")
else:
    st.info("🟢 **尚未使用**：目前佔用 0.0%")

if usage_pct > 0:
    st.progress(min(usage_pct / 100, 1.0))

if total_item_area > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 目前已選貨物統計")
    total_pieces = 0
    for item in st.session_state['items']:
        if item['qty'] > 0:
            item_total_area = item['l'] * item['w'] * item['qty']
            st.write(f"- **{item['name']}**：{item['qty']} 件 (佔地 {item_total_area} cm²)")
            total_pieces += item['qty']
    st.markdown(f"**總計件數**：{total_pieces} 件 | **總佔用面積**：{total_item_area} cm²")
