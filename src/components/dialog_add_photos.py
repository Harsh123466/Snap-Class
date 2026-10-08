import streamlit as st
from PIL import Image


@st.dialog("Capture or Upload Classroom Photos")
def add_photos_dialog():
    st.markdown(
        """
        <p class="muted-copy" style="margin-bottom: 1.25rem;">
            Add high-quality classroom snapshots to queue them for AI face detection and attendance marking.
        </p>
        """,
        unsafe_allow_html=True,
    )

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = 'primary' if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('📷 Live Camera', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'

    with t2:
        type_upload = 'primary' if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('📁 Upload Files', type=type_upload, width='stretch'):
            st.session_state.photo_tab = 'upload'

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast('Snapshot added to queue.')
            st.rerun()

    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader(
            'Choose image files (JPG, PNG, JPEG)',
            type=['jpg', 'png', 'jpeg'],
            accept_multiple_files=True,
            key='dialog_upload',
        )

        if uploaded_files:
            for f in uploaded_files:
                st.session_state.attendance_images.append(Image.open(f))

            st.toast(f'{len(uploaded_files)} photos uploaded successfully.')
            st.rerun()

    st.divider()

    if st.button('Done & Return to Queue', type='primary', width='stretch'):
        st.rerun()
