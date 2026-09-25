import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import os
# 【換回最暴力的左下角重力引擎 MaxRectsBl】
from rectpack import newPacker, PackingBin, SORT_NONE, MaxRectsBl

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

# 【完美修復：一鍵清空邏輯】強制刪除網頁暫存元件記憶體，確保完全歸零
def reset_all():
    # 1. 清除 UI 輸入框的記憶體綁定
    for key in list(st.session_state.keys()):
        if str(key).startswith('qty_') or str(key).startswith('edit_'):
            del st.session_state[key]
            
    # 2. 清除資料庫裡的數量
    for item in st.session_state['items']:
        if item['type'] == 'regular':
            item['qty'] = 0

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
        # 當清除按鈕觸發 del st.session_state[key] 後，這裡會重新抓取 value=item['qty']，也就是 0
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

# 3. 核心運算
if calc_btn:
    # 解開旋轉封印 (rotation=True) + 強制使用死命靠左下的 MaxRectsBl
    packer = newPacker(rotation=True, sort_algo=SORT_NONE, bin_algo=PackingBin.BFF, pack_algo=MaxRectsBl)
    packer.add_bin(st.session_state['truck_l'], st.session_state['truck_w']) 
    
    total_items = {}
    rectangles_to_pack = []
    
    for idx, item in enumerate(st.session_state['items']):
        if item['qty'] > 0:
            total_items[idx] = {'name': item['name'], 'req': item['qty'], 'packed': 0}
            for _ in range(item['qty']):
                # 直接餵給系統長寬，讓系統自己像玩俄羅斯方塊一樣轉動尋找最佳解
                rectangles_to_pack.append({
                    'l': item['l'], 
                    'w': item['w'], 
                    'rid': idx, 
                    'pri': item['priority'],
                    'name': item['name']
                })
    
    # 【完美理貨排序法】：
    # 1. 優先級 (打勾放車頭)
    # 2. 面積越大越先放 (大箱先堆疊)
    # 3. 長邊越長越先放 (建立牆壁)
    # 4. 同品名連續放 (幫助系統把一樣的箱子排在一起)
    rectangles_to_pack.sort(key=lambda x: (-x['pri'], -(x['l']*x['w']), -max(x['l'], x['w']), x['name']))
    
    for r in rectangles_to_pack:
        packer.add_rect(r['l'], r['w'], r['rid'])
        
    packer.pack()
    
    if len(packer) > 0:
        bin_data = packer[0]
        fig, ax = plt.subplots(figsize=(12, 4)) 
        ax.set_xlim(0, st.session_state['truck_l'])
        ax.set_ylim(0, st.session_state['truck_w'])
        ax.set_aspect('equal')
        
        ax.add_patch(patches.Rectangle((0, 0), st.session_state['truck_l'], st.session_state['truck_w'], fill=False, lw=3))
        
        colors = ['#e15759', '#4e79a7', '#f28e2b', '#76b7b2', '#59a14f', '#edc949', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ac']
        
        for rect in bin_data:
            x, y, w, h, rid = rect.x, rect.y, rect.width, rect.height, rect.rid
            
            total_items[rid]['packed'] += 1
            color = colors[rid % len(colors)]
            
            ax.add_patch(patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='white', facecolor=color))
            ax.text(x + w/2, y + h/2, f"{total_items[rid]['name']}\n{w}x{h}", 
                    ha='center', va='center', color='white', fontsize=8, fontweight='bold')
            
        ax.set_title("裝載俯視圖 (強迫無縫填滿 + 小箱補洞)")
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
