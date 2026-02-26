from datetime import date, timedelta

def generate_schedule(topics, exam_date, daily_hours, subject_name, level):
    today = date.today()
    total_days_until_exam = (exam_date - today).days

    if total_days_until_exam <= 2:
        raise ValueError("Not enough days before exam.")

    difficulty_weight = {
        "Beginner": {"Easy": 1, "Medium": 2, "Hard": 3},
        "Intermediate": {"Easy": 1, "Medium": 2, "Hard": 4},
        "Advanced": {"Easy": 0, "Medium": 1, "Hard": 2},
    }

    for t in topics:
        t["priority"] = difficulty_weight[level].get(t["difficulty"], 1)

    topics = sorted(topics, key=lambda x: x["priority"], reverse=True)

    plan = []
    current_date = today
    topics_completed = []

    reserve_revision_days = min(3, total_days_until_exam // 4)
    study_deadline = exam_date - timedelta(days=reserve_revision_days)

    for topic in topics:
        hours_needed = topic["estimated_hours"]
        
        # Split hours between Reading and Practice based on difficulty
        if topic["difficulty"] == "Easy":
            reading_hours = hours_needed
            practice_hours = 0
        elif topic["difficulty"] == "Medium":
            reading_hours = max(1, hours_needed // 2)
            practice_hours = hours_needed - reading_hours
        else:  # Hard
            reading_hours = max(1, hours_needed // 3)
            practice_hours = hours_needed - reading_hours

        # Add Reading sessions first
        hours_allocated = 0
        while hours_allocated < reading_hours:
            if current_date >= study_deadline:
                break

            remaining_hours = reading_hours - hours_allocated
            session_hours = min(remaining_hours, daily_hours)

            plan.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "subject": subject_name,
                "topic": topic["topic_name"],
                "study_type": "Reading",
                "duration_hours": session_hours
            })

            hours_allocated += session_hours
            current_date += timedelta(days=1)

        # Add Practice sessions after Reading
        hours_allocated = 0
        while hours_allocated < practice_hours:
            if current_date >= study_deadline:
                break

            remaining_hours = practice_hours - hours_allocated
            session_hours = min(remaining_hours, daily_hours)

            plan.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "subject": subject_name,
                "topic": topic["topic_name"],
                "study_type": "Practice",
                "duration_hours": session_hours
            })

            hours_allocated += session_hours
            current_date += timedelta(days=1)

        topics_completed.append(topic["topic_name"])

    revision_date = current_date
    revision_count = 0
    max_revisions = min(reserve_revision_days, (exam_date - revision_date).days)

    for i in range(max_revisions):
        if revision_date >= exam_date:
            break

        if i == max_revisions - 1:
            revision_topic = "Final Exam Preparation"
        elif revision_count < len(topics_completed):
            revision_topic = f"Revision: {topics_completed[revision_count]}"
            revision_count += 1
        else:
            revision_topic = "Full Subject Revision"

        plan.append({
            "date": revision_date.strftime("%Y-%m-%d"),
            "subject": subject_name,
            "topic": revision_topic,
            "study_type": "Revision",
            "duration_hours": daily_hours
        })

        revision_date += timedelta(days=1)

    return plan
