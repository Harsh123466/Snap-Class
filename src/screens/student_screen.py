import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_background_dashboard, style_base_layout
import numpy as np
from PIL import Image
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student
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
        return

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xlarge')

    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home', type='secondary', key='loginbackbtn', shortcut='control+backspace'):
            st.session_state['login_type'] = None
            st.rerun()

#     st.markdown("""
# <h2 style="color:black; text-align: center;">Login using password
# </h2>
# """, unsafe_allow_html=True)
    
    # st.space()
    st.space()

    st.markdown("""
<h2 style="color:black; text-align: center;">Login using FaceId
</h2>
""", unsafe_allow_html=True)
    
    show_registration = False
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
                    student_id = list(detected.keys())[0]
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
                        show_registration = True
                else:
                    if len(all_idx) == 0:
                        st.info("No students are registered yet. Please create your profile.")
                    else:
                        st.info('Face not recognized! you might be a new student!')
                    show_registration = True

    if show_registration:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder="e.g. Harsh Adhana")

            st.subheader('Optional : Voice Enrollment')
            st.info('Enroll your voice for only attendance')

            audio_data = None

            try:
                audio_data = st.audio_input('Record a short phrase for 10 sec like My name is Harsh, I am present ....')
            except Exception:
                st.error('Audio Data failed')

            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner('Creating profile....'):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)

                        if len(encodings) != 1:
                            st.error('Could not capture exactly one face for registration')
                        else:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile Created! Hi, {new_name}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error('Could not create your profile')

                else:
                    st.warning('Please enter your name!')

                        
