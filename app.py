import streamlit as st
import os

def init_state():
    st.session_state['truck_l'] = 820
    st.session_state['truck_w'] = 243
    
    if 'reset_count' not in st.session_state:
        st.session_state['reset_count'] = 0
        
    if 'double_layer_choices' not in st.session_state:
        st.session_state['double_layer_choices'] = []
    
    st.session_state['items'] = [
        # === 快速粗估專區 ===
        {"name": "📦 快速大箱 (約同 DPS2/IOS大)", "l": 100, "w": 95, "qty": 0, "priority": False, "skip": False, "type": "quick"},
        {"name": "📦 快速中箱 (約同 UCU/ETTN)", "l": 80, "w": 75, "qty": 0, "priority": False, "skip": False, "type": "quick"},
        {"name": "📦 快速小箱 (約同 EX2/WET)", "l": 65, "w": 60, "qty": 0, "priority": False, "skip": False, "type": "quick"},
        
        # === 正規貨物清單 ===
        {"name": "333", "l": 150, "w": 150, "qty": 0, "priority": True, "skip": False, "type": "regular"},
        {"name": "LAM", "l": 75, "w": 116, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "EX2", "l": 60, "w": 67, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "EP2", "l": 119, "w": 67, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "WET", "l": 62, "w": 78, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "WET長箱", "l": 102, "w": 52, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "ETTN", "l": 65, "w": 95, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "DPS2", "l": 80, "w": 126, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "DPS2小", "l": 53, "w": 104, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "UCU", "l": 61, "w": 106, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "ICP", "l": 82, "w": 82, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "APC", "l": 63, "w": 63, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "IOS大", "l": 122, "w": 80, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "IOS小", "l": 102, "w": 80, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "爐管方型", "l": 70, "w": 70, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "BJM", "l": 66, "w": 125, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "辛巳大", "l": 76, "w": 56, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "辛巳小", "l": 70, "w": 46, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "SDRM", "l": 67, "w": 56, "qty": 0, "priority": False, "skip": False, "type": "regular"},
        {"name": "CUP", "l": 90, "w": 56, "qty": 0, "priority": False, "skip": False, "type": "regular"}
    ]

if 'items' not in st.session_state:
    init_state()

def add_temp_item():
    st.session_state['items'].append({"name": "臨時新增", "l": 50, "w": 50, "qty": 1, "priority": False, "skip": False, "type": "temp"})

def reset_all():
    st.session_state['reset_count'] += 1
    st.session_state['double_layer_choices'] = []
    for item in st.session_state['items']:
        item['qty'] = 0
        item['skip'] = False

st.set_page_config(page_title="貨車裝箱防爆計算器", layout="centered")
st.title("📦 貨車裝箱防爆計算器")

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

# 動態抓取數量 > 0 且沒有被勾選「不上車」的貨品
active_items = [item['name'] for item in st.session_state['items'] if item['qty'] > 0 and not item.get('skip', False)]

# 自動清理舊紀錄，避免出現 Streamlit 警告
if 'double_layer_choices' in st.session_state:
    st.session_state['double_layer_choices'] = [
        name for name in st.session_state['double_layer_choices'] if name in active_items
    ]

if active_items:
    double_choices = st.multiselect(
        "選擇可「疊兩層」的貨物 (佔地面積將自動減半)：",
        options=active_items,
        key="double_layer_choices"
    )
else:
    st.info("請先在上方輸入要載的貨物數量。")
    double_choices = []

# ==========================================
# 算面積並更新上方的進度條 (透過 st.empty)
# ==========================================
quick_area = 0
regular_area = 0

for item in st.session_state['items']:
    if item['qty'] > 0 and not item.get('skip', False):
        single = item['l'] * item['w']
        # 如果該品名出現在下拉選單中，面積減半
        if item['name'] in double_choices:
            single = single / 2
        
        if item['type'] == 'quick':
            quick_area += single * item['qty']
        else:
            regular_area += single * item['qty']

quick_pct = (quick_area / truck_area) * 100 if truck_area > 0 else 0
with quick_ph.container():
    st.info(f"⚡ **快速估算佔用**：{quick_pct:.1f}%")
    st.progress(min(quick_pct / 100, 1.0))

regular_pct = (regular_area / truck_area) * 100 if truck_area > 0 else 0
with reg_ph.container():
    st.info(f"📍 **精確品名佔用**：{regular_pct:.1f}%")
    st.progress(min(regular_pct / 100, 1.0))

# ==========================================
# 📊 總和裝載狀態與超載建議 (置底)
# ==========================================
st.markdown("---")
st.subheader("📊 總和裝載狀態與超載建議")

total_item_area = quick_area + regular_area
total_pct = (total_item_area / truck_area) * 100 if truck_area > 0 else 0

if total_pct > 100:
    excess_area = total_item_area - truck_area
    st.error(f"🚨 **整車已超載！** 目前總佔用達 **{total_pct:.1f}%**！")
    
    st.markdown("### 💡 建議留車不上車清單：")
    
    disposable_items = []
    for item in st.session_state['items']:
        if item['qty'] > 0 and not item.get('skip', False):
            single_area = item['l'] * item['w']
            if item['name'] in double_choices:
                single_area = single_area / 2
            disposable_items.append({
                'name': item['name'],
                'single_area': single_area,
                'max_qty': item['qty'],
                'priority': item.get('priority', False)
            })
            
    disposable_items.sort(key=lambda x: (x['priority'], -x['single_area']))
    
    found_solution = False
    temp_excess = excess_area
    
    for item in disposable_items:
        if item['single_area'] > 0:
            needed_drop = -(-int(temp_excess) // int(item['single_area'])) 
            drop_qty = min(needed_drop, item['max_qty'])
            
            if drop_qty > 0:
                star = " ⭐(雖優先但體積大)" if item['priority'] else ""
                st.warning(f"👉 建議拿掉 **{item['name']}** × {drop_qty} 件{star}")
                temp_excess -= item['single_area'] * drop_qty
                found_solution = True
                if temp_excess <= 0:
                    break
                    
    if temp_excess > 0:
        if found_solution:
            st.error("⚠️ 拿掉上述貨物後，仍處於超載狀態。請自行評估還要剔除哪些貨物！")

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
        if item['qty'] > 0 and not item.get('skip', False):
            double_mark = " 📦[疊兩層]" if item['name'] in double_choices else ""
            st.write(f"- **{item['name']}{double_mark}**：{item['qty']} 件")
            total_pieces += item['qty']
    st.markdown(f"**總計件數**：{total_pieces} 件")
