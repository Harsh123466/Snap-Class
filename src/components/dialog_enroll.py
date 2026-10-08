import time
import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.markdown(
        """
        <p class="muted-copy" style="margin-bottom: 1.25rem;">
            Enter the subject code shared by your instructor to join the class workspace.
        </p>
        """,
        unsafe_allow_html=True,
    )

    join_code = st.text_input("Subject Code", placeholder="e.g. BCS401").strip()

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    if st.button("Enroll Now", type="primary", width="stretch"):
        if not join_code:
            st.warning("Please enter a valid subject code.")
            return

        with st.spinner("Verifying subject code..."):
            res = (
                supabase.table("subjects")
                .select("subject_id, name, subject_code")
                .eq("subject_code", join_code)
                .execute()
            )

        if not res.data:
            st.error("Subject code not found. Please check with your teacher.")
            return

        subject = res.data[0]
        student_id = st.session_state.student_data["student_id"]
        
        check = (
            supabase.table("subject_students")
            .select("*")
            .eq("subject_id", subject["subject_id"])
            .eq("student_id", student_id)
            .execute()
        )

        if check.data:
            st.info(f"You are already enrolled in **{subject['name']}**.")
            return

        with st.spinner(f"Joining {subject['name']}..."):
            enroll_student_to_subject(student_id, subject["subject_id"])
            
        st.success(f"Successfully enrolled in **{subject['name']}**!")
        st.toast(f"Joined {subject['name']}")
        time.sleep(1)
        st.rerun()
