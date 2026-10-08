import time
import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Quick Class Enrollment")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.student_data["student_id"]

    with st.spinner("Fetching class details..."):
        res = (
            supabase.table("subjects")
            .select("subject_id, name, section")
            .eq("subject_code", subject_code)
            .execute()
        )

    if not res.data:
        st.error("Subject code from URL parameter was not found.")
        if st.button("Close Modal", type="primary", width="stretch"):
            st.query_params.clear()
            st.rerun()
        return

    subject = res.data[0]
    
    check = (
        supabase.table("subject_students")
        .select("*")
        .eq("subject_id", subject["subject_id"])
        .eq("student_id", student_id)
        .execute()
    )

    if check.data:
        st.info(f"You are already enrolled in **{subject['name']}** (Section {subject['section']}).")
        if st.button("Continue to Dashboard", type="primary", width="stretch"):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(
        f"""
        <div style="background:#f0fdfa; border:1px solid #99f6e4; border-radius:12px; padding:1.25rem; margin-bottom:1.25rem; text-align:center;">
            <div class="eyebrow" style="color:#0f766e;">Class Invitation</div>
            <h3 style="margin:0.25rem 0 0.4rem; color:#0f172a;">{subject['name']}</h3>
            <p style="margin:0; color:#475569;">Section {subject['section']} &bull; Code: <b>{subject_code}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("Would you like to enroll in this subject workspace now?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("No Thanks", width="stretch", type="tertiary"):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("Yes, Enroll Now", type="primary", width="stretch"):
            with st.spinner("Enrolling..."):
                enroll_student_to_subject(student_id, subject["subject_id"])
            st.success(f"Enrolled in **{subject['name']}** successfully!")
            st.toast(f"Enrolled in {subject['name']}")
            st.query_params.clear()
            time.sleep(1)
            st.rerun()
