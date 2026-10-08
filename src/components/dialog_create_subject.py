import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject Workspace")
def create_subject_dialog(teacher_id):
    st.markdown(
        """
        <p class="muted-copy" style="margin-bottom: 1.25rem;">
            Set up a new subject space to enroll students, generate QR join links, and track session attendance.
        </p>
        """,
        unsafe_allow_html=True,
    )

    sub_id = st.text_input("Subject Code", placeholder="e.g. BCS401", help="Unique identifier code for the course").strip()
    sub_name = st.text_input("Subject Name", placeholder="e.g. Computer Networks").strip()
    sub_section = st.text_input("Section / Batch", placeholder="e.g. Section A").strip()

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    if st.button("Create Subject Now", type="primary", width="stretch"):
        if sub_id and sub_name and sub_section:
            try:
                with st.spinner("Creating subject workspace..."):
                    create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.toast(f"Subject '{sub_name}' created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating subject: {str(e)}")
        else:
            st.warning("Please fill in all required fields (Code, Name, Section).")
