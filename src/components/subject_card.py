import html

import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None, progress=None):
    """Render a safe subject card using Streamlit layout primitives."""
    safe_name = html.escape(str(name))
    safe_code = html.escape(str(code))
    safe_section = html.escape(str(section))

    with st.container(border=True):
        title_col, progress_col = st.columns([4, 1.2])

        with title_col:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap; margin-bottom:0.35rem;">
                    <span class="eyebrow">Section {safe_section}</span>
                    <span class="status-chip success">Active</span>
                </div>
                <div class="panel-title" style="font-size:1.25rem !important; margin:0 0 0.45rem !important;">{safe_name}</div>
                <div class="muted-copy">
                    Join code
                    <code style="padding:0.14rem 0.45rem; margin-left:0.35rem; font-size:0.82rem;">{safe_code}</code>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with progress_col:
            if progress is not None:
                val = max(0, min(100, int(progress)))
                tone = "success" if val >= 75 else "warn" if val >= 50 else "danger"
                status = "Healthy" if val >= 75 else "Watch" if val >= 50 else "At risk"
                st.markdown(
                    f"""
                    <div style="min-width: 112px; text-align: right;">
                        <div class="status-chip {tone}" style="margin-bottom:0.7rem;">{status} | {val}%</div>
                        <div class="progress-track" aria-label="Attendance {val}%">
                            <div class="progress-fill" style="width:{val}%;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        if stats:
            chips = []
            for icon, label, value in stats:
                safe_icon = html.escape(str(icon))
                safe_label = html.escape(str(label))
                safe_value = html.escape(str(value))
                chips.append(
                    f'<span class="chip"><span>{safe_icon}</span><strong>{safe_value}</strong> {safe_label}</span>'
                )

            st.markdown(
                f'<div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:1rem;">{"".join(chips)}</div>',
                unsafe_allow_html=True,
            )

    if footer_callback:
        footer_callback()
