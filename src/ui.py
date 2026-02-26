import streamlit as st
import pandas as pd
from datetime import date
import os
import shutil

from src.data_input import SubjectInput, StudentProfile, validate_profile
from src.pdf_reader import load_and_chunk_pdf, create_vector_store
from src.topic_analyzer import extract_topics
from src.scheduler import generate_schedule
from src.summary_generator import generate_summary, save_summary
from src.config import UPLOADS_PATH, OUTPUTS_PATH


# Page Config

st.set_page_config(page_title="AI Study Planner", page_icon="📚", layout="wide")
st.title("📚 AI Study Planner")
st.markdown("Smart AI-powered personalized study planner")


# Session State Init

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "daily_hours" not in st.session_state:
    st.session_state.daily_hours = 3

if "num_subjects" not in st.session_state:
    st.session_state.num_subjects = 2

if "subjects_data" not in st.session_state:
    st.session_state.subjects_data = []

if "generated_plan" not in st.session_state:
    st.session_state.generated_plan = []


# Sidebar Navigation

step = st.sidebar.radio(
    "Navigation",
    ["1️⃣ Student Info", "2️⃣ Upload Subjects", "3️⃣ Generate Plan"]
)


# STEP 1 — Student Info

if step == "1️⃣ Student Info":

    st.header("👤 Student Information")

    st.session_state.student_name = st.text_input(
        "Your Name",
        value=st.session_state.student_name
    )

    st.session_state.daily_hours = st.slider(
        "Daily Study Hours",
        1, 8,
        value=st.session_state.daily_hours
    )

    st.session_state.num_subjects = st.number_input(
        "Number of Subjects",
        1, 6,
        value=st.session_state.num_subjects
    )

    st.success("Go to 'Upload Subjects' from sidebar.")


# STEP 2 — Upload Subjects

elif step == "2️⃣ Upload Subjects":

    if not st.session_state.student_name:
        st.warning("Please complete Student Info first.")
        st.stop()

    st.header("📖 Upload Subjects & Syllabus")

    if "temp_subjects" not in st.session_state:
        st.session_state.temp_subjects = {}
    
    if "uploaded_pdfs" not in st.session_state:
        st.session_state.uploaded_pdfs = {}

    for i in range(int(st.session_state.num_subjects)):

        st.subheader(f"Subject {i + 1}")

        col1, col2, col3 = st.columns(3)

        name_key = f"name_{i}"
        level_key = f"level_{i}"
        date_key = f"date_{i}"
        
        name = col1.text_input("Subject Name", key=name_key)
        level = col2.selectbox(
            "Student Level",
            ["Beginner", "Intermediate", "Advanced"],
            key=level_key
        )
        exam_date = col3.date_input(
            "Exam Date",
            min_value=date.today(),
            key=date_key
        )

        pdf_file = st.file_uploader(
            f"Upload syllabus for {name if name else 'Subject'}",
            type=["pdf"],
            key=f"pdf_{i}"
        )

        if pdf_file and i not in st.session_state.uploaded_pdfs:
            os.makedirs(UPLOADS_PATH, exist_ok=True)
            pdf_path = f"{UPLOADS_PATH}/{name if name else f'subject_{i}'}_{pdf_file.name}"
            
            with open(pdf_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            
            st.session_state.uploaded_pdfs[i] = pdf_path

        if name and i in st.session_state.uploaded_pdfs:
            st.session_state.temp_subjects[i] = SubjectInput(
                name=name,
                exam_date=exam_date,
                pdf_path=st.session_state.uploaded_pdfs[i],
                level=level
            )

    if st.session_state.temp_subjects:
        st.info(f"Saved {len(st.session_state.temp_subjects)} out of {int(st.session_state.num_subjects)} subjects")

    if st.button("Save Subjects"):

        if len(st.session_state.temp_subjects) != int(st.session_state.num_subjects):
            st.error(f"Please complete all subjects before saving. Currently saved: {len(st.session_state.temp_subjects)}/{int(st.session_state.num_subjects)}")
        else:
            st.session_state.subjects_data = list(
                st.session_state.temp_subjects.values()
            )
            st.success("Subjects saved successfully!")
            st.info("Now go to 'Generate Plan'.")



# STEP 3 — Generate Plan

elif step == "3️⃣ Generate Plan":

    if not st.session_state.subjects_data:
        st.warning("Please upload and save subjects first.")
        st.stop()

    st.header("🚀 Generate Study Plan")

    generate_summaries = st.checkbox("Generate AI Summaries for Top Topics?")

    if st.button("Generate My Smart Plan", use_container_width=True):

        profile = StudentProfile(
            student_name=st.session_state.student_name,
            subjects=st.session_state.subjects_data,
            daily_study_hours=st.session_state.daily_hours
        )

        try:
            validate_profile(profile)

            if os.path.exists(OUTPUTS_PATH):
                shutil.rmtree(OUTPUTS_PATH)

            os.makedirs(OUTPUTS_PATH, exist_ok=True)

            st.session_state.generated_plan = []

            for subj in profile.subjects:

                with st.spinner(f"Processing {subj.name}..."):

                    chunks = load_and_chunk_pdf(subj.pdf_path)
                    create_vector_store(chunks, subj.name)

                    topics = extract_topics(subj.name, subj.level)

                    plan = generate_schedule(
                        topics,
                        subj.exam_date,
                        profile.daily_study_hours,
                        subj.name,
                        subj.level
                    )

                    st.session_state.generated_plan.extend(plan)

                    subject_folder = os.path.join(
                        OUTPUTS_PATH,
                        subj.name.replace(" ", "_")
                    )
                    os.makedirs(subject_folder, exist_ok=True)

                    pd.DataFrame(plan).to_csv(
                        os.path.join(subject_folder, "study_plan.csv"),
                        index=False
                    )

                    if generate_summaries:
                        for topic in topics[:3]:
                            summary = generate_summary(
                                subj.name,
                                topic["topic_name"]
                            )
                            save_summary(
                                summary,
                                subj.name,
                                topic["topic_name"]
                            )

                st.success(f"{subj.name} completed!")

        except Exception as e:
            st.error(f"Error: {e}")


    # DISPLAY SUBJECT TABS

    if st.session_state.generated_plan:

        st.divider()
        st.header("🗂 Subject Study Plans")

        subjects = st.session_state.subjects_data
        subject_names = [s.name for s in subjects]

        tabs = st.tabs(subject_names)

        for i, subj in enumerate(subjects):

            with tabs[i]:

                subject_plan = [
                    row for row in st.session_state.generated_plan
                    if row["subject"] == subj.name
                ]

                if subject_plan:

                    df = pd.DataFrame(subject_plan)
                    df["date"] = pd.to_datetime(df["date"])
                    df = df.sort_values("date")
                    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

                    st.subheader("Study Plan")
                    st.dataframe(df, use_container_width=True)

                    st.metric(
                        "Total Study Hours",
                        df["duration_hours"].sum()
                    )

                    st.subheader("📚 Topic Summaries")

                    subject_folder = os.path.join(
                        OUTPUTS_PATH,
                        subj.name.replace(" ", "_")
                    )

                    if os.path.exists(subject_folder):

                        summary_files = [
                            f for f in os.listdir(subject_folder)
                            if f.endswith(".txt")
                        ]

                        if summary_files:
                            for file in summary_files:

                                file_path = os.path.join(subject_folder, file)

                                with open(file_path, "r", encoding="utf-8") as f:
                                    content = f.read()

                                with st.expander(file.replace(".txt", "")):
                                    st.write(content)
                        else:
                            st.info("No summaries generated.")

                else:
                    st.info("No plan generated for this subject.")
