"""
CurricuLab AI - Intelligent Curriculum Design Platform
Landing page with role selection
"""
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="CurricuLab AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

from src.utils.theme import apply_theme

# Apply custom theme
apply_theme()

# Initialize session state
if 'role' not in st.session_state:
    st.session_state['role'] = None

# Header with Logo
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown('<h1 class="app-title">CurricuLab AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="app-subtitle">Intelligent Curriculum Design Platform</p>', unsafe_allow_html=True)

with header_col2:
    try:
        st.image("src/assets/logo.png", use_container_width=True)
    except Exception as e:
        # Fallback if image not found
        pass

# Role Selection Section
st.markdown('<p class="role-label">Choose Workspace</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button("Student", use_container_width=True):
        st.session_state['role'] = 'student'
        st.switch_page("pages/Student_Dashboard.py")

with col2:
    if st.button("Professor", use_container_width=True):
        st.session_state['role'] = 'professor'
        st.switch_page("pages/Professor_Dashboard.py")
