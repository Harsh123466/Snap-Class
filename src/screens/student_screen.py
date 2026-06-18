import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_background_dashboard, style_base_layout
import numpy as np
from PIL import Image


def student_screen():
    style_background_dashboard()
    style_base_layout()

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xlarge')

    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home', type='secondary', key='loginbackbtn', shortcut='control+backspace'):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("""
<h2 style="color:black; text-align: center;">Login using password
</h2>
""", unsafe_allow_html=True)
    
    st.space()
    st.space()

    st.markdown("""
<h2 style="color:black; text-align: center;">Login using FaceId
</h2>
""", unsafe_allow_html=True)
    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        np.array(Image.open(photo_source))