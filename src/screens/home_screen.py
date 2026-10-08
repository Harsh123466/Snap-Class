import streamlit as st

from src.components.header import header_home
from src.ui.base_layout import style_background_home, style_base_layout


def home_screen():
    style_base_layout()
    style_background_home()

    header_home()

    st.markdown(
        """
        <div class="section-header sc-fade-in">
            <div class="portal-label">How it works</div>
            <div class="section-title">Scan. Recognize. Record.</div>
            <p class="section-copy">
                SmartClass turns classroom photos, voice checks, and join codes into verified attendance records.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    wf_col1, wf_col2, wf_col3 = st.columns(3)
    steps = [
        ("01", "Scan", "Capture a classroom photo, record voice, or let students enter with camera sign-in."),
        ("02", "Recognize", "AI compares faces and voice embeddings against enrolled student profiles."),
        ("03", "Record", "Review the roster, confirm present or absent status, and save the session archive."),
    ]

    for col, (number, title, copy) in zip((wf_col1, wf_col2, wf_col3), steps):
        with col:
            st.markdown(
                f"""
                <div class="wf-card sc-fade-in">
                    <div class="step-index">{number}</div>
                    <h4>{title}</h4>
                    <p>{copy}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="section-header sc-fade-in">
            <div class="portal-label">Choose your workspace</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="portal-card sc-fade-in">
                <div class="portal-icon">ST</div>
                <h3>Student Portal</h3>
                <p>
                    Sign in with camera face recognition, join subjects using a code or QR link,
                    and track your per-subject attendance standing from mobile or desktop.
                </p>
                <ul>
                    <li>Touchless camera sign-in</li>
                    <li>One-step class enrollment</li>
                    <li>Color-coded attendance status</li>
                    <li>Subject-wise session history</li>
                </ul>
            </div>
            <div style="margin-top: 1rem;"></div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Enter Student Portal",
            type="primary",
            use_container_width=True,
            key="home_btn_student",
        ):
            st.session_state["login_type"] = "student"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="portal-card sc-fade-in">
                <div class="portal-icon">TC</div>
                <h3>Teacher Portal</h3>
                <p>
                    Create subject workspaces, share join QR codes, run face or voice attendance,
                    and review analytics across saved class sessions.
                </p>
                <ul>
                    <li>Classroom photo attendance</li>
                    <li>Voice verification sessions</li>
                    <li>QR and join-code sharing</li>
                    <li>Attendance archives and charts</li>
                </ul>
            </div>
            <div style="margin-top: 1rem;"></div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Enter Teacher Portal",
            type="primary",
            use_container_width=True,
            key="home_btn_teacher",
        ):
            st.session_state["login_type"] = "teacher"
            st.rerun()
