import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject
import time

@st.dialog("Enroll in subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. BCS401')

    if st.button('Enroll new', type='primary', width='stretch'):
        if join_code:
            res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', join_code).execute()
            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data['student_id']

                check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('subject_id', subject_id).execute()
                if check.data:
                    st.warning('You are already Enrolled in this class')
                else:
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success('Successfully enrolled!')
                    time.sleep(1)
                    st.rerun()

        else:
            st.warning('Please enter a subject code')