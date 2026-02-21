import streamlit as st
import pandas as pd
from datetime import date
import os

from src.data_input import SubjectInput, StudentProfile, validate_profile
from src.pdf_reader import load_and_chunk_pdf, create_vector_store
from src.topic_analyzer import extract_topics, rank_topics
from src.scheduler import generate_schedule
from src.summary_generator import generate_summary, save_summary
from src.config import UPLOADS_PATH, OUTPUTS_PATH

# ---- Page Config ----
st.set_page_config(page_title="AI Study Planner", page_icon="📚", layout="wide")
st.title("📚 AI Study Planner")
st.markdown("A smart personalized study plan based on your syllabus")

# ---- Sidebar ----
with st.sidebar:
    st.header("👤 Student Info")
    student_name = st.text_input("Your Name")
    daily_hours = st.slider("Daily Study Hours", 1, 8, 3)
    num_subjects = st.number_input("Number of Subjects", 1, 6, 2)
    generate_summaries = st.checkbox("Generate topic summaries?")

# ---- Subject Inputs ----
st.header("📖 Subjects")
subjects_data = []

for i in range(int(num_subjects)):
    st.subheader(f"Subject {i + 1}")
    col1, col2, col3 = st.columns(3)

    name = col1.text_input("Subject Name", key=f"name_{i}")
    level = col2.selectbox(
        "Student Level",
        ["Beginner", "Intermediate", "Advanced"],
        key=f"level_{i}"
    )
    exam_date = col3.date_input(
        "Exam Date",
        min_value=date.today(),
        key=f"date_{i}"
    )

    pdf_file = st.file_uploader(
    f"Upload syllabus for {name}",
    type=["pdf", "docx", "txt"],
    key=f"pdf_{i}"
)

    if pdf_file and name:
        os.makedirs(UPLOADS_PATH, exist_ok=True)
        pdf_path = f"{UPLOADS_PATH}/{name}_{pdf_file.name}"
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.read())

        subjects_data.append(SubjectInput(
            name=name,
            exam_date=exam_date,
            pdf_path=pdf_path,
            level=level
        ))

# ---- Generate Button ----
st.divider()

if st.button("🚀 Generate My Study Plan!", use_container_width=True):
    if not student_name:
        st.error("Please enter your name first!")
    elif not subjects_data:
        st.error("Please upload a PDF for each subject!")
    else:
        try:
            profile = StudentProfile(
                student_name=student_name,
                subjects=subjects_data,
                daily_study_hours=daily_hours
            )
            validate_profile(profile)

            full_plan = []

            for subj in profile.subjects:
                with st.spinner(f"⏳ Processing {subj.name}..."):

                    # 1. Read PDF
                    st.info(f"📄 Reading PDF for {subj.name}...")
                    chunks = load_and_chunk_pdf(subj.pdf_path)
                    create_vector_store(chunks, subj.name)

                    # 2. Extract Topics
                    st.info(f"🔍 Extracting topics from {subj.name}...")
                    topics = extract_topics(subj.name, subj.level)
                    ranked = rank_topics(topics, subj.level)

                    # 3. Generate Schedule
                    st.info(f"📅 Building study plan for {subj.name}...")
                    plan = generate_schedule(
                        ranked, subj.exam_date,
                        daily_hours, subj.name, subj.level
                    )
                    full_plan.extend(plan)

                    # 4. Summaries (optional)
                    if generate_summaries:
                        st.info(f"📝 Generating summaries for {subj.name}...")
                        for topic in ranked[:3]:
                            summary = generate_summary(subj.name, topic["topic_name"])
                            save_summary(subj.name, topic["topic_name"], summary)

                    st.success(f"✅ {subj.name} done!")

            # ---- Display Plan ----
            st.header("🗓️ Your Study Plan")
            df = pd.DataFrame(full_plan).sort_values(["date", "subject"])
            st.dataframe(df, use_container_width=True)

            # ---- Export CSV ----
            os.makedirs(OUTPUTS_PATH, exist_ok=True)
            csv = df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Plan as CSV",
                data=csv,
                file_name=f"{student_name}_study_plan.csv",
                mime="text/csv",
                use_container_width=True
            )

        except ValueError as e:
            st.error(f"❌ Error: {e}")
        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")