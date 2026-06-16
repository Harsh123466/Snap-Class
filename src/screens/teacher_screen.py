import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login

def teacher_screen():
    
    style_background_dashboard()
    style_base_layout()

    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == 'login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type == 'register':
        teacher_screen_register()



def teacher_screen_login():
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
    
    teacher_username = st.text_input("Enter username", placeholder="ananyaSharma")

    teacher_pass = st.text_input("Enter password", placeholder="Enter your password", type='password')

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Login', type='secondary', icon=':material/login:', shortcut='control+enter', width='stretch'):
            if teacher_login(teacher_username, teacher_pass):
                st.toast("Welcome back!", icon='👋')
                import time
                time.sleep(1)
                st.rerun()
            else: st.error("Invalid username and password")
    with btnc2:
        if st.button('Register', type='primary', icon=':material/person_add:', shortcut='control+enter', width='stretch'):
            st.session_state.teacher_login_type = 'register'



def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "ALL fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username is already exists"
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"
    
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully Created Login Now"
    except Exception as e:
        print(e)
        return False, "Unexpected Error"


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xlarge')

    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home', type='secondary', key='registerbackbtn', shortcut='control+backspace'):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("""
<h2 style="color:black; text-align: center;">Register your teacher profile
</h2>
""", unsafe_allow_html=True)
    
    st.space()
    st.space()
    
    teacher_username = st.text_input("Enter username", placeholder="ananyaSharma")

    teacher_name = st.text_input("Enter name", placeholder="Ananya Sharma")

    teacher_pass = st.text_input("Enter password", placeholder="Enter your password", type='password')

    teacher_pass_confirm = st.text_input("Confirm your password", placeholder="Enter your password again", type='password')

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Register now', type='secondary', icon=':material/login:', shortcut='control+enter', width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else: st.error(message)

    with btnc2:
        if st.button('Login', type='primary', icon=':material/person_add:', shortcut='control+enter', width='stretch'):
            st.session_state.teacher_login_type = 'login'
