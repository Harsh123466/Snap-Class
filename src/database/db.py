from src.database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def check_pass(pwd, hased):
    return bcrypt.checkpw(pwd.encode(), hased.encode())


def check_teacher_exists(username):
    # checks for unique username, return false when username is already exists
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0


def create_teacher(username, password, name): 
    data = {"username":username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username",username).execute()    # fetch teacher info from database then check teacher's username is exists
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):    # this is for check entered password is correct or not
            return teacher
        
    return None




def get_all_students():
    response = supabase.table('students').select('*').execute()
    return response.data


def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding':face_embedding, 'voice_embedding':voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {'subject_code':subject_code, 'name':name, 'section':section, 'teacher_id':teacher_id}
    response = supabase.table('subjects').insert(data).execute()

    return response.data


def get_teacher_subjects(teacher_id):
    response = supabase.table('subject').select('*,subject_student(count), attendance_logs(timestamp)').eq('teacher_id', teacher_id).execute()
    subjects = response.data

    # for sub in subjects:   
