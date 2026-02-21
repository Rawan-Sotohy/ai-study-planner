from dataclasses import dataclass, field
from datetime import date
from typing import List

@dataclass
class SubjectInput:
    name: str
    exam_date: date
    pdf_path: str
    level: str  # Beginner / Intermediate / Advanced

@dataclass
class StudentProfile:
    student_name: str
    subjects: List[SubjectInput]
    daily_study_hours: int = 3

def validate_profile(profile: StudentProfile) -> bool:
    today = date.today()
    for subj in profile.subjects:
        if subj.exam_date <= today:
            raise ValueError(f"Exam date for {subj.name} must be in the future.")
        if subj.level not in ["Beginner", "Intermediate", "Advanced"]:
            raise ValueError(f"Invalid level for {subj.name}.")
    return True