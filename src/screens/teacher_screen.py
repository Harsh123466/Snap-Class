from datetime import datetime
import html

import numpy as np
import pandas as pd
import streamlit as st

from src.components.dialog_add_photos import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.components.header import header_dashboard
from src.components.subject_card import subject_card
from src.database.config import supabase
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    get_attendance_for_teacher,
    get_teacher_subjects,
    teacher_login,
)
from src.pipelines.face_pipeline import predict_attendance
from src.ui.base_layout import style_background_dashboard, style_base_layout


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif st.session_state.get("teacher_login_type", "login") == "login":
        teacher_screen_login()
    else:
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    teacher_name = html.escape(str(teacher_data["name"]))
    teacher_username = html.escape(str(teacher_data.get("username", "teacher")))

    # Left Sidebar Navigation
    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-profile-card">
                <div style="display:flex; align-items:center; gap:0.75rem;">
                    <div class="sidebar-profile-avatar">👨‍🏫</div>
                    <div style="overflow:hidden;">
                        <h4 style="margin:0; font-size:1.05rem; font-weight:800; color:#ffffff !important;">{teacher_name}</h4>
                        <div style="font-size:0.78rem; color:#94a3b8 !important;">@{teacher_username}</div>
                        <span style="background:rgba(79,70,229,0.4); color:#c084fc !important; border:1px solid rgba(139,92,246,0.4); border-radius:9999px; padding:0.12rem 0.5rem; font-size:0.7rem; font-weight:700; display:inline-block; margin-top:0.35rem;">Teacher Workspace</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='eyebrow' style='color:#94a3b8 !important;'>NAVIGATION MENU</div>", unsafe_allow_html=True)
        
        nav_selection = st.radio(
            "Teacher Menu",
            options=["📸 Take AI Attendance", "📚 Manage Subjects", "📊 Analytics & Archives"],
            label_visibility="collapsed",
            key="teacher_sidebar_nav",
        )

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

        if st.button("← Switch Workspace", type="tertiary", use_container_width=True, key="teacher_nav_home"):
            st.session_state["login_type"] = None
            st.rerun()

        if st.button("🚪 Sign Out", type="secondary", use_container_width=True, key="teacher_nav_logout"):
            st.session_state["is_logged_in"] = False
            if "teacher_data" in st.session_state:
                del st.session_state.teacher_data
            st.rerun()

    # Dashboard Header Banner
    header_dashboard()
    st.markdown(
        f"""
        <div class="hub-hero">
            <div class="eyebrow">Teacher Command Workspace</div>
            <div class="hub-title">Welcome back, {teacher_name}</div>
            <p style="color:#e2e8f0 !important;">Manage subject spaces, share QR join links, execute face or voice AI attendance, and review session archives.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if nav_selection == "📸 Take AI Attendance":
        teacher_tab_take_attendance()
    elif nav_selection == "📚 Manage Subjects":
        teacher_tab_manage_subjects()
    else:
        teacher_tab_attendance_records()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    
    st.markdown(
        """
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
            <div>
                <div class="eyebrow">Live Classroom Session</div>
                <div class="panel-title">Take AI Attendance</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    with st.spinner("Loading subjects..."):
        subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.markdown(
            """
            <div class="empty-state sc-fade-in">
                <div class="empty-state-icon">+</div>
                <div class="panel-title" style="text-align:center; font-size:1.25rem !important;">No Subject Spaces Created Yet</div>
                <p class="muted-copy">Create your first subject space before running an AI attendance session.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Create First Subject Space", type="primary", use_container_width=True):
            create_subject_dialog(teacher_id)
        return

    subject_options = {f"{s['name']} ({s['subject_code']}) - Sec {s['section']}": s["subject_id"] for s in subjects}
    
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1:
        selected_subject_label = st.selectbox("Select Target Subject Workspace", options=list(subject_options.keys()))
    with col2:
        if st.button("📷 Add Classroom Photos", type="primary", use_container_width=True):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]
    photo_count = len(st.session_state.attendance_images)

    # Metric Cards Row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon-wrapper stat-icon-indigo">📚</div>
                <div>
                    <div class="stat-val">{len(subjects)}</div>
                    <div class="stat-lbl">Active Subjects</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon-wrapper stat-icon-purple">📷</div>
                <div>
                    <div class="stat-val">{photo_count}</div>
                    <div class="stat-lbl">Queued Photos</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-icon-wrapper stat-icon-emerald">🤖</div>
                <div>
                    <div class="stat-val">2</div>
                    <div class="stat-lbl">AI Scan Engines</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)

    if st.session_state.attendance_images:
        st.markdown(f"<div class='eyebrow'>Queued Classroom Photos ({photo_count})</div>", unsafe_allow_html=True)
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f"Photo {idx + 1}")
    else:
        st.markdown(
            """
            <div class="empty-state" style="padding:1.4rem; margin-bottom:1rem;">
                <p class="muted-copy">Photo queue is empty. Add classroom photos above or use voice attendance below.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("Clear Photo Queue", use_container_width=True, type="tertiary", disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button("⚡ Run AI Face Analysis", use_container_width=True, type="primary", disabled=not has_photos):
            run_face_attendance(selected_subject_id)

    with c3:
        if st.button("🎙️ Use Voice Attendance", type="primary", use_container_width=True):
            voice_attendance_dialog(selected_subject_id)


def run_face_attendance(selected_subject_id):
    with st.spinner("Scanning classroom photos with AI Face Recognition model..."):
        all_detected_ids = {}

        for idx, img in enumerate(st.session_state.attendance_images):
            img_np = np.array(img.convert("RGB"))
            detected, _, _ = predict_attendance(img_np)

            for sid in detected.keys():
                student_id = int(sid)
                all_detected_ids.setdefault(student_id, []).append(f"Photo {idx + 1}")

        enrolled_res = (
            supabase.table("subject_students")
            .select("*, students(*)")
            .eq("subject_id", selected_subject_id)
            .execute()
        )
        enrolled_students = enrolled_res.data

        if not enrolled_students:
            st.warning("No students are enrolled in this subject yet.")
            return

        results, attendance_to_log = [], []
        current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        for node in enrolled_students:
            student = node["students"]
            sources = all_detected_ids.get(int(student["student_id"]), [])
            is_present = len(sources) > 0

            results.append(
                {
                    "Name": student["name"],
                    "ID": student["student_id"],
                    "Source": ", ".join(sources) if is_present else "-",
                    "Status": "Present" if is_present else "Absent",
                }
            )
            attendance_to_log.append(
                {
                    "student_id": student["student_id"],
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present),
                }
            )

    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    col1, col2 = st.columns([2, 1], vertical_alignment="bottom")
    with col1:
        st.markdown(
            """
            <div style="margin:0;">
                <div class="eyebrow">Class Workspaces</div>
                <div class="panel-title">Manage Subjects</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("➕ Create New Subject", type="primary", use_container_width=True):
            create_subject_dialog(teacher_id)

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    with st.spinner("Fetching subjects..."):
        subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.markdown(
            """
            <div class="empty-state sc-fade-in">
                <div class="empty-state-icon">+</div>
                <div class="panel-title" style="text-align:center; font-size:1.25rem !important;">No Subjects Created Yet</div>
                <p class="muted-copy">Create a subject workspace to generate QR codes and enroll students.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    cols = st.columns(2)
    for idx, sub in enumerate(subjects):
        stats = [
            ("👥", "Students", sub["total_students"]),
            ("🗓️", "Sessions", sub["total_classes"]),
        ]

        def share_btn(subject=sub):
            if st.button(
                f"🔗 Share {subject['subject_code']}",
                key=f"share_{subject['subject_code']}",
                use_container_width=True,
                type="tertiary",
            ):
                share_subject_dialog(subject["name"], subject["subject_code"])

        with cols[idx % 2]:
            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=stats,
                footer_callback=share_btn,
            )


def teacher_tab_attendance_records():
    st.markdown(
        """
        <div style="margin-top:0; margin-bottom:1rem;">
            <div class="eyebrow">Historical Analytics & Logs</div>
            <div class="panel-title">Attendance Archives</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    teacher_id = st.session_state.teacher_data["teacher_id"]
    
    with st.spinner("Retrieving historical attendance logs..."):
        records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.markdown(
            """
            <div class="empty-state sc-fade-in">
                <div class="empty-state-icon">%</div>
                <div class="panel-title" style="text-align:center; font-size:1.25rem !important;">No Attendance Logs Saved Yet</div>
                <p class="muted-copy">Take attendance for a class session and confirm the results to save archives here.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    data = []
    for record in records:
        ts = record.get("timestamp")
        data.append(
            {
                "student_id": record.get("student_id"),
                "ts_group": ts.split(".")[0] if ts else None,
                "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
                "Subject": record["subjects"]["name"],
                "Subject Code": record["subjects"]["subject_code"],
                "is_present": bool(record.get("is_present", False)),
            }
        )

    df = pd.DataFrame(data)
    summary = (
        df.groupby(["ts_group", "Time", "Subject", "Subject Code"])
        .agg(Present_Count=("is_present", "sum"), Total_Count=("is_present", "count"))
        .reset_index()
    )
    summary["Attendance Rate"] = (
        summary["Present_Count"].astype(str) + " / " + summary["Total_Count"].astype(str) + " students"
    )

    # Calculate clear metrics
    saved_sessions_count = len(summary)
    unique_students_count = df["student_id"].nunique() if "student_id" in df.columns else 0
    total_log_checks = len(df)

    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon-wrapper stat-icon-indigo">🗓️</div>
                <div>
                    <div class="stat-val">{saved_sessions_count}</div>
                    <div class="stat-lbl">Saved Class Sessions</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon-wrapper stat-icon-purple">👥</div>
                <div>
                    <div class="stat-val">{unique_students_count}</div>
                    <div class="stat-lbl">Unique Students Verified</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon-wrapper stat-icon-emerald">📋</div>
                <div>
                    <div class="stat-val">{total_log_checks}</div>
                    <div class="stat-lbl">Total Log Checks</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>Attendance Session Breakdown</div>", unsafe_allow_html=True)
    
    chart_df = summary[["Subject", "Present_Count", "Total_Count"]].groupby("Subject").sum().reset_index()
    if not chart_df.empty:
        st.bar_chart(chart_df.set_index("Subject"), color=["#4f46e5", "#cbd5e1"])

    display_df = summary.sort_values(by="ts_group", ascending=False)[
        ["Time", "Subject", "Subject Code", "Attendance Rate"]
    ]

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

    return False


def teacher_screen_login():
    render_auth_header()

    hero_col, form_col = st.columns([1.35, 1], gap="large", vertical_alignment="top")
    with hero_col:
        st.markdown(
            """
            <div class="hub-hero">
                <div class="eyebrow">Teacher Portal</div>
                <div class="hub-title">Automate Classroom Attendance</div>
                <p style="color:#e2e8f0 !important;">Streamline daily class check-in with AI multi-face recognition, voice verification, and instant QR sharing.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with form_col:
        st.markdown(
            """
            <div class="auth-card sc-fade-in">
                <div class="eyebrow">Secure Sign In</div>
                <div class="panel-title" style="font-size:1.35rem !important;">Teacher Login</div>
                <p class="muted-copy">Enter your teacher credentials to access your dashboard.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        teacher_username = st.text_input("Username", placeholder="e.g. ananyaroy")
        teacher_pass = st.text_input("Password", type="password", placeholder="Enter password")

        btnc1, btnc2 = st.columns(2)
        with btnc1:
            if st.button("Sign In", use_container_width=True, type="primary"):
                if login_teacher(teacher_username, teacher_pass):
                    st.toast("Welcome back!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with btnc2:
            if st.button("Register Account", type="tertiary", use_container_width=True):
                st.session_state.teacher_login_type = "register"
                st.rerun()

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        if st.button("← Back to Home Portal", type="tertiary", use_container_width=True, key="login_back_home"):
            st.session_state["login_type"] = None
            st.rerun()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required."
    if check_teacher_exists(teacher_username):
        return False, "Username already taken."
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Profile created successfully! You can log in now."
    except Exception:
        return False, "Unexpected error while creating the teacher profile."


def teacher_screen_register():
    render_auth_header()

    hero_col, form_col = st.columns([1.25, 1], gap="large", vertical_alignment="top")
    with hero_col:
        st.markdown(
            """
            <div class="hub-hero">
                <div class="eyebrow">Teacher Onboarding</div>
                <div class="hub-title">Create Instructor Profile</div>
                <p style="color:#e2e8f0 !important;">Register once to setup subject spaces, invite students, and run real-time AI attendance verification.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with form_col:
        st.markdown(
            """
            <div class="auth-card sc-fade-in">
                <div class="eyebrow">New Registration</div>
                <div class="panel-title" style="font-size:1.35rem !important;">Register Teacher</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        teacher_username = st.text_input("Username", placeholder="e.g. ananyaroy")
        teacher_name = st.text_input("Full Name", placeholder="e.g. Prof. Ananya Roy")
        teacher_pass = st.text_input("Password", type="password", placeholder="Enter password")
        teacher_pass_confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")

        btnc1, btnc2 = st.columns(2)
        with btnc1:
            if st.button("Register Now", type="primary", use_container_width=True):
                success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
                if success:
                    st.success(message)
                    st.session_state.teacher_login_type = "login"
                    st.rerun()
                else:
                    st.error(message)

        with btnc2:
            if st.button("← Back to Login", type="tertiary", use_container_width=True):
                st.session_state.teacher_login_type = "login"
                st.rerun()

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        if st.button("← Back to Home Portal", type="tertiary", use_container_width=True, key="reg_back_home"):
            st.session_state["login_type"] = None
            st.rerun()


def render_auth_header():
    header_dashboard()
