import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import os

# === 字型設定 ===
font_path = "NotoSansTC-VariableFont_wght.ttf"
if os.path.exists(font_path):
    fe = fm.FontEntry(fname=font_path, name='CustomFont')
    fm.fontManager.ttflist.insert(0, fe)
    plt.rcParams['font.family'] = ['CustomFont']
else:
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'PingFang TC', 'SimHei']

plt.rcParams['axes.unicode_minus'] = False

def init_state():
    st.session_state['truck_l'] = 820
    st.session_state['truck_w'] = 243
    
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
    new_items = []
    for item in st.session_state['items']:
        if item['type'] == 'regular':
            item['qty'] = 0
            new_items.append(item)
    st.session_state['items'] = new_items

# 1. 介面設定
st.set_page_config(page_title="貨車裝箱計算器", layout="centered")
st.title("📦 貨車裝箱計算器")

st.markdown(f"<p style='color: gray; margin-bottom: 5px;'>🚚 目前車斗規格：長 {st.session_state['truck_l']} cm × 寬 {st.session_state['truck_w']} cm</p>", unsafe_allow_html=True)

# === 即時面積初估 ===
truck_area = st.session_state['truck_l'] * st.session_state['truck_w']
total_item_area = sum(item['l'] * item['w'] * item['qty'] for item in st.session_state['items'])
usage_pct = (total_item_area / truck_area) * 100 if truck_area > 0 else 0

if usage_pct > 100:
    st.error(f"🚨 **絕對載不下！** 貨物總面積已達 {usage_pct:.1f}% (超過車斗極限)")
elif usage_pct > 85:
    st.warning(f"⚠️ **非常極限！** 面積佔用 {usage_pct:.1f}% (可能因縫隙而裝不下，建議按計算排版確認)")
elif usage_pct > 0:
    st.info(f"🟢 **面積初估安全**：目前佔用 {usage_pct:.1f}%")

if usage_pct > 0:
    st.progress(min(usage_pct / 100, 1.0))

st.markdown("---")
st.subheader("📥 貨物數量設定")

for i, item in enumerate(st.session_state['items']):
    col_info, col_qty = st.columns([6.5, 3.5])
    
    with col_info:
        icon = "📍" if item["type"] == "regular" else "⚠️"
        pri_text = "⭐" if item["priority"] else ""
        st.markdown(f"<div style='margin-top: 12px;'><b>{icon} {item['name']}</b> {pri_text} <span style='font-size:0.8em; color:gray;'>({item['l']}x{item['w']})</span></div>", unsafe_allow_html=True)
    
    with col_qty:
        item['qty'] = st.number_input("數量", value=item['qty'], min_value=0, step=1, key=f"qty_{i}", label_visibility="collapsed")
    
    if item["type"] == "temp":
        with st.expander("✏️ 調整臨時貨物設定"):
            item['name'] = st.text_input("品名", value=item['name'], key=f"edit_name_{i}")
            c1, c2 = st.columns(2)
            item['l'] = c1.number_input("長(cm)", value=item['l'], min_value=1, step=5, key=f"edit_l_{i}")
            item['w'] = c2.number_input("寬(cm)", value=item['w'], min_value=1, step=5, key=f"edit_w_{i}")
            item['priority'] = st.checkbox("⭐ 優先放車頭", value=item['priority'], key=f"edit_pri_{i}")
            
    st.markdown("<hr style='margin: 4px 0px; border: none; border-top: 1px solid #eee;'>", unsafe_allow_html=True)

st.button("➕ 新增臨時貨物", on_click=add_temp_item, use_container_width=True)
st.markdown("<br>", unsafe_allow_html=True)

b1, b2 = st.columns(2)
with b1:
    calc_btn = st.button("▶️ 開始計算排版", type="primary", use_container_width=True)
with b2:
    st.button("🔄 一鍵清空數量", on_click=reset_all, use_container_width=True)

# 3. 核心運算：完全自製的「人類築牆式排版 (Shelf Packing)」
if calc_btn:
    truck_w = st.session_state['truck_w']
    truck_l = st.session_state['truck_l']
    
    total_items = {}
    boxes_to_pack = []
    
    # 計算最佳方向並準備箱子
    for idx, item in enumerate(st.session_state['items']):
        if item['qty'] > 0:
            total_items[idx] = {'name': item['name'], 'req': item['qty'], 'packed': 0}
            w1, w2 = item['l'], item['w']
            
            fit_1, waste_1 = truck_w // w1, truck_w % w1
            fit_2, waste_2 = truck_w // w2, truck_w % w2
            
            if fit_1 == 0 and fit_2 == 0: best_w, best_l = w1, w2
            elif fit_1 == 0: best_w, best_l = w2, w1
            elif fit_2 == 0: best_w, best_l = w1, w2
            elif waste_1 < waste_2: best_w, best_l = w1, w2
            elif waste_2 < waste_1: best_w, best_l = w2, w1
            else: best_w, best_l = (w1, w2) if w2 < w1 else (w2, w1)
                
            for _ in range(item['qty']):
                boxes_to_pack.append({
                    'w': best_w, 
                    'l': best_l, 
                    'rid': idx, 
                    'pri': item['priority'],
                    'name': item['name']
                })
    
    # 【關鍵排序】優先級別 > 箱子深度(長度) > 寬度。這保證了長度一樣的箱子絕對會被排在同一列！
    boxes_to_pack.sort(key=lambda x: (-x['pri'], -x['l'], -x['w']))
    
    bin_data = []
    current_x = 0  # 記錄當前排在車深的位置
    current_y = 0  # 記錄當前排已使用的寬度
    current_max_l = 0 # 記錄當前排最深(長)的尺寸
    
    for box in boxes_to_pack:
        placed = False
        
        # 1. 嘗試將箱子加入目前的排
        # 條件：車寬還有空間 + (如果是新排則沒限制，否則箱子長度不能超過這排的基準深度)
        can_fit_width = (current_y + box['w'] <= truck_w)
        can_fit_length = (current_max_l == 0 or box['l'] <= current_max_l)
        
        if can_fit_width and can_fit_length:
            if current_max_l == 0:
                current_max_l = box['l']
            
            if current_x + current_max_l <= truck_l:
                bin_data.append({'x': current_x, 'y': current_y, 'l': box['l'], 'w': box['w'], 'rid': box['rid']})
                current_y += box['w']
                total_items[box['rid']]['packed'] += 1
                placed = True
                
        # 2. 目前的排滿了，或是箱子太長會突出去，直接在後面開新的一排
        if not placed:
            if current_max_l > 0:
                current_x += current_max_l
                
            current_y = 0
            current_max_l = box['l']
            
            if current_x + current_max_l <= truck_l and box['w'] <= truck_w:
                bin_data.append({'x': current_x, 'y': current_y, 'l': box['l'], 'w': box['w'], 'rid': box['rid']})
                current_y += box['w']
                total_items[box['rid']]['packed'] += 1
    
    # 畫圖邏輯
    if len(bin_data) > 0:
        fig, ax = plt.subplots(figsize=(12, 4)) 
        ax.set_xlim(0, st.session_state['truck_l'])
        ax.set_ylim(0, st.session_state['truck_w'])
        ax.set_aspect('equal')
        
        ax.add_patch(patches.Rectangle((0, 0), st.session_state['truck_l'], st.session_state['truck_w'], fill=False, lw=3))
        
        colors = ['#e15759', '#4e79a7', '#f28e2b', '#76b7b2', '#59a14f', '#edc949', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ac']
        
        for rect in bin_data:
            x, y, l, w, rid = rect['x'], rect['y'], rect['l'], rect['w'], rect['rid']
            color = colors[rid % len(colors)]
            
            ax.add_patch(patches.Rectangle((x, y), l, w, linewidth=1, edgecolor='white', facecolor=color))
            ax.text(x + l/2, y + w/2, f"{total_items[rid]['name']}\n{l}x{w}", 
                    ha='center', va='center', color='white', fontsize=8, fontweight='bold')
            
        ax.set_title("裝載俯視圖 (左側為車頭，啟用完全人類築牆排版)")
        ax.set_xlabel("車斗長度 (cm)")
        ax.set_ylabel("車斗寬度 (cm)")
        st.pyplot(fig)
        
        st.success("✅ 成功裝載清單")
        for k, v in total_items.items():
            if v['packed'] > 0:
                st.write(f"- {v['name']}：{v['packed']} 件")
                
        unpacked_exist = any(v['req'] > v['packed'] for v in total_items.values())
        if unpacked_exist:
            st.error("❌ 超出未裝載清單 (請確認是否分車)")
            for k, v in total_items.items():
                if v['req'] > v['packed']:
                    st.write(f"- {v['name']}：剩 {v['req'] - v['packed']} 件未裝入")
    else:
        st.warning("沒有貨物被裝載，請檢查尺寸或數量是否正確。")
