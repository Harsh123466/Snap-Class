import streamlit as st


def header_home():
    """Renders the SmartClass landing hero."""
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(
        f"""
        <div class="home-hero sc-fade-in">
            <div class="brand-mark">
                <img src="{logo_url}" alt="SmartClass Logo" />
            </div>
            <div style="margin-top: 1.25rem;">
                <div class="home-kicker">AI-powered attendance workspace</div>
                <div class="home-title">SmartClass <span class="accent-text">Attendance</span></div>
                <p class="home-subtitle">
                    A premium biometric and voice attendance system for modern classrooms.
                    Create class spaces, verify presence with AI, and keep every session record clear.
                </p>
                <div class="chip-row">
                    <span class="chip">Face recognition</span>
                    <span class="chip">Voice verification</span>
                    <span class="chip">QR class joining</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def header_dashboard():
    """Renders the compact dashboard brand header."""
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(
        f"""
        <div class="dashboard-brand sc-fade-in">
            <div class="dashboard-brand-mark">
                <img src="{logo_url}" alt="SmartClass Logo" />
            </div>
            <div>
                <div class="eyebrow">Smart EdTech SaaS Platform</div>
                <div class="panel-title" style="margin-top:0;">SmartClass</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
