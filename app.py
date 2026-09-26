import streamlit as st
import os

def init_state():
    st.session_state['truck_l'] = 820
    st.session_state['truck_w'] = 240
    
    if 'reset_count' not in st.session_state:
        st.session_state['reset_count'] = 0
    
    st.session_state['items'] = [
        # === 快速粗估專區 ===
        {"name": "📦 快速大箱 (約同 DPS2/IOS大)", "l": 100, "w": 95, "qty": 0, "priority": False, "required": False, "type": "quick"},
        {"name": "📦 快速中箱 (約同 UCU/ETTN)", "l": 80, "w": 75, "qty": 0, "priority": False, "required": False, "type": "quick"},
        {"name": "📦 快速小箱 (約同 EX2/WET)", "l": 65, "w": 60, "qty": 0, "priority": False, "required": False, "type": "quick"},
        
        # === 正規貨物清單 ===
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

st.set_page_config(page_title="貨車裝箱計算器", layout="centered")
st.title("📦 貨車裝箱計算器")

r_id = st.session_state.get('reset_count', 0)
truck_area = st.session_state['truck_l'] * st.session_state['truck_w']

# ==========================================
# ⚡ 急件快速粗估區
# ==========================================
st.subheader("⚡ 急件快速估算 ")
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
    st.warning(f"⚠️ **非常極限！** 總面積佔用 {total_pct:.1f}% (接近滿載，注意縫隙)")
elif total_pct > 0:
    st.info(f"🟢 **空間安全**：總面積佔用 {total_pct:.1f}%，可順利出車！")
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
