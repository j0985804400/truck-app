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
        {"name": "333", "l": 150, "w": 150, "qty": 0, "priority": True, "type": "regular", "rotate": False},
        {"name": "LAM", "l": 1, "w": 1, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "EX2", "l": 60, "w": 67, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "WET", "l": 62, "w": 78, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "WET長箱", "l": 102, "w": 52, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "ETTN", "l": 65, "w": 95, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "DPS2", "l": 80, "w": 126, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "UCU", "l": 61, "w": 106, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "ICP", "l": 1, "w": 1, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "APC", "l": 1, "w": 1, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "IOS大", "l": 122, "w": 80, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "IOS小", "l": 102, "w": 80, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "爐管方型", "l": 70, "w": 70, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "辛巳大", "l": 76, "w": 56, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "辛巳小", "l": 70, "w": 46, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "SDRM", "l": 67, "w": 56, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "CUP", "l": 90, "w": 56, "qty": 0, "priority": False, "type": "regular", "rotate": False},
        {"name": "CUP SOD", "l": 80, "w": 50, "qty": 0, "priority": False, "type": "regular", "rotate": False}
    ]

if 'items' not in st.session_state:
    init_state()

def add_temp_item():
    st.session_state['items'].append({
        "name": "臨時新增", "l": 50, "w": 50, "qty": 1, "priority": False, "type": "temp", "rotate": False
    })

# 徹底清除 UI 暫存記憶體與歸零
def reset_all():
    for key in list(st.session_state.keys()):
        if str(key).startswith('qty_') or str(key).startswith('edit_') or str(key).startswith('rot_'):
            del st.session_state[key]
            
    for item in st.session_state['items']:
        if item['type'] == 'regular':
            item['qty'] = 0
            item['rotate'] = False

st.set_page_config(page_title="貨車裝箱計算器", layout="centered")
st.title("📦 貨車裝箱計算器 (手動排版版)")

st.markdown(f"<p style='color: gray; margin-bottom: 5px;'>🚚 目前車斗規格：寬 {st.session_state['truck_w']} cm × 長 {st.session_state['truck_l']} cm (直立俯視)</p>", unsafe_allow_html=True)

# === 1. 即時面積防爆防線 (精準數學換算) ===
truck_area = st.session_state['truck_l'] * st.session_state['truck_w']
total_item_area = sum(item['l'] * item['w'] * item['qty'] for item in st.session_state['items'])
usage_pct = (total_item_area / truck_area) * 100 if truck_area > 0 else 0

if usage_pct > 100:
    st.error(f"🚨 **面積超載！** 目前總面積佔用達 {usage_pct:.1f}% (已超越車斗極限，絕對載不下)")
elif usage_pct > 85:
    st.warning(f"⚠️ **非常極限！** 面積佔用 {usage_pct:.1f}% (接近滿載，需注意實際擺放縫隙)")
elif usage_pct > 0:
    st.info(f"🟢 **面積初估安全**：目前佔用 {usage_pct:.1f}%")

if usage_pct > 0:
    st.progress(min(usage_pct / 100, 1.0))

st.markdown("---")
st.subheader("📥 貨物數量與方向設定")

for i, item in enumerate(st.session_state['items']):
    col_info, col_qty, col_rot = st.columns([4.5, 3.0, 2.5])
    
    with col_info:
        icon = "📍" if item["type"] == "regular" else "⚠️"
        pri_text = "⭐" if item["priority"] else ""
        st.markdown(f"<div style='margin-top: 10px;'><b>{icon} {item['name']}</b> {pri_text}<br><span style='font-size:0.75em; color:gray;'>({item['l']}x{item['w']})</span></div>", unsafe_allow_html=True)
    
    with col_qty:
        item['qty'] = st.number_input("數量", value=item['qty'], min_value=0, step=1, key=f"qty_{i}", label_visibility="collapsed")
        
    with col_rot:
        if item['qty'] > 0:
            # 讓你可以手動切換直放或橫放
            rot_label = "橫放旋轉" if not item.get('rotate', False) else "恢復直放"
            if st.button(rot_label, key=f"rot_{i}"):
                item['rotate'] = not item.get('rotate', False)
                st.rerun()
    
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
    if st.button("🔄 一鍵清空數量", use_container_width=True):
        reset_all()
        st.rerun()

st.markdown("---")
st.subheader("🗺️ 直立車斗即時預覽圖 (下方為車頭)")

# === 2. 直立車斗視覺呈現 (依照數量與方向依序排入) ===
fig, ax = plt.subplots(figsize=(6, 14))
truck_w = st.session_state['truck_w']
truck_l = st.session_state['truck_l']

ax.set_xlim(0, truck_w)
ax.set_ylim(0, truck_l)
ax.set_aspect('equal')

# 畫出車斗外框 (寬 243, 長 820)
ax.add_patch(patches.Rectangle((0, 0), truck_w, truck_l, fill=False, lw=3, edgecolor='black'))

colors = ['#e15759', '#4e79a7', '#f28e2b', '#76b7b2', '#59a14f', '#edc949', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ac']

# 簡單的順序流排模擬：從車頭 (y=0) 開始依序往車尾擺放
curr_x = 0
curr_y = 0
row_max_h = 0

has_items = False
for idx, item in enumerate(st.session_state['items']):
    if item['qty'] > 0:
        has_items = True
        # 根據是否旋轉決定實際佔用的寬與長
        box_w = item['w'] if item.get('rotate', False) else item['l'] # 對應 X 軸 (車寬方向)
        box_h = item['l'] if item.get('rotate', False) else item['w'] # 對應 Y 軸 (車長方向)
        color = colors[idx % len(colors)]
        
        for _ in range(item['qty']):
            # 如果超過車寬，換到下一排
            if curr_x + box_w > truck_w:
                curr_x = 0
                curr_y += row_max_h
                row_max_h = 0
                
            # 如果超出車長極限
            if curr_y + box_h > truck_l:
                break
                
            ax.add_patch(patches.Rectangle((curr_x, curr_y), box_w, box_h, linewidth=1, edgecolor='white', facecolor=color))
            ax.text(curr_x + box_w/2, curr_y + box_h/2, f"{item['name']}\n{box_w}x{box_h}", 
                    ha='center', va='center', color='white', fontsize=8, fontweight='bold')
            
            row_max_h = max(row_max_h, box_h)
            curr_x += box_w

ax.set_title("直立車斗示意圖 (底部為車頭)")
ax.set_xlabel("車斗寬度 (cm)")
ax.set_ylabel("車斗長度 (cm)")
st.pyplot(fig)

if not has_items:
    st.info("💡 請在上方輸入貨物數量，圖表即時為您呈現視覺配置。")
