import streamlit as st
from src.database.db import create_attendance


def show_attendance_result(df, logs):
    """Renders the interactive attendance verification matrix with summary metrics and confirmation controls."""
    total_count = len(df)
    present_count = len(df[df["Status"] == "Present"]) if not df.empty and "Status" in df.columns else 0
    absent_count = total_count - present_count
    present_pct = int((present_count / total_count) * 100) if total_count else 0

    m1, m2, m3 = st.columns(3)
    m1.markdown(f'<div class="mini-stat"><b>{total_count}</b><span>Total Students</span></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="mini-stat"><b style="color:#22c55e;">{present_count}</b><span>Detected Present</span></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="mini-stat"><b style="color:#f43f5e;">{absent_count}</b><span>Marked Absent</span></div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="margin-top:1rem;">
            <div style="display:flex; justify-content:space-between; gap:1rem; margin-bottom:0.5rem;">
                <span class="eyebrow">Session confidence</span>
                <span class="status-chip success">{present_count} of {total_count} present</span>
            </div>
            <div class="progress-track"><div class="progress-fill" style="width:{present_pct}%;"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown('<p class="muted-copy">Review the verified attendance details below before saving to the database.</p>', unsafe_allow_html=True)
    
    st.dataframe(df, hide_index=True, width="stretch")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Discard Session", width="stretch", type="tertiary"):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button("Confirm & Save Records", width="stretch", type="primary"):
            try:
                with st.spinner("Saving attendance records to database..."):
                    create_attendance(logs)
                st.toast("Attendance session saved successfully! 🎉")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error(f"Sync failed: {str(e)}. Please try again.")


@st.dialog("Verified Attendance Report")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)
