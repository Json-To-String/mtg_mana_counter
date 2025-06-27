import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="MTG Mana Tracker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'mana_counters' not in st.session_state:
    st.session_state.mana_counters = {
        'White': 0,
        'Blue': 0,
        'Black': 0,
        'Red': 0,
        'Green': 0,
        'Colorless': 0
    }

if 'undo_history' not in st.session_state:
    st.session_state.undo_history = []

def save_undo_state(action_description):
    current_state = st.session_state.mana_counters.copy()
    st.session_state.undo_history.append({
        'state': current_state,
        'action': action_description
    })
    # Keep only last 10 actions to prevent memory issues
    if len(st.session_state.undo_history) > 10:
        st.session_state.undo_history.pop(0)

def undo_last_action():
    if st.session_state.undo_history:
        last_state = st.session_state.undo_history.pop()
        st.session_state.mana_counters = last_state['state']
        return last_state['action']
    return None

st.markdown("""
<style>
    /* Mobile-first responsive design */
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px;
        margin: 0.25rem 0;
    }
    
    /* Make counter displays larger on mobile */
    .big-counter {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    /* Compact spacing on mobile */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
        .stButton > button {
            height: 2.5rem;
            font-size: 1rem;
        }
        
        .big-counter {
            font-size: 1.5rem;
            padding: 0.5rem;
        }
    }
    
    /* Hide streamlit menu and footer on mobile */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Shortcut buttons styling */
    .stButton button[data-testid*="add5"], 
    .stButton button[data-testid*="add10"] {
        background-color: rgba(0, 123, 255, 0.1);
        border: 1px solid rgba(0, 123, 255, 0.3);
        color: #007bff;
    }
    
    .stButton button[data-testid*="add5"]:hover, 
    .stButton button[data-testid*="add10"]:hover {
        background-color: rgba(0, 123, 255, 0.2);
    }
    
    /* Better spacing */
    .element-container {
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

color_styles = {
    'White': '#FFFBD5',
    'Blue': '#0E68AB',
    'Black': '#150B00',
    'Red': '#D3202A',
    'Green': '#00733E',
    'Colorless': '#CAC5C0'
}

chart_colors = {
    'White': '#FFF2CC',
    'Blue': '#1f77b4',
    'Black': '#2F2F2F',
    'Red': '#d62728',
    'Green': '#2ca02c',
    'Colorless': '#7f7f7f'
}

st.title("MTG mana Tracker")

cols = st.columns([1, 1])  # Always 2 columns for better mobile experience

for i, (color, count) in enumerate(st.session_state.mana_counters.items()):
    col_idx = i % 2  # Use 2 columns instead of 3 for mobile
    
    with cols[col_idx]:
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
        
        st.markdown(f"<div class='big-counter'>{count}</div>", unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button(f"➖ Remove", key=f"sub_{color}", help=f"Remove 1 {color} mana"):
                if st.session_state.mana_counters[color] > 0:
                    save_undo_state(f"Removed 1 {color} mana")
                    st.session_state.mana_counters[color] -= 1
                    st.rerun()
        
        with btn_col2:
            if st.button(f"➕ Add", key=f"add_{color}", help=f"Add 1 {color} mana"):
                save_undo_state(f"Added 1 {color} mana")
                st.session_state.mana_counters[color] += 1
                st.rerun()
        
        shortcut_col1, shortcut_col2 = st.columns(2)
        
        with shortcut_col1:
            if st.button(f"➕5", key=f"add5_{color}", help=f"Add 5 {color} mana"):
                save_undo_state(f"Added 5 {color} mana")
                st.session_state.mana_counters[color] += 5
                st.rerun()
        
        with shortcut_col2:
            if st.button(f"➕10", key=f"add10_{color}", help=f"Add 10 {color} mana"):
                save_undo_state(f"Added 10 {color} mana")
                st.session_state.mana_counters[color] += 10
                st.rerun()
        
        st.markdown("---")

st.markdown("### 🎮 Controls")
control_col1, control_col2, control_col3 = st.columns([1, 1, 1])

with control_col1:
    if st.button("🔄 Reset All", type="primary", help="Reset all mana counters to 0"):
        save_undo_state("Reset all counters")
        for color in st.session_state.mana_counters:
            st.session_state.mana_counters[color] = 0
        st.rerun()

with control_col2:
    # Undo button
    if st.session_state.undo_history:
        last_action = st.session_state.undo_history[-1]['action']
        if st.button("↩️ Undo", help=f"Undo: {last_action}"):
            undone_action = undo_last_action()
            st.success(f"Undid: {undone_action}")
            st.rerun()
    else:
        st.button("↩️ Undo", disabled=True, help="No actions to undo")

with control_col3:
    total_mana = sum(st.session_state.mana_counters.values())
    st.metric("Total mana", total_mana, help="Sum of all mana counters")

st.markdown("---")
st.markdown("*Tap **➕ Add** or **➖ Remove** for single mana changes. Use **➕5** and **➕10** for shortcuts. **↩️ Undo** reverses your last action.*")

with st.expander("📊 mana Breakdown", expanded=True):
    if total_mana > 0:
        df = pd.DataFrame({
            'Color': list(st.session_state.mana_counters.keys()),
            'mana': list(st.session_state.mana_counters.values())
        })
        
        df_filtered = df[df['mana'] > 0]
        
        if not df_filtered.empty:
            colors = [chart_colors[color] for color in df_filtered['Color']]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=df_filtered['Color'],
                    y=df_filtered['mana'],
                    marker_color=colors,
                    text=df_filtered['mana'],
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>mana: %{y}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title="mana Distribution",
                xaxis_title="Color",
                yaxis_title="mana Count",
                showlegend=False,
                height=350,  # Shorter height for mobile
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                transition_duration=500,
                yaxis=dict(range=[0, max(df['mana']) + 1]),
                margin=dict(l=20, r=20, t=40, b=20),  # Tighter margins for mobile
                font=dict(size=12)  # Readable font size on mobile
            )
            
            fig.update_traces(
                marker_line_color='rgb(8,48,107)',
                marker_line_width=1.5,
                opacity=0.8
            )
            
            st.plotly_chart(fig, use_container_width=True, key="mana_chart")
        else:
            st.info("Add some mana counters to see the chart!")
    else:
        st.info("No mana counters active - add some mana to see the breakdown!")