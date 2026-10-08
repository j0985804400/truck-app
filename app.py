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

if 'items' not in st.
