import io
import html
import segno
import streamlit as st


@st.dialog("Share Subject Join Code & QR")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "http://localhost:8501"
    join_url = f"{app_domain}/?join-code={subject_code}"
    safe_subject_name = html.escape(str(subject_name))
    safe_subject_code = html.escape(str(subject_code))
    safe_join_url = html.escape(join_url)

    st.markdown(
        f"""
        <div style="margin-bottom: 1.25rem;">
            <div class="panel-title" style="font-size:1.35rem !important;">{safe_subject_name}</div>
            <p class="muted-copy">Share this QR code or join link with your students for instant enrollment.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=2)

    col1, col2 = st.columns([1.1, 1], gap="medium")

    with col1:
        st.markdown("<div class='eyebrow'>Direct Join Code</div>", unsafe_allow_html=True)
        st.code(safe_subject_code, language="text")
        
        st.markdown("<div class='eyebrow' style='margin-top:0.8rem;'>Join URL</div>", unsafe_allow_html=True)
        st.code(safe_join_url, language="text")
        
        st.info("Students can scan the QR code with their mobile device or enter the subject code on their portal.")

    with col2:
        st.markdown("<div class='eyebrow' style='text-align:center;'>Class QR Code</div>", unsafe_allow_html=True)
        st.image(out.getvalue(), use_container_width=True, caption=f"Scan to join {subject_code}")
