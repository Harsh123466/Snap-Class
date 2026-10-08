import html
import time

import numpy as np
import streamlit as st
from PIL import Image

from src.components.dialog_enroll import enroll_dialog
from src.components.header import header_dashboard
from src.components.subject_card import subject_card
from src.database.db import (
    create_student,
    get_all_students,
    get_student_attendance,
    get_student_subjects,
    unenroll_student_to_subject,
)
from src.pipelines.face_pipeline import get_face_embeddings, predict_attendance, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.ui.base_layout import style_background_dashboard, style_base_layout


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    render_auth_header()

    hero_col, scan_col = st.columns([1.35, 1], gap="large", vertical_alignment="top")

    with hero_col:
        st.markdown(
            """
            <div class="hub-hero">
                <div class="eyebrow">Student Face ID Entrance</div>
                <div class="hub-title">Touchless Face Verification</div>
                <p style="color:#e2e8f0 !important;">
                    Position your face in front of the camera for instant AI recognition and dashboard sign in.
                    New students can register a profile directly below.
                </p>
                <div class="feature-grid">
                    <div class="glass-tile"><b>01. Scan</b><span>Center face in light</span></div>
                    <div class="glass-tile"><b>02. Join</b><span>Enrolled subject spaces</span></div>
                    <div class="glass-tile"><b>03. Track</b><span>Live attendance stats</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with scan_col:
        st.markdown(
            """
            <div class="camera-card sc-fade-in">
                <div class="eyebrow">Camera Check</div>
                <div class="panel-title" style="font-size:1.35rem !important;">Sign In with Face ID</div>
                <p class="muted-copy">Ensure your face is centered and in good lighting.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        show_registration = False
        photo_source = st.camera_input("Position your face in the box below")

        if photo_source:
            img = np.array(Image.open(photo_source))

            with st.spinner("AI is scanning your face embeddings..."):
                detected, all_idx, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("No face detected. Please position your face clearly in good lighting.")
            elif num_faces > 1:
                st.warning("Multiple faces detected. Please ensure only your face is visible.")
            elif detected:
                student_id = list(detected.keys())[0]
                all_students = get_all_students()
                student = next((s for s in all_students if s["student_id"] == student_id), None)

                if student:
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = "student"
                    st.session_state.student_data = student
                    st.toast(f"Welcome back, {student['name']}! 🎉")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.info("Face detected but no matching student profile was found.")
                    show_registration = True
            else:
                if len(all_idx) == 0:
                    st.info("No registered students found in database. Create your profile below.")
                else:
                    st.info("Face not recognized in system database. You can register as a new student.")
                show_registration = True

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        if st.button("← Back to Home Portal", type="tertiary", use_container_width=True, key="student_login_back_home"):
            st.session_state["login_type"] = None
            st.rerun()

        if show_registration:
            render_student_registration(photo_source)


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]
    student_name = html.escape(str(student_data["name"]))

    # Left Sidebar Navigation
    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-profile-card">
                <div style="display:flex; align-items:center; gap:0.75rem;">
                    <div class="sidebar-profile-avatar">🎓</div>
                    <div style="overflow:hidden;">
                        <h4 style="margin:0; font-size:1.05rem; font-weight:800; color:#ffffff !important;">{student_name}</h4>
                        <div style="font-size:0.78rem; color:#94a3b8 !important;">ID #{student_data['student_id']}</div>
                        <span style="background:rgba(15,118,110,0.4); color:#5eead4 !important; border:1px solid rgba(45,212,191,0.4); border-radius:9999px; padding:0.12rem 0.5rem; font-size:0.7rem; font-weight:700; display:inline-block; margin-top:0.35rem;">Student Portal</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='eyebrow' style='color:#94a3b8 !important;'>STUDENT CONTROLS</div>", unsafe_allow_html=True)
        
        if st.button("➕ Enroll in Class Space", type="primary", use_container_width=True, key="side_enroll"):
            enroll_dialog()

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

        if st.button("← Switch Workspace", type="tertiary", use_container_width=True, key="student_nav_home"):
            st.session_state["login_type"] = None
            st.rerun()

        if st.button("🚪 Sign Out", type="secondary", use_container_width=True, key="student_nav_logout"):
            st.session_state["is_logged_in"] = False
            if "student_data" in st.session_state:
                del st.session_state.student_data
            st.rerun()

    header_dashboard()
    st.markdown(
        f"""
        <div class="hub-hero">
            <div class="eyebrow">Student Dashboard</div>
            <div class="hub-title">Hi, {student_name}</div>
            <p style="color:#e2e8f0 !important;">Track your subject enrollments, session attendance percentage, and class status in real time.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("Loading your enrolled subjects and attendance logs..."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    for log in logs:
        sid = log["subject_id"]
        stats_map.setdefault(sid, {"total": 0, "attend": 0})
        stats_map[sid]["total"] += 1
        if log.get("is_present"):
            stats_map[sid]["attend"] += 1

    total_subjects = len(subjects)
    total_classes = sum(item["total"] for item in stats_map.values())
    attended_classes = sum(item["attend"] for item in stats_map.values())
    overall = int((attended_classes / total_classes) * 100) if total_classes else 0

    col_gauge, col_stats = st.columns([1, 2], gap="large")

    with col_gauge:
        gauge_color = "#0f766e" if overall >= 75 else "#f59e0b" if overall >= 50 else "#e11d48"
        stroke_offset = 100 - overall
        st.markdown(
            f"""
            <div class="gauge-container">
                <div class="eyebrow" style="margin-bottom:0.4rem;">Overall Attendance Gauge</div>
                <div style="position:relative; width:130px; height:130px; margin:0.5rem auto;">
                    <svg viewBox="0 0 36 36" style="width:130px; height:130px; transform:rotate(-90deg);">
                        <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" stroke="#e2e8f0" stroke-width="3.5" fill="none" />
                        <path stroke-dasharray="100, 100" stroke-dashoffset="{stroke_offset}" stroke="{gauge_color}" stroke-width="3.5" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                    </svg>
                    <div style="position:absolute; top:40px; left:0; right:0; font-size:1.6rem; font-weight:800; color:{gauge_color};">{overall}%</div>
                </div>
                <div style="font-size:0.84rem; color:#64748b; font-weight:600;">Overall Campus Standing</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_stats:
        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        with s1:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-icon-wrapper stat-icon-teal">📚</div>
                    <div>
                        <div class="stat-val">{total_subjects}</div>
                        <div class="stat-lbl">Enrolled Subjects</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with s2:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-icon-wrapper stat-icon-indigo">✅</div>
                    <div>
                        <div class="stat-val">{attended_classes} / {total_classes}</div>
                        <div class="stat-lbl">Attended Classes</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div style="margin-top:1.5rem; margin-bottom:0.8rem;">
            <div class="eyebrow">Class Workspace</div>
            <div class="panel-title">Enrolled Subjects Overview</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not subjects:
        st.markdown(
            """
            <div class="empty-state sc-fade-in">
                <div class="empty-state-icon">+</div>
                <div class="panel-title" style="text-align:center; font-size:1.25rem !important;">Not Enrolled in Any Subjects Yet</div>
                <p class="muted-copy">Use Enroll in Class Space in the left sidebar to join with a subject code or QR link.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    cols = st.columns(2)
    for idx, sub_node in enumerate(subjects):
        sub = sub_node["subjects"]
        sid = sub["subject_id"]
        stats = stats_map.get(sid, {"total": 0, "attend": 0})
        percent = int((stats["attend"] / stats["total"]) * 100) if stats["total"] else 0

        def unenroll_button(subject=sub):
            if st.button(
                "Unenroll from Class",
                type="tertiary",
                use_container_width=True,
                key=f"unenroll_{subject['subject_id']}",
            ):
                unenroll_student_to_subject(student_id, subject["subject_id"])
                st.toast(f"Unenrolled from {subject['name']} successfully.")
                st.rerun()

        with cols[idx % 2]:
            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=[
                    ("🗓️", "total sessions", stats["total"]),
                    ("✅", "attended", stats["attend"]),
                ],
                progress=percent,
                footer_callback=unenroll_button,
            )


def render_student_registration(photo_source):
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            """
            <div class="eyebrow">New Student Onboarding</div>
            <div class="panel-title" style="font-size:1.35rem !important;">Register Student Profile</div>
            """,
            unsafe_allow_html=True,
        )
        new_name = st.text_input("Full Name", placeholder="e.g. Harsh Adhana")

        st.subheader("Optional Voice Enrollment")
        st.info("Record a short phrase if your instructor uses voice attendance.")

        audio_data = None
        try:
            audio_data = st.audio_input("Record classroom voice phrase")
        except Exception:
            st.error("Audio recording is not supported in this browser.")

        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("Create Student Account", type="primary", use_container_width=True):
                if not new_name:
                    st.warning("Please enter your name.")
                    return

                with st.spinner("Extracting face embeddings and creating student profile..."):
                    img = np.array(Image.open(photo_source))
                    encodings = get_face_embeddings(img)

                    if len(encodings) != 1:
                        st.error("Could not capture exactly one clear face for registration. Try again.")
                        return

                    voice_emb = get_voice_embedding(audio_data.read()) if audio_data else None
                    response_data = create_student(
                        new_name,
                        face_embedding=encodings[0].tolist(),
                        voice_embedding=voice_emb,
                    )

                    if response_data:
                        train_classifier()
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = response_data[0]
                        st.toast(f"Profile created! Welcome, {new_name}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Could not create student profile. Please try again.")

        with btn_c2:
            if st.button("← Cancel & Back to Login", type="tertiary", use_container_width=True, key="reg_cancel_btn"):
                st.rerun()


def render_auth_header():
    header_dashboard()
