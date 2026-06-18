import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_background_dashboard, style_base_layout
import numpy as np
from PIL import Image
from src.pipelines.face_pipeline import predict_attendance
from src.database.db import get_all_students
import time



def student_dashboard():
    st.markdown("""
<h2 style="color:black; text-align: center;">DASHBOARD HERE 
</h2>
""", unsafe_allow_html=True)



def student_screen():
    style_background_dashboard()
    style_base_layout()

    if 'student_data' in st.session_state:
        student_dashboard()

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
        img = np.array(Image.open(photo_source))

        with st.spinner('AI is scanning...'):
            detected, all_idx, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('Face not found')
            elif num_faces > 1:
                st.warning('Multiple faces found')
            else:
                if detected:
                    student_id = list(detected.key())[0]
                    all_students = get_all_students()

                    student = next((s for s in all_students if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.info('Face not recognized! you might be a new student!')
                        