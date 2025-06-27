import streamlit as st

# Initialize session state for mana counters
if 'mana_counters' not in st.session_state:
    st.session_state.mana_counters = {
        'White': 0,
        'Blue': 0,
        'Black': 0,
        'Red': 0,
        'Green': 0,
        'Colorless': 0
    }

# App title
st.title(" Magic Mana Tracker")
st.markdown("---")

# Color mapping for styling
color_styles = {
    'White': '#FFFBD5',
    'Blue': '#0E68AB',
    'Black': '#150B00',
    'Red': '#D3202A',
    'Green': '#00733E',
    'Colorless': '#CAC5C0'
}

# Create columns for layout
cols = st.columns(3)

for i, (color, count) in enumerate(st.session_state.mana_counters.items()):
    col_idx = i % 3
    
    with cols[col_idx]:
        # Color header with styling
        if color == 'White':
            st.markdown(f"### ⚪ {color}")
        elif color == 'Blue':
            st.markdown(f"### 🔵 {color}")
        elif color == 'Black':
            st.markdown(f"### ⚫ {color}")
        elif color == 'Red':
            st.markdown(f"### 🔴 {color}")
        elif color == 'Green':
            st.markdown(f"### 🟢 {color}")
        else:  # Colorless
            st.markdown(f"### ⚪ {color}")
        
        st.markdown(f"**Mana: {count}**")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button(f"➖", key=f"sub_{color}"):
                if st.session_state.mana_counters[color] > 0:
                    st.session_state.mana_counters[color] -= 1
                    st.rerun()
        
        with col2:
            st.markdown(f"<div style='text-align: center; font-size: 24px; font-weight: bold;'>{count}</div>", 
                       unsafe_allow_html=True)
        
        with col3:
            if st.button(f"➕", key=f"add_{color}"):
                st.session_state.mana_counters[color] += 1
                st.rerun()
        
        st.markdown("---")

st.markdown("### Controls")
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🔄 Reset All", type="primary"):
        for color in st.session_state.mana_counters:
            st.session_state.mana_counters[color] = 0
        st.rerun()

with col2:
    total_mana = sum(st.session_state.mana_counters.values())
    st.metric("Total mana", total_mana)

st.markdown("---")
st.markdown("*Click ➕ to add mana, ➖ to subtract mana, or Reset All to clear all counters.*")

with st.expander("mana Breakdown"):
    for color, count in st.session_state.mana_counters.items():
        if count > 0:
            st.write(f"{color}: {count}")
    if total_mana == 0:
        st.write("No mana counters active")