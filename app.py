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
        {"name": "ICP", "l": 82, "w": 82, "qty": 0, "priority": False, "type": "regular"},
        {"name": "APC", "l": 1, "w": 1, "qty": 0, "priority": False, "type": "regular"},
        {"name": "IOS大", "l": 122, "w": 80, "qty": 0, "priority": False, "type": "regular"},
        {"name": "IOS小", "l": 102, "w": 80, "qty": 0, "priority": False, "type": "regular"},
        {"name": "爐管方型", "l": 70, "w": 70, "qty": 0, "priority": False, "type": "regular"},
        {"name": "辛巳大", "l": 76, "w": 56, "qty": 0, "priority": False, "type": "regular"},
        {"name": "辛巳小", "l": 70, "w": 46, "qty": 0, "priority": False, "type": "regular"},
        {"name": "SDRM", "l": 67, "w": 56, "qty": 0, "priority": False, "type": "regular"},
        {"name": "CUP", "l": 90, "w": 56, "qty": 0, "priority": False, "type": "regular"},
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

# === 智慧超載分流建議 (置底) ===
st.markdown("---")
st.subheader("🚨 裝載狀態與超載建議")

truck_area = st.session_state['truck_l'] * st.session_state['truck_w']
total_item_area = sum(item['l'] * item['w'] * item['qty'] for item in st.session_state['items'])
usage_pct = (total_item_area / truck_area) * 100 if truck_area > 0 else 0

if usage_pct > 100:
    excess_area = total_item_area - truck_area
    st.error(f"🚨 **面積超載！** 目前超出約 **{excess_area:,} cm²** 空間！")
    
    st.markdown("### 💡 建議留車不上車清單：")
    st.markdown("為了消除超載，建議從下列已選貨物中挑選部分不上車：")
    
    # 收集目前有選的貨物（優先挑選非 priority 的項目）
    selected_items = []
    for item in st.session_state['items']:
        if item['qty'] > 0:
            single_area = item['l'] * item['w']
            selected_items.append({
                'name': item['name'],
                'single_area': single_area,
                'max_qty': item['qty'],
                'priority': item['priority']
            })
            
    # 排序：非優先車頭放前面，單件面積大的放後面讓系統精算
    selected_items.sort(key=lambda x: (x['priority'], -x['single_area']))
    
    found_solution = False
    for item in selected_items:
        if item['single_area'] > 0:
            # 計算拿掉幾件剛好可以降到超載範圍內
            needed_drop = -(-excess_area // item['single_area']) # 向上取整
            drop_qty = min(needed_drop, item['max_qty'])
            if drop_qty > 0:
                star = " ⭐(車頭優先，建議保留)" if item['priority'] else ""
                st.warning(f"👉 建議拿掉 **{item['name']}** × {drop_qty} 件 (可清出 {item['single_area'] * drop_qty:,} cm²){star}")
                excess_area -= item['single_area'] * drop_qty
                found_solution = True
                if excess_area <= 0:
                    break
                    
    if not found_solution:
        st.info("目前選擇的貨物皆為單件巨大件，建議整箱調整。")

elif usage_pct > 85:
    st.warning(f"⚠️ **非常極限！** 面積佔用 {usage_pct:.1f}% (接近滿載，注意縫隙)")
elif usage_pct > 0:
    st.info(f"🟢 **空間安全**：目前佔用 {usage_pct:.1f}%，可順利出車！")
else:
    st.info("🟢 **尚未使用**：目前佔用 0.0%")

if usage_pct > 0:
    st.progress(min(usage_pct / 100, 1.0))
