import streamlit as st
import math
import json
import urllib.parse

def init_state():
    st.session_state['truck_l'] = 820
    st.session_state['truck_w'] = 240
    
    if 'reset_count' not in st.session_state:
        st.session_state['reset_count'] = 0
    
    # 預設乾淨的貨物清單
    default_items = [
        {"name": "WET", "l": 62, "w": 78, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "1. WET系列"},
        {"name": "WET長箱", "l": 102, "w": 52, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "1. WET系列"},
        {"name": "LAM", "l": 75, "w": 116, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "2. LAM與DPS2系列"},
        {"name": "DPS2", "l": 80, "w": 126, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "2. LAM與DPS2系列"},
        {"name": "DPS2小", "l": 53, "w": 104, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "2. LAM與DPS2系列"},
        {"name": "SDRM", "l": 67, "w": 56, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "2. LAM與DPS2系列"},
        {"name": "IOS大", "l": 122, "w": 80, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "3. IOS系列"},
        {"name": "IOS小", "l": 102, "w": 80, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "3. IOS系列"},
        {"name": "EX2", "l": 60, "w": 67, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "4. EX與EP系列"},
        {"name": "EP2", "l": 119, "w": 67, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "4. EX與EP系列"},
        {"name": "ETTN", "l": 65, "w": 95, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "5. ETTN/UCU系列"},
        {"name": "UCU", "l": 61, "w": 106, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "5. ETTN/UCU系列"},
        {"name": "ICP", "l": 82, "w": 82, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "5. ETTN/UCU系列"},
        {"name": "APC", "l": 63, "w": 63, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "5. ETTN/UCU系列"},
        {"name": "爐管方型", "l": 70, "w": 70, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "6. 爐管與大型設備"},
        {"name": "BJM", "l": 66, "w": 125, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "6. 爐管與大型設備"},
        {"name": "333", "l": 150, "w": 150, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "6. 爐管與大型設備"},
        {"name": "辛巳大", "l": 76, "w": 56, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "7. 辛巳系列"},
        {"name": "辛巳小", "l": 70, "w": 46, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "7. 辛巳系列"},
        {"name": "CUP", "l": 90, "w": 56, "qty": 0, "stacked_qty": 0, "skip": False, "type": "regular", "cat": "8. CUP系列"}
    ]

    # === 【修復 BUG】安全的網址還原機制 ===
    if "cart" in st.query_params:
        try:
            cart_str = urllib.parse.unquote(st.query_params["cart"])
            saved_data = json.loads(cart_str)
            
            # 區分常規貨物與臨時貨物 (避免臨時貨物同名覆蓋)
            regular_saved = {d['n']: d for d in saved_data if d.get('t') != 'temp'}
            temp_saved = [d for d in saved_data if d.get('t') == 'temp']
            
            st.session_state['items'] = []
            for item in default_items:
                if item['name'] in regular_saved:
                    s = regular_saved[item['name']]
                    item['qty'] = s.get('q', 0)
                    item['stacked_qty'] = s.get('s', 0)
                    item['skip'] = s.get('k', False)
                st.session_state['items'].append(item)
            
            # 依序復原臨時新增的貨物
            for s in temp_saved:
                st.session_state['items'].append({
                    "name": s['n'], "l": s.get('l',50), "w": s.get('w',50),
                    "qty": s.get('q',0), "stacked_qty": s.get('s',0),
                    "skip": s.get('k',False), "type": "temp", "cat": "9. 臨時自訂"
                })
        except Exception as e:
            st.session_state['items'] = default_items
    else:
        st.session_state['items'] = default_items

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
    st.query_params.clear()

st.set_page_config(page_title="貨車裝箱計算器", layout="centered")

# ==========================================
# 🚀 頂部區塊優化：將「清空按鈕」移至標題旁邊
# ==========================================
col_title, col_btn = st.columns([7, 3], vertical_alignment="center")
with col_title:
    st.title("📦 裝箱計算器")
with col_btn:
    if st.button("🔄 全部清空", type="primary", use_container_width=True):
        reset_all()
        st.rerun()

r_id = st.session_state.get('reset_count', 0)
truck_area = st.session_state['truck_l'] * st.session_state['truck_w']
standard_box_area = 62 * 78  

# ==========================================
# 📥 分類品名與數量設定
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📥 品項數量設定")

regular_items = [item for item in st.session_state['items'] if item['type'] in ['regular', 'temp']]
categories = sorted(list(set(item['cat'] for item in regular_items)))

cat_colors = {
    "1. WET系列": "#FF6B6B", "2. LAM與DPS2系列": "#4D96FF", "3. IOS系列": "#6BCB77",
    "4. EX與EP系列": "#FF66B2", "5. ETTN/UCU系列": "#FFD93D", "6. 爐管與大型設備": "#B983FF",
    "7. 辛巳系列": "#FF9F45", "8. CUP系列": "#00ADB5", "9. 臨時自訂": "#9E9E9E"
}

for cat in categories:
    color = cat_colors.get(cat, "#4D96FF")
    st.markdown(f"<div style='border-left: 5px solid {color}; padding-left: 8px; margin-top: 14px; margin-bottom: 6px; font-weight: bold; color: {color};'>{cat}</div>", unsafe_allow_html=True)
    
    cat_items = [item for item in regular_items if item['cat'] == cat]
    for item in cat_items:
        idx = st.session_state['items'].index(item)
        
        # UX 優化：加入 vertical_alignment 置中對齊
        c_name, c_qty = st.columns([6, 4], vertical_alignment="center")
        with c_name:
            st.markdown(f"<b>{item['name']}</b> <span style='color: #aaa; font-size: 0.8em;'>({item['l']}x{item['w']}cm)</span>", unsafe_allow_html=True)
        with c_qty:
            item['qty'] = st.number_input("數量", value=item['qty'], min_value=0, step=1, key=f'qty_{idx}_v{r_id}', label_visibility="collapsed")
            
        if item["type"] == "temp":
            with st.expander("✏️ 調整尺寸與名稱"):
                item['name'] = st.text_input("品名", value=item['name'], key=f'edit_name_{idx}_v{r_id}')
                c1, c2 = st.columns(2)
                item['l'] = c1.number_input("長(cm)", value=item['l'], min_value=1, step=5, key=f'edit_l_{idx}_v{r_id}')
                item['w'] = c2.number_input("寬(cm)", value=item['w'], min_value=1, step=5, key=f'edit_w_{idx}_v{r_id}')
                
        st.markdown("<hr style='margin: 4px 0px; border: none; border-top: 1px solid #222;'>", unsafe_allow_html=True)

st.button("➕ 新增臨時自訂貨物", on_click=add_temp_item, use_container_width=True)

# ==========================================
# 📊 中段即時趴數面板
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
mid_progress_ph = st.empty()

# ==========================================
# 📦 已選貨物裝載設定區
# ==========================================
st.markdown("---")
st.subheader("📦 特殊裝載設定")

active_items = [item for item in st.session_state['items'] if item['qty'] > 0]

if active_items:
    for i, item in enumerate(active_items):
        if item.get('stacked_qty', 0) > item['qty']:
            item['stacked_qty'] = item['qty']
            
        c_name, c_skip, c_stack = st.columns([4, 3, 3], vertical_alignment="center")
        with c_name:
            st.markdown(f"<b>{item['name']}</b> <span style='color:#aaa; font-size:0.8em;'>({item['qty']}件)</span>", unsafe_allow_html=True)
        with c_skip:
            item['skip'] = st.checkbox("🚫不上車", value=item.get('skip', False), key=f'skip_{idx}_{i}_v{r_id}')
        with c_stack:
            item['stacked_qty'] = st.number_input(
                "疊上層數", value=item.get('stacked_qty', 0), min_value=0, max_value=item['qty'], 
                step=1, key=f"stack_{idx}_{i}_v{r_id}", label_visibility="collapsed"
            )
        st.markdown("<hr style='margin: 4px 0px; border: none; border-top: 1px dashed #444;'>", unsafe_allow_html=True)
else:
    st.info("請先在上方輸入貨物數量。")

# ==========================================
# 🧮 面積結算與安全判定
# ==========================================
regular_area = 0
total_pieces = 0
for item in st.session_state['items']:
    if item['qty'] > 0 and not item.get('skip', False):
        single = item['l'] * item['w']
        floor_qty = item['qty'] - item.get('stacked_qty', 0)
        regular_area += single * floor_qty
        total_pieces += item['qty']

total_pct = (regular_area / truck_area) * 100 if truck_area > 0 else 0
remaining_area = max(0, truck_area - regular_area)
remaining_boxes = math.floor(remaining_area / standard_box_area)

with mid_progress_ph.container():
    if total_pct > 100:
        st.error(f"🚨 **總佔用：{total_pct:.1f}% (已超載！)**")
    elif total_pct > 85:
        st.warning(f"⚠️ **總佔用：{total_pct:.1f}% (接近滿載)**")
    elif total_pct > 0:
        st.success(f"🟢 **總佔用：{total_pct:.1f}%**")
    else:
        st.info("🟢 **目前佔用：0.0%**")
    st.progress(min(total_pct / 100, 1.0))

# ==========================================
# 📊 最終建議與 Line 派車單
# ==========================================
st.markdown("---")
suggest_remove_lines = []

if total_pct > 100:
    st.error(f"🚨 **整車已超載！** 最終佔用達 **{total_pct:.1f}%**！")
    st.markdown("### 💡 建議留車明細：")
    
    disposable_items = []
    for item in st.session_state['items']:
        if item['qty'] > 0 and not item.get('skip', False):
            floor_qty = item['qty'] - item.get('stacked_qty', 0)
            if floor_qty > 0:  
                disposable_items.append({'name': item['name'], 'single_area': item['l'] * item['w'], 'max_qty': floor_qty})
            
    disposable_items.sort(key=lambda x: -x['single_area'])
    temp_excess = regular_area - truck_area
    
    for item in disposable_items:
        if item['single_area'] > 0:
            needed_drop = -(-int(temp_excess) // int(item['single_area'])) 
            drop_qty = min(needed_drop, item['max_qty'])
            
            if drop_qty > 0:
                st.warning(f"👉 建議拿掉 **{item['name']}** × {drop_qty} 件")
                suggest_remove_lines.append(f"👉 {item['name']} × {drop_qty} 件")
                temp_excess -= item['single_area'] * drop_qty
                if temp_excess <= 0: break

if regular_area > 0:
    st.subheader("📲 派車單匯出 (可直接複製)")
    
    manifest_lines, skipped_lines = [], []
    for item in st.session_state['items']:
        if item['qty'] > 0:
            if item.get('skip', False):
                skipped_lines.append(f"🚫 {item['name']} × {item['qty']} (不上車)")
            else:
                stack_str = f" [疊上層 {item['stacked_qty']} 件]" if item.get('stacked_qty', 0) > 0 else ""
                manifest_lines.append(f"✅ {item['name']} × {item['qty']}{stack_str}")
    
    report_text = f"🚚 【裝載派車單】\n📊 佔用率：{total_pct:.1f}%\n📦 出車總件數：{total_pieces} 件\n──────────────\n【📌 預計上車明細】\n" + "\n".join(manifest_lines) + "\n"
    
    if suggest_remove_lines:
        report_text += "──────────────\n【🚨 超過貨量，建議拿去明細】\n" + "\n".join(suggest_remove_lines) + "\n"
    if skipped_lines:
        report_text += "──────────────\n【⚠️ 已設定留車明細】\n" + "\n".join(skipped_lines) + "\n"
        
    st.code(report_text, language="text")

# ==========================================
# 💾 網址自動儲存機制
# ==========================================
save_data = [
    {'n': i['name'], 'q': i['qty'], 's': i.get('stacked_qty', 0), 'k': i.get('skip', False), 'l': i['l'], 'w': i['w'], 't': i['type'], 'c': i['cat']}
    for i in st.session_state['items'] if i['qty'] > 0 or i['type'] == 'temp'
]

if save_data:
    st.query_params["cart"] = urllib.parse.quote(json.dumps(save_data))
elif "cart" in st.query_params:
    del st.query_params["cart"]
