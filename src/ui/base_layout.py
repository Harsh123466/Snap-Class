import streamlit as st


def style_background_home():
    """Applies the immersive SmartClass portal background."""
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at 12% 8%, rgba(99, 102, 241, 0.28), transparent 34rem),
                    radial-gradient(circle at 88% 16%, rgba(34, 211, 238, 0.18), transparent 32rem),
                    radial-gradient(circle at 48% 92%, rgba(16, 185, 129, 0.12), transparent 28rem),
                    var(--sc-bg) !important;
                background-attachment: fixed !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_background_dashboard():
    """Applies the premium dark SaaS dashboard background."""
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at 8% 0%, rgba(99, 102, 241, 0.20), transparent 34rem),
                    radial-gradient(circle at 92% 12%, rgba(34, 211, 238, 0.14), transparent 30rem),
                    linear-gradient(180deg, #090d18 0%, #0b1020 42%, #070a12 100%) !important;
                background-attachment: fixed !important;
            }

            .stMain > div {
                background: transparent !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_base_layout():
    """Injects the SmartClass design system and global Streamlit component styling."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

            :root {
                --sc-bg: #070a12;
                --sc-bg-soft: #0b1020;
                --sc-panel: rgba(15, 23, 42, 0.78);
                --sc-panel-strong: rgba(17, 25, 46, 0.94);
                --sc-panel-muted: rgba(30, 41, 59, 0.72);
                --sc-border: rgba(148, 163, 184, 0.20);
                --sc-border-strong: rgba(125, 211, 252, 0.34);
                --sc-text: #f8fafc;
                --sc-muted: #94a3b8;
                --sc-subtle: #64748b;
                --sc-indigo: #6366f1;
                --sc-cyan: #22d3ee;
                --sc-teal: #14b8a6;
                --sc-green: #22c55e;
                --sc-amber: #f59e0b;
                --sc-red: #f43f5e;
                --sc-gradient: linear-gradient(135deg, #6366f1 0%, #22d3ee 100%);
                --sc-gradient-soft: linear-gradient(135deg, rgba(99, 102, 241, 0.18), rgba(34, 211, 238, 0.10));
                --sc-radius-sm: 12px;
                --sc-radius-md: 16px;
                --sc-radius-lg: 22px;
                --sc-shadow: 0 24px 80px rgba(0, 0, 0, 0.34);
                --sc-shadow-soft: 0 14px 40px rgba(0, 0, 0, 0.22);
                --sc-focus: 0 0 0 3px rgba(34, 211, 238, 0.28);
            }

            #MainMenu, footer { visibility: hidden; }
            header[data-testid="stHeader"] { visibility: hidden; }
            .stAppHeader { display: none !important; }

            html, body, [class*="css"], .stApp {
                color: var(--sc-text) !important;
                font-family: 'Manrope', 'Inter', system-ui, sans-serif !important;
            }

            .block-container {
                max-width: 1240px;
                padding-top: 1.15rem !important;
                padding-bottom: 4rem !important;
            }

            * { letter-spacing: 0; }
            a, a:visited { color: var(--sc-cyan) !important; }

            .sc-fade-in { animation: scFadeIn 420ms ease both; }
            @keyframes scFadeIn {
                from { opacity: 0; transform: translateY(8px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .sc-shell, .hub-hero, .portal-card, .wf-card, .cap-card, .stat-card,
            .gauge-container, .subject-card, .empty-state, .auth-card, .camera-card,
            .mini-stat {
                background: var(--sc-panel);
                border: 1px solid var(--sc-border);
                box-shadow: var(--sc-shadow-soft);
                backdrop-filter: blur(20px);
            }

            .home-hero {
                max-width: 960px;
                margin: 0 auto 1.7rem;
                padding: 3rem 1rem 1rem;
                text-align: center;
            }

            .brand-mark, .dashboard-brand-mark {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                border-radius: var(--sc-radius-md);
                border: 1px solid rgba(255, 255, 255, 0.16);
                background: rgba(255, 255, 255, 0.94);
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.36);
                padding: 0.7rem 1rem;
            }

            .brand-mark img { height: 64px; object-fit: contain; }
            .dashboard-brand { display: flex; align-items: center; gap: 0.9rem; padding: 0.3rem 0 1rem; }
            .dashboard-brand-mark { border-radius: var(--sc-radius-sm); padding: 0.42rem 0.62rem; box-shadow: 0 12px 34px rgba(0, 0, 0, 0.20); }
            .dashboard-brand-mark img { height: 46px; object-fit: contain; }

            .home-kicker, .portal-label, .eyebrow {
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                color: #a5f3fc !important;
                font-size: 0.76rem !important;
                font-weight: 800 !important;
                letter-spacing: 0.08em !important;
                text-transform: uppercase;
            }

            .home-kicker, .portal-label {
                justify-content: center;
                border: 1px solid rgba(125, 211, 252, 0.36) !important;
                border-radius: 999px;
                background: rgba(8, 47, 73, 0.42) !important;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 12px 34px rgba(34, 211, 238, 0.12);
                margin-bottom: 1rem;
                padding: 0.5rem 1rem;
            }

            .home-title, .sc-display {
                color: var(--sc-text) !important;
                font-family: 'Space Grotesk', 'Manrope', sans-serif !important;
                font-size: clamp(2.8rem, 6vw, 5.2rem) !important;
                font-weight: 700 !important;
                line-height: 0.96 !important;
                margin: 0.6rem 0 0.9rem !important;
            }

            .accent-text {
                background: var(--sc-gradient);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent !important;
            }

            .home-subtitle, .sc-subtitle {
                color: #cbd5e1 !important;
                font-size: 1.05rem !important;
                line-height: 1.75 !important;
                max-width: 760px;
                margin: 0 auto 1.45rem !important;
            }

            .chip-row { display: flex; justify-content: center; gap: 0.65rem; flex-wrap: wrap; margin-top: 1.25rem; }
            .chip, .status-chip {
                align-items: center;
                background: rgba(15, 23, 42, 0.70);
                border: 1px solid rgba(148, 163, 184, 0.24);
                border-radius: 999px;
                color: #e2e8f0 !important;
                display: inline-flex;
                font-size: 0.82rem;
                font-weight: 800;
                gap: 0.4rem;
                padding: 0.4rem 0.75rem;
            }

            .status-chip.success { color: #bbf7d0 !important; border-color: rgba(34, 197, 94, 0.38); background: rgba(20, 83, 45, 0.34); }
            .status-chip.warn { color: #fde68a !important; border-color: rgba(245, 158, 11, 0.40); background: rgba(120, 53, 15, 0.34); }
            .status-chip.danger { color: #fecdd3 !important; border-color: rgba(244, 63, 94, 0.40); background: rgba(136, 19, 55, 0.34); }

            .section-header { margin: 1.8rem 0 1rem; text-align: center; }
            .section-title, .panel-title {
                color: var(--sc-text) !important;
                font-family: 'Space Grotesk', 'Manrope', sans-serif !important;
                font-size: clamp(1.5rem, 2.5vw, 2.2rem) !important;
                font-weight: 700 !important;
                line-height: 1.15 !important;
                margin: 0.25rem 0 0.35rem !important;
            }

            .panel-title { font-size: 1.55rem !important; text-align: left; }
            .section-copy, .muted-copy { color: var(--sc-muted) !important; line-height: 1.65 !important; margin: 0; }

            .wf-card, .cap-card, .portal-card {
                border-radius: var(--sc-radius-lg) !important;
                min-height: 215px;
                padding: 1.25rem !important;
                transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease, background 180ms ease;
            }

            .wf-card:hover, .cap-card:hover, .portal-card:hover, .subject-card:hover {
                border-color: rgba(125, 211, 252, 0.46) !important;
                box-shadow: 0 24px 70px rgba(14, 165, 233, 0.16);
                transform: translateY(-3px);
            }

            .step-index, .portal-icon, .stat-icon-wrapper {
                align-items: center;
                background: var(--sc-gradient);
                border-radius: var(--sc-radius-sm);
                box-shadow: 0 12px 34px rgba(99, 102, 241, 0.28);
                color: #ffffff;
                display: inline-flex;
                font-weight: 900;
                justify-content: center;
            }

            .step-index { height: 42px; margin-bottom: 0.8rem; width: 42px; }
            .portal-icon { font-size: 1.55rem; height: 58px; margin-bottom: 1rem; width: 58px; }

            .wf-card h4, .cap-card h4, .portal-card h3 {
                color: var(--sc-text) !important;
                font-family: 'Space Grotesk', 'Manrope', sans-serif !important;
                font-size: 1.12rem !important;
                font-weight: 700 !important;
                margin: 0.35rem 0 0.45rem !important;
            }

            .wf-card p, .cap-card p, .portal-card p, .portal-card li {
                color: #cbd5e1 !important;
                font-size: 0.92rem !important;
                line-height: 1.62 !important;
            }

            .portal-card { min-height: 320px; padding: 1.55rem !important; }
            .portal-card ul { margin: 1rem 0 0; padding-left: 1.1rem; }

            .hub-hero {
                background:
                    linear-gradient(135deg, rgba(99, 102, 241, 0.88), rgba(8, 47, 73, 0.82)),
                    radial-gradient(circle at 82% 20%, rgba(34, 211, 238, 0.38), transparent 18rem);
                border-radius: var(--sc-radius-lg);
                margin-bottom: 1.35rem;
                overflow: hidden;
                padding: 1.8rem 2rem;
                position: relative;
            }

            .hub-hero:after {
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.10), transparent);
                content: "";
                height: 1px;
                left: 1.5rem;
                position: absolute;
                right: 1.5rem;
                top: 0;
            }

            .hub-title {
                color: #ffffff !important;
                font-family: 'Space Grotesk', 'Manrope', sans-serif !important;
                font-size: clamp(1.8rem, 3.8vw, 3rem) !important;
                font-weight: 700 !important;
                line-height: 1.04 !important;
                margin: 0.25rem 0 0.5rem !important;
            }

            .feature-grid { display: grid; gap: 0.65rem; grid-template-columns: repeat(3, minmax(0, 1fr)); margin-top: 1.1rem; }
            .glass-tile { background: rgba(255, 255, 255, 0.09); border: 1px solid rgba(255, 255, 255, 0.16); border-radius: var(--sc-radius-sm); padding: 0.8rem; }
            .glass-tile b, .glass-tile span { display: block; }
            .glass-tile span { color: #cbd5e1; font-size: 0.78rem; margin-top: 0.2rem; }

            [data-testid="stSidebar"] {
                background: rgba(7, 10, 18, 0.96) !important;
                border-right: 1px solid var(--sc-border) !important;
                display: flex !important;
                visibility: visible !important;
                opacity: 1 !important;
                min-width: 290px !important;
                width: 290px !important;
                max-width: 290px !important;
                position: relative !important;
                left: 0 !important;
                top: 0 !important;
                transform: translateX(0) !important;
                margin-left: 0 !important;
                z-index: 10 !important;
            }

            [data-testid="stSidebar"] > div:first-child {
                visibility: visible !important;
                opacity: 1 !important;
                width: 100% !important;
                transform: translateX(0) !important;
            }

            [data-testid="stSidebar"] * { color: var(--sc-text) !important; }
            [data-testid="stSidebar"] .stRadio label {
                background: rgba(15, 23, 42, 0.72);
                border: 1px solid rgba(148, 163, 184, 0.18);
                border-radius: var(--sc-radius-sm);
                margin-bottom: 0.45rem !important;
                padding: 0.68rem 0.9rem !important;
                transition: all 180ms ease;
            }

            [data-testid="stSidebar"] .stRadio label:hover {
                background: rgba(14, 165, 233, 0.14) !important;
                border-color: rgba(125, 211, 252, 0.44) !important;
            }

            .sidebar-profile-card {
                background: rgba(15, 23, 42, 0.84);
                border: 1px solid rgba(148, 163, 184, 0.20);
                border-radius: var(--sc-radius-md);
                margin-bottom: 1.25rem;
                padding: 1rem;
            }

            .sidebar-profile-avatar {
                align-items: center;
                background: var(--sc-gradient);
                border-radius: var(--sc-radius-sm);
                color: #ffffff;
                display: inline-flex;
                font-size: 1.1rem;
                font-weight: 900;
                height: 46px;
                justify-content: center;
                width: 46px;
            }

            .stButton > button {
                border-radius: var(--sc-radius-sm) !important;
                font-weight: 800 !important;
                min-height: 2.8rem !important;
                padding: 0.62rem 1.1rem !important;
                transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease, background 160ms ease !important;
            }

            .stButton > button:focus-visible, input:focus, textarea:focus, [data-baseweb="select"] > div:focus-within {
                box-shadow: var(--sc-focus) !important;
                outline: none !important;
            }

            .stButton > button[kind="primary"] {
                background: var(--sc-gradient) !important;
                border: 1px solid rgba(125, 211, 252, 0.44) !important;
                color: #ffffff !important;
                box-shadow: 0 16px 40px rgba(34, 211, 238, 0.18) !important;
            }

            .stButton > button[kind="primary"]:hover {
                box-shadow: 0 20px 48px rgba(99, 102, 241, 0.26) !important;
                transform: translateY(-1px) !important;
            }

            .stButton > button[kind="secondary"] {
                background: rgba(244, 63, 94, 0.16) !important;
                border: 1px solid rgba(244, 63, 94, 0.42) !important;
                color: #fecdd3 !important;
            }

            .stButton > button[kind="tertiary"], .stButton > button:not([kind]) {
                background: rgba(15, 23, 42, 0.74) !important;
                border: 1px solid rgba(148, 163, 184, 0.24) !important;
                color: #e2e8f0 !important;
            }

            .stButton > button[kind="tertiary"]:hover, .stButton > button:not([kind]):hover {
                background: rgba(30, 41, 59, 0.92) !important;
                border-color: rgba(125, 211, 252, 0.42) !important;
                transform: translateY(-1px) !important;
            }

            .stButton > button:disabled { opacity: 0.48 !important; transform: none !important; }

            label, .stTextInput label, .stSelectbox label, .stFileUploader label, .stCameraInput label, .stAudioInput label {
                color: #dbeafe !important;
                font-weight: 800 !important;
            }

            div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input, textarea, div[data-baseweb="select"] > div {
                background: rgba(15, 23, 42, 0.86) !important;
                border: 1px solid rgba(148, 163, 184, 0.26) !important;
                border-radius: var(--sc-radius-sm) !important;
                color: var(--sc-text) !important;
            }

            div[data-testid="stTextInput"] input::placeholder { color: #64748b !important; }
            [data-testid="stCameraInput"], [data-testid="stFileUploader"], [data-testid="stAudioInput"] {
                background: rgba(15, 23, 42, 0.52);
                border: 1px dashed rgba(125, 211, 252, 0.30);
                border-radius: var(--sc-radius-md);
                padding: 0.8rem;
            }

            .stat-card {
                align-items: center;
                border-radius: var(--sc-radius-md);
                display: flex;
                gap: 0.9rem;
                min-height: 104px;
                padding: 1rem 1.1rem;
            }

            .stat-icon-wrapper { flex: 0 0 auto; font-size: 1.12rem; height: 48px; width: 48px; }
            .stat-icon-indigo { background: linear-gradient(135deg, #6366f1, #38bdf8); }
            .stat-icon-purple { background: linear-gradient(135deg, #8b5cf6, #22d3ee); }
            .stat-icon-emerald, .stat-icon-teal { background: linear-gradient(135deg, #14b8a6, #22c55e); }

            .stat-val {
                color: var(--sc-text);
                font-family: 'Space Grotesk', 'Manrope', sans-serif;
                font-size: 1.8rem;
                font-weight: 700;
                line-height: 1.05;
            }

            .stat-lbl {
                color: var(--sc-muted);
                font-size: 0.82rem;
                font-weight: 800;
                margin-top: 0.2rem;
            }

            .gauge-container { border-radius: var(--sc-radius-lg); padding: 1.45rem; text-align: center; }
            .empty-state {
                border-radius: var(--sc-radius-lg);
                border-style: dashed;
                padding: 2.4rem 1.3rem;
                text-align: center;
            }

            .empty-state-icon {
                align-items: center;
                background: var(--sc-gradient-soft);
                border: 1px solid rgba(125, 211, 252, 0.28);
                border-radius: 50%;
                color: #a5f3fc;
                display: inline-flex;
                font-size: 1.35rem;
                height: 54px;
                justify-content: center;
                margin-bottom: 0.85rem;
                width: 54px;
            }

            .auth-card, .camera-card { border-radius: var(--sc-radius-lg); padding: 1.45rem; }
            .scan-frame {
                border: 1px solid rgba(125, 211, 252, 0.30);
                border-radius: var(--sc-radius-md);
                box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.04);
                margin-top: 1rem;
                padding: 0.8rem;
            }

            .mini-stat { border-radius: var(--sc-radius-md); padding: 1rem; text-align: center; }
            .mini-stat b {
                color: var(--sc-text);
                display: block;
                font-family: 'Space Grotesk', 'Manrope', sans-serif;
                font-size: 1.8rem;
                line-height: 1;
            }

            .mini-stat span { color: var(--sc-muted); display: block; font-size: 0.8rem; font-weight: 800; margin-top: 0.35rem; }
            .progress-track { background: rgba(148, 163, 184, 0.18); border-radius: 999px; height: 0.52rem; overflow: hidden; width: 100%; }
            .progress-fill { animation: scGrowBar 700ms ease both; background: var(--sc-gradient); border-radius: inherit; height: 100%; transform-origin: left; }
            @keyframes scGrowBar { from { transform: scaleX(0.2); } to { transform: scaleX(1); } }

            div[data-testid="stDialog"] > div {
                background: rgba(7, 10, 18, 0.96) !important;
                border: 1px solid rgba(125, 211, 252, 0.28) !important;
                border-radius: var(--sc-radius-lg) !important;
                box-shadow: var(--sc-shadow) !important;
            }

            div[data-testid="stDialog"] * { color: var(--sc-text); }
            .stAlert { border-radius: var(--sc-radius-sm) !important; }
            .stDataFrame, [data-testid="stTable"] {
                border: 1px solid var(--sc-border) !important;
                border-radius: var(--sc-radius-md) !important;
                overflow: hidden !important;
            }

            code, pre {
                background: rgba(15, 23, 42, 0.86) !important;
                border: 1px solid rgba(148, 163, 184, 0.22) !important;
                border-radius: var(--sc-radius-sm) !important;
                color: #a5f3fc !important;
            }

            hr { border-color: rgba(148, 163, 184, 0.18) !important; }

            @media (max-width: 760px) {
                .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
                .home-hero { padding-top: 2rem; }
                .hub-hero { padding: 1.35rem; }
                .feature-grid { grid-template-columns: 1fr; }
                .portal-card, .wf-card, .cap-card { min-height: auto; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
