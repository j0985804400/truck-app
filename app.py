import streamlit as st
import os

def init_state():
    st.session_state['truck_l'] = 820
    st.session_state['truck_w'] = 240
    
    if 'reset_count' not in st.session_state:
        st.session_state['reset_count'] = 0
    
    st.session_state['items'] = [
        # === 快速粗估專區 ===
        {"name": "📦 快速大箱 (約同 DPS2/IOS大)", "l": 100, "w": 95, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "quick"},
        {"name": "📦 快速中箱 (約同 UCU/ETTN)", "l": 80, "w": 75, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "quick"},
        {"name": "📦 快速小箱 (約同 EX2/WET)", "l": 65, "w": 60, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "quick"},
        
        # === 正規貨物清單 ===
        {"name": "333", "l": 150, "w": 150, "qty": 0, "stacked_qty": 0, "priority": True, "skip": False, "type": "regular"},
        {"name": "LAM", "l": 75, "w": 116, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "EX2", "l": 60, "w": 67, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "EP2", "l": 119, "w": 67, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "WET", "l": 62, "w": 78, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "WET長箱", "l": 102, "w": 52, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "ETTN", "l": 65, "w": 95, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "DPS2", "l": 80, "w": 126, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "DPS2小", "l": 53, "w": 104, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "UCU", "l": 61, "w": 106, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "ICP", "l": 82, "w": 82, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "APC", "l": 63, "w": 63, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "IOS大", "l": 122, "w": 80, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "IOS小", "l": 102, "w": 80, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "爐管方型", "l": 70, "w": 70, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "BJM", "l": 66, "w": 125, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "辛巳大", "l": 76, "w": 56, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "辛巳小", "l": 70, "w": 46, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "SDRM", "l": 67, "w": 56, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "CUP", "l": 90, "w": 56, "qty": 0, "stacked_qty": 0, "priority": False, "skip": False, "type": "regular"}
    ]

if 'items' not in st.session_state:
    init_state()

def add_temp_item():
    st.session_state['items'].append({"name": "臨時新增", "l": 50, "w": 50, "qty": 1, "stacked_qty": 0, "priority": False, "skip": False, "type": "temp"})

def reset_all():
    st.session_state['reset_count'] += 1
    for item in st.session_state['items']:
        item['qty'] = 0
        item['stacked_qty'] = 0
        item['skip'] = False

st.set_page_config(page_title="貨車裝箱計算器", layout="centered")
st.title("📦 貨車裝箱計算器")

r_id = st.session_state.get('reset_count', 0)
truck_area = st.session_state['truck_l'] * st.session_state['truck_w']

# ==========================================
# ⚡ 急件快速粗估區
# ==========================================
st.subheader("⚡ 急件快速估算 (不挑品名)")
for i, item in enumerate(st.session_state['items']):
    if item['type'] == 'quick':
        st.markdown(f"**{item['name']}**")
        item['qty'] = st.number_input("數量", value=item['qty'], min_value=0, step=1, key=f'qty_{i}_v{r_id}', label_visibility="collapsed")
        st.markdown("<hr style='margin: 4px 0px; border: none; border-top: 1px solid #222;'>", unsafe_allow_html=True)

# 預留上方進度條的位置
quick_ph = st.empty()

# ==========================================
# 📥 精確品名設定區
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📥 精確品名與數量設定")
for i, item in enumerate(st.session_state['items']):
    if item['type'] != 'quick':
        pri_text = "⭐ " if item.get("priority") else ""
        st.markdown(f"{pri_text}**{item['name']}** *({item['l']}x{item['w']})*")
        
        c_qty, c_skip = st.columns([7, 3])
        with c_qty:
            item['qty'] = st.number_input("數量", value=item['qty'], min_value=0, step=1, key=f'qty_{i}_v{r_id}', label_visibility="collapsed")
        with c_skip:
            item['skip'] = st.checkbox("🚫不上車", value=item.get('skip', False), key=f'skip_{i}_v{r_id}')
        
        if item["type"] == "temp":
            with st.expander("✏️ 調整臨時貨物"):
                item['name'] = st.text_input("品名", value=item['name'], key=f'edit_name_{i}_v{r_id}')
                c1, c2 = st.columns(2)
                item['l'] = c1.number_input("長(cm)", value=item['l'], min_value=1, step=5, key=f'edit_l_{i}_v{r_id}')
                item['w'] = c2.number_input("寬(cm)", value=item['w'], min_value=1, step=5, key=f'edit_w_{i}_v{r_id}')
                item['priority'] = st.checkbox("⭐ 優先放車頭", value=item['priority'], key=f'edit_pri_{i}_v{r_id}')
                
        st.markdown("<hr style='margin: 4px 0px; border: none; border-top: 1px solid #222;'>", unsafe_allow_html=True)

st.button("➕ 新增臨時貨物", on_click=add_temp_item, use_container_width=True)

# 預留上方進度條的位置
reg_ph = st.empty()

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 一鍵清空數量", type="secondary", use_container_width=True):
    reset_all()
    st.rerun()

# ==========================================
# 📦 統一堆疊設定區 (只顯示已選且要上車的貨物)
# ==========================================
st.markdown("---")
st.subheader("📦 已選貨物堆疊設定")
st.caption("設定疊在上層的件數，系統將自動從車斗佔用面積中扣除。")

active_items = [item for item in st.session_state['items'] if item['qty'] > 0 and not item.get('skip', False)]

if active_items:
    for i, item in enumerate(active_items):
        # 防呆：避免上層數量超過總數量
        if item.get('stacked_qty', 0) > item['qty']:
            item['stacked_qty'] = item['qty']
            
        c_name, c_stack = st.columns([5, 5])
        with c_name:
            st.markdown(f"<div style='margin-top: 8px;'><b>{item['name']}</b> (共 {item['qty']} 件)</div>", unsafe_allow_html=True)
        with c_stack:
            item['stacked_qty'] = st.number_input(
                "疊上層數", 
                value=item.get('stacked_qty', 0), 
                min_value=0, 
                max_value=item['qty'], 
                step=1, 
                key=f"stack_{item['name']}_{i}_{r_id}",
                label_visibility="collapsed"
            )
        st.markdown("<hr style='margin: 4px 0px; border: none; border-top: 1px dashed #444;'>", unsafe_allow_html=True)
else:
    st.info("請先在上方輸入要載的貨物數量。")

# ==========================================
# 算面積並更新上方的進度條 (透過 st.empty)
# ==========================================
quick_area = 0
regular_area = 0

for item in st.session_state['items']:
    if item['qty'] > 0 and not item.get('skip', False):
        single = item['l'] * item['w']
        floor_qty = item['qty'] - item.get('stacked_qty', 0)
        
        if item['type'] == 'quick':
            quick_area += single * floor_qty
        else:
            regular_area += single * floor_qty

quick_pct = (quick_area / truck_area) * 100 if truck_area > 0 else 0
with quick_ph.container():
    st.info(f"⚡ **快速估算佔用**：{quick_pct:.1f}%")
    st.
