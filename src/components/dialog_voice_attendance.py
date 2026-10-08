from datetime import datetime
import pandas as pd
import streamlit as st

from src.components.dialog_attendance_results import show_attendance_result
from src.database.config import supabase
from src.pipelines.voice_pipeline import process_bulk_audio


@st.dialog("AI Voice Verification & Attendance")
def voice_attendance_dialog(selected_subject_id):
    st.markdown(
        """
        <div style="background:#f0fdfa; border:1px solid #99f6e4; border-radius:12px; padding:1rem; margin-bottom:1.25rem;">
            <div style="display:flex; align-items:center; gap:0.5rem; color:#0f766e; font-weight:700; margin-bottom:0.3rem;">
                🎙️ Voice Verification Guide
            </div>
            <p style="margin:0; color:#134e4a !important; font-size:0.9rem;">
                Record classroom audio while enrolled students state their phrase. The voice embedding model will compare similarities against enrolled profiles.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    audio_data = st.audio_input("Record classroom audio")

    if st.button("Analyze Classroom Audio", width="stretch", type="primary"):
        if not audio_data:
            st.warning("Please record classroom audio first.")
            return

        with st.spinner("Analyzing audio frequencies and comparing student voice embeddings..."):
            enrolled_res = (
                supabase.table("subject_students")
                .select("*, students(*)")
                .eq("subject_id", selected_subject_id)
                .execute()
            )
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students are enrolled in this subject.")
                return

            candidates_dict = {
                s["students"]["student_id"]: s["students"]["voice_embedding"]
                for s in enrolled_students
                if s["students"].get("voice_embedding")
            }

            if not candidates_dict:
                st.error("No enrolled students have registered voice profiles yet.")
                return

            detected_scores = process_bulk_audio(audio_data.read(), candidates_dict)
            results, attendance_to_log = [], []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node["students"]
                score = detected_scores.get(student["student_id"], 0.0)
                is_present = bool(score > 0)

                results.append(
                    {
                        "Name": student["name"],
                        "ID": student["student_id"],
                        "Similarity Score": round(score, 3) if is_present else "-",
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

            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    if st.session_state.get("voice_attendance_results"):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs)
