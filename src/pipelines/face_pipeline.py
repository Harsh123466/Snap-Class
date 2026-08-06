import numpy as np
import streamlit as st
from sklearn.svm import SVC
import dlib
import face_recognition_models

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()    # its is use for detect where faces are located in an image


    sp = dlib.shape_predictor(                     # its is use for find importants facial landmarks like eye corners, nose tip, jawline, mouth corner , etc
        face_recognition_models.pose_predictor_model_location()
    )


    facerec = dlib.face_recognition_model_v1(      # Converts an aligned face into a numerical embedding.
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 1)

    encoding = []

    for face in faces:
        shape = sp(image_np, face)

        embedding = facerec.compute_face_descriptor(image_np, shape, 1)    # 128 embedding

        encoding.append(np.array(embedding))

    return encoding


@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        print("Database is empty")
        return None

    for student in student_db:
        embedding = student.get("face_embedding")
        student_id = student.get("student_id")

        if embedding is not None and student_id is not None:
            X.append(np.array(embedding, dtype=np.float32))
            y.append(int(student_id))

    if len(X) == 0:
        print("No face embeddings found")
        return None

    unique_students = sorted(list(set(y)))

    print("=" * 50)
    print("Training Model")
    print("Total Samples :", len(X))
    print("Unique Students :", unique_students)
    print("=" * 50)

    # Only one student registered
    if len(unique_students) == 1:
        print("Single student mode. Skipping SVM training.")
        return {
            "clf": None,
            "X": X,
            "y": y
        }

    clf = SVC(
        kernel="linear",
        class_weight="balanced"
    )

    clf.fit(X, y)

    return {
        "clf": clf,
        "X": X,
        "y": y
    }



def train_classifier():
    st.cache_resource.clear()

    model_data = get_trained_model()

    if model_data is None:
        print("Model creation failed")
        return False

    print("Model Ready")
    return True




def predict_attendance(class_image_np):

    encodings = get_face_embeddings(class_image_np)

    detected_student = {}

    model_data = get_trained_model()

    if model_data is None:
        return detected_student, [], len(encodings)

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:

        # -------------------------
        # Single Student Mode
        # -------------------------
        if clf is None:

            distance = np.linalg.norm(X_train[0] - encoding)

            print("Single Student Distance :", distance)

            # You can tune this after testing
            if distance <= 0.45:
                detected_student[int(y_train[0])] = True

            continue

        # -------------------------
        # Multi Student Mode
        # -------------------------
        predicted_id = int(clf.predict([encoding])[0])

        idx = y_train.index(predicted_id)

        student_embedding = X_train[idx]

        distance = np.linalg.norm(student_embedding - encoding)

        print("Predicted :", predicted_id)
        print("Distance :", distance)

        if distance <= 0.45:
            detected_student[predicted_id] = True

    return detected_student, all_students, len(encodings)