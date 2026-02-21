# AI Study Planner

AI Study Planner is a smart study scheduling system that helps students organize their preparation before exams.

## 🚀 Features

- Input subjects and exam dates
- Select student level (Beginner / Intermediate / Advanced)
- Upload syllabus PDFs
- Analyze PDFs using RAG
- Prioritize topics based on importance and difficulty
- Generate a structured daily study plan
- Export study plan as CSV
- Generate optional summaries for each unit

## 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- RAG Pipeline
- Hugging Face / OpenAI Models

## 📂 Project Structure

- `src/` → Core logic
- `data/` → Uploaded PDFs
- `outputs/` → Generated study plans and summaries
- `tests/` → Unit tests

## ▶ How to Run

```bash
pip install -r requirements.txt
streamlit run src/ui.py
```
