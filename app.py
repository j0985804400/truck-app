import streamlit as st

def init_state():
    st.session_state['truck_l'] = 820
    st.session_state['truck_w'] = 240
    
    if 'reset_count' not in st.session_state:
        st.session_state['reset_count'] = 0
    
    st.session_state['items'] = [
        # === 正規貨物清單 ===
        # 1. WET 類
        {"name": "WET", "l": 62, "w": 78, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "1. WET系列"},
        {"name": "WET長箱", "l": 102, "w": 52, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "1. WET系列"},
        
        # 2. LAM / DPS2 類
        {"name": "LAM", "l": 75, "w": 116, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "2. LAM與DPS2系列"},
        {"name": "DPS2", "l": 80, "w": 126, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "2. LAM與DPS2系列"},
        {"name": "DPS2小", "l": 53, "w": 104, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "2. LAM與DPS2系列"},
        {"name": "SDRM", "l": 67, "w": 56, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "2. LAM與DPS2系列"},
        
        # 3. IOS 類
        {"name": "IOS大", "l": 122, "w": 80, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "3. IOS系列"},
        {"name": "IOS小", "l": 102, "w": 80, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "3. IOS系列"},
        
        # 4. EX 與 EP 類 (放在 ETTN 上面)
        {"name": "EX2", "l": 60, "w": 67, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "4. EX與EP系列"},
        {"name": "EP2", "l": 119, "w": 67, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "4. EX與EP系列"},
        
        # 5. ETTN / UCU / ICP / APC 類
        {"name": "ETTN", "l": 65, "w": 95, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "5. ETTN/UCU系列"},
        {"name": "UCU", "l": 61, "w": 106, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "5. ETTN/UCU系列"},
        {"name": "ICP", "l": 82, "w": 82, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "5. ETTN/UCU系列"},
        {"name": "APC", "l": 63, "w": 63, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "5. ETTN/UCU系列"},
        
        # 6. 爐管 / BJM / 333 類
        {"name": "爐管方型", "l": 70, "w": 70, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "6. 爐管與大型設備"},
        {"name": "BJM", "l": 66, "w": 125, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "6. 爐管與大型設備"},
        {"name": "333", "l": 150, "w": 150, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "6. 爐管與大型設備"},
        
        # 7. 辛巳類
        {"name": "辛巳大", "l": 76, "w": 56, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "7. 辛巳系列"},
        {"name": "辛巳小", "l": 70, "w": 46, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "7. 辛巳系列"},
        
        # 8. CUP 類
        {"name": "CUP", "l": 90, "w": 56, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "8. CUP系列"}
    ]

if 'items' not in st.session_state:
    init_state()

def add_temp_item():
    st.session_state['items'].append({"name": "臨時新增", "l": 50, "w": 50, "qty": 0, "stacked_qty": 0, "skip": False, "type": "temp", "cat": "9. 臨時自訂"})

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
# ⚡ 滿載預警提醒
# ==========================================
st.warning("⚠️ 提醒：約 35 箱即滿載！")

# ==========================================
# 📥 8大分類精確品名與數量設定區
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📥 精確品名與數量設定")

regular_items = [item for item in st.session_state['items'] if item['type'] in ['regular', 'temp']]
categories = sorted(list(set(item['cat'] for item in regular_items)))

cat_colors = {
    "1. WET系列": "#FF6B6B",
    "2. LAM與DPS2系列": "#4D96FF",
    "3. IOS系列": "#6BCB77",
    "4. EX與EP系列": "#FF66B2",
    "5. ETTN/UCU系列": "#FFD93D",
    "6. 爐管與大型設備": "#B983FF",
    "7. 辛巳系列": "#FF9F45",
    "8. CUP系列": "#00ADB5",
    "9. 臨時自訂": "#EEEEEE"
}

for cat in categories:
    color = cat_colors.get(cat, "#4D96FF")
    st.markdown(f"<div style='border-left: 5px solid {color}; padding-left: 8px; margin-top: 14px; margin-bottom: 6px; font-weight: bold; color: {color};'>{cat}</div>", unsafe_allow_html=True)
    
    cat_items = [item for item in regular_items if item['cat'] == cat]
    for item in cat_items:
        idx = st.session_state['items'].index(item)
        c_name, c_qty = st.columns([6, 4])
        with c_name:
            st.markdown(f"<div style='margin-top: 8px;'><b>{item['name']}</b> <span style='color: #aaa; font-size: 0.8em;'>({item['l']}x{item['w']}cm)</span></div>", unsafe_allow_html=True)
        with c_qty:
            item['qty'] = st.number_input("數量", value=item['qty'], min_value=0, step=1, key=f'qty_{idx}_v{r_id}', label_visibility="collapsed")
            
        if item["type"] == "temp":
            with st.expander("✏️ 調整此臨時貨物尺寸與名稱"):
                item['name'] = st.text_input("品名", value=item['name'], key=f'edit_name_{idx}_v{r_id}')
                c1, c2 = st.columns(2)
                item['l'] = c1.number_input("長(cm)", value=item['l'], min_value=1, step=5, key=f'edit_l_{idx}_v{r_id}')
                item['w'] = c2.number_input("寬(cm)", value=item['w'], min_value=1, step=5, key=f'edit_w_{idx}_v{r_id}')
                
        st.markdown("<hr style='margin: 4px 0px; border: none; border-top: 1px solid #222;'>", unsafe_allow_html=True)

st.button("➕ 新增臨時自訂貨物", on_click=add_temp_item, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 一鍵清空數量", type="secondary", use_container_width=True):
    reset_all()
    st.rerun()

# ==========================================
# 📊 中段：輸入完品項後的即時趴數面板
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
mid_progress_ph = st.empty()

# ==========================================
# 📦 已選貨物裝載設定區 (不上車勾選 + 疊上層數設定)
# ==========================================
st.markdown("---")
st.subheader("📦 已選貨物裝載設定")
st.caption("在此統一管理已選貨物的不上車狀態，或設定疊在上層的件數。")

active_items = [item for item in st.session_state['items'] if item['qty'] > 0]

if active_items:
    for i, item in enumerate(active_items):
        if item.get('stacked_qty', 0) > item['qty']:
            item['stacked_qty'] = item['qty']
            
        c_name, c_skip, c_stack = st.columns([4, 3, 3])
        with c_name:
            st.markdown(f"<div style='margin-top: 8px;'><b>{item['name']}</b><br><span style='color:#aaa; font-size:0.8em;'>({item['qty']}件)</span></div>", unsafe_allow_html=True)
        with c_skip:
            item['skip'] = st.checkbox("🚫不上車", value=item.get('skip', False), key=f'skip_ctrl_{item["name"]}_{i}_{r_id}')
        with c_stack:
            item['stacked_qty'] = st.number_input(
                "疊上層數", 
                value=item.get('stacked_qty', 0), 
                min_value=0, 
                max_value=item['qty'], 
                step=1, 
                key=f"stack_ctrl_{item['name']}_{i}_{r_id}",
                label_visibility="collapsed"
            )
        st.markdown("<hr style='margin: 4px 0px; border: none; border-top: 1px dashed #444;'>", unsafe_allow_html=True)
else:
    st.info("請先在上方輸入要載的貨物數量。")

# ==========================================
# 算面積 (統一在底層計算)
# ==========================================
regular_area = 0
for item in st.session_state['items']:
    if item['qty'] > 0 and not item.get('skip', False):
        single = item['l'] * item['w']
        floor_qty = item['qty'] - item.get('stacked_qty', 0)
        regular_area += single * floor_qty

total_pct = (regular_area / truck_area) * 100 if truck_area > 0 else 0

# 將算好的趴數塞回中段面板
with mid_progress_ph.container():
    if total_pct > 100:
        st.error(f"🚨 **目前總佔用：{total_pct:.1f}% (已超載！)**")
    elif total_pct > 85:
        st.warning(f"⚠️ **目前總佔用：{total_pct:.1f}% (接近滿載)**")
    elif total_pct > 0:
        st.success(f"🟢 **目前總佔用：{total_pct:.1f}%**")
    else:
        st.info("🟢 **目前佔用：0.0%**")
    st.progress(min(total_pct / 100, 1.0))

# ==========================================
# 📊 置底：最終裝載狀態與超載建議
# ==========================================
st.markdown("---")
st.subheader("📊 最終裝載狀態與超載建議")

if total_pct > 100:
    st.error(f"🚨 **整車已超載！** 最終佔用達 **{total_pct:.1f}%**！")
    st.progress(1.0)
    
    st.markdown("### 💡 建議留車不上車清單：")
    
    disposable_items = []
    for item in st.session_state['items']:
        if item['qty'] > 0 and not item.get('skip', False):
            floor_qty = item['qty'] - item.get('stacked_qty', 0)
            if floor_qty > 0:  
                single_area = item['l'] * item['w']
                disposable_items.append({
                    'name': item['name'],
                    'single_area': single_area,
                    'max_qty': floor_qty
                })
            
    disposable_items.sort(key=lambda x: -x['single_area'])
    
    found_solution = False
    temp_excess = regular_area - truck_area
    
    for item in disposable_items:
        if item['single_area'] > 0:
            needed_drop = -(-int(temp_excess) // int(item['single_area'])) 
            drop_qty = min(needed_drop, item['max_qty'])
            
            if drop_qty > 0:
                st.warning(f"👉 建議拿掉 **{item['name']}** × {drop_qty} 件")
                temp_excess -= item['single_area'] * drop_qty
                found_solution = True
                if temp_excess <= 0:
                    break
                    
    if temp_excess > 0:
        if found_solution:
            st.error("⚠️ 拿掉上述貨物後，仍處於超載狀態。請自行評估還要剔除哪些貨物！")
        else:
            st.error("⚠️ 查無可建議剔除的貨物，請手動調整數量。")

elif total_pct > 85:
    st.warning(f"⚠️ **非常極限！** 最終佔用 {total_pct:.1f}% (接近滿載，注意縫隙)")
    st.progress(min(total_pct / 100, 1.0))
elif total_pct > 0:
    st.info(f"🟢 **空間安全**：最終佔用 {total_pct:.1f}%，可順利出車！")
    st.progress(min(total_pct / 100, 1.0))
else:
    st.info("🟢 **尚未使用**：目前佔用 0.0%")

if regular_area > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 目前已選貨物總計")
    total_pieces = 0

    for item in st.session_state['items']:
        if item['qty'] > 0 and not item.get('skip', False):
            stack_mark = f" 📦[疊上層 {item['stacked_qty']} 件]" if item.get('stacked_qty', 0) > 0 else ""
            st.write(f"- **{item['name']}**：共 {item['qty']} 件{stack_mark}")
            total_pieces += item['qty']
    st.markdown(f"**總計出車件數**：{total_pieces} 件")
