import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from rectpack import newPacker, PackingBin, SORT_NONE

# === 新增：解決畫圖中文顯示變成方塊的問題 ===
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'PingFang TC', 'SimHei'] # 設定字體為微軟正黑體
plt.rcParams['axes.unicode_minus'] = False
# =========================================

# 1. 初始化系統狀態
def init_state():
    st.session_state['truck_l'] = 300
    st.session_state['truck_w'] = 150
    st.session_state['items'] = [
        {"name": "常規紙箱A", "l": 60, "w": 50, "qty": 0, "priority": True, "type": "regular"},
        {"name": "常規紙箱B", "l": 80, "w": 50, "qty": 0, "priority": False, "type": "regular"}
    ]

if 'items' not in st.session_state:
    init_state()

def add_regular_item():
    st.session_state['items'].append({"name": "新常規貨物", "l": 50, "w": 50, "qty": 0, "priority": False, "type": "regular"})

def add_temp_item():
    st.session_state['items'].append({"name": "臨時新增貨物", "l": 50, "w": 50, "qty": 1, "priority": False, "type": "temp"})

def reset_all():
    new_items = []
    for item in st.session_state['items']:
        if item['type'] == 'regular':
            item['qty'] = 0
            new_items.append(item)
    st.session_state['items'] = new_items

# 2. 介面設計
st.set_page_config(page_title="貨車裝箱計算器", layout="centered")
st.title("📦 貨車裝箱計算器")

with st.expander("🚚 1. 設定車斗尺寸", expanded=False):
    col1, col2 = st.columns(2)
    st.session_state['truck_l'] = col1.number_input("車斗長度 (cm)", value=st.session_state['truck_l'], step=10)
    st.session_state['truck_w'] = col2.number_input("車斗寬度 (cm)", value=st.session_state['truck_w'], step=10)

st.subheader("📥 2. 貨物清單設定")

col_add_reg, col_add_temp = st.columns(2)
col_add_reg.button("➕ 新增常規尺寸", on_click=add_regular_item, use_container_width=True)
col_add_temp.button("➕ 新增臨時貨物", on_click=add_temp_item, use_container_width=True)
st.markdown("---")

for i, item in enumerate(st.session_state['items']):
    with st.container():
        type_label = "📍" if item["type"] == "regular" else "⚠️ (臨時)"
        st.markdown(f"**{type_label} 貨物 {i+1}**")
        item['name'] = st.text_input("品名", value=item['name'], key=f"name_{i}")
        
        c1, c2, c3 = st.columns(3)
        item['l'] = c1.number_input("長(cm)", value=item['l'], min_value=1, step=5, key=f"l_{i}")
        item['w'] = c2.number_input("寬(cm)", value=item['w'], min_value=1, step=5, key=f"w_{i}")
        item['qty'] = c3.number_input("數量", value=item['qty'], min_value=0, step=1, key=f"qty_{i}")
        
        item['priority'] = st.checkbox("⭐ 優先放車頭最裡面", value=item['priority'], key=f"pri_{i}")
        st.divider()

st.button("🔄 一鍵清空重置", on_click=reset_all, type="primary", use_container_width=True)

# 3. 核心運算與繪圖邏輯
if st.button("▶️ 開始計算排版", type="primary", use_container_width=True):
    packer = newPacker(sort_algo=SORT_NONE, bin_algo=PackingBin.BFF)
    packer.add_bin(st.session_state['truck_l'], st.session_state['truck_w'])
    
    total_items = {}
    rectangles_to_pack = []
    
    for idx, item in enumerate(st.session_state['items']):
        if item['qty'] > 0:
            total_items[idx] = {'name': item['name'], 'req': item['qty'], 'packed': 0}
            for _ in range(item['qty']):
                rectangles_to_pack.append((item['l'], item['w'], idx, item['priority']))
    
    rectangles_to_pack.sort(key=lambda x: (not x[3], -(x[0]*x[1])))
    
    for r in rectangles_to_pack:
        packer.add_rect(r[0], r[1], r[2])
        
    packer.pack()
    
    # 4. 統計與顯示結果
    if len(packer) > 0:
        bin_data = packer[0]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_xlim(0, st.session_state['truck_l'])
        ax.set_ylim(0, st.session_state['truck_w'])
        ax.add_patch(patches.Rectangle((0, 0), st.session_state['truck_l'], st.session_state['truck_w'], fill=False, lw=3))
        
        colors = ['#e15759', '#4e79a7', '#f28e2b', '#76b7b2', '#59a14f', '#edc949']
        
        for rect in bin_data:
            x, y, w, h, rid = rect.x, rect.y, rect.width, rect.height, rect.rid
            total_items[rid]['packed'] += 1
            color = colors[rid % len(colors)]
            
            ax.add_patch(patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='white', facecolor=color))
            ax.text(x + w/2, y + h/2, f"{total_items[rid]['name']}\n{w}x{h}", 
                    ha='center', va='center', color='white', fontsize=8, fontweight='bold')
            
        ax.set_title("裝載俯視圖 (左側為車頭)")
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