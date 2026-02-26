# 📚 AI Study Planner

Smart AI-powered personalized study planner that uses RAG (Retrieval-Augmented Generation) to create optimized study schedules from syllabus PDFs.

## 🎯 Features

- **PDF Syllabus Analysis**: Upload syllabus PDFs and extract topics automatically using RAG
- **Personalized Scheduling**: Generate study plans based on exam dates, daily hours, and difficulty level
- **Smart Study Types**: 
  - 📖 **Reading**: Learn new easy topics
  - ✍️ **Practice**: Solve problems & exercises for medium/hard topics
  - 🔄 **Revision**: Review all material before exams
- **Multi-Subject Support**: Manage multiple subjects with separate plans
- **AI Summaries**: Optional AI-generated summaries for top topics
- **Export to CSV**: Download study plans for offline use

---

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **LLM**: Groq API (llama-3.3-70b-versatile)
- **RAG Pipeline**: LangChain + FAISS vector store
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **PDF Processing**: PyPDF2

---

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-study-planner.git
cd ai-study-planner
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key from: https://console.groq.com/

## 💻 Usage

1. **Run the application**
```bash
python -m streamlit run src/ui.py
```

2. **Follow the steps in the UI:**

### Step 1: Student Info
- Enter your name
- Set daily study hours (1-8)
- Choose number of subjects

### Step 2: Upload Subjects
- For each subject:
  - Enter subject name
  - Select difficulty level (Beginner/Intermediate/Advanced)
  - Choose exam date
  - Upload syllabus PDF
- Click "Save Subjects"

### Step 3: Generate Plan
- Optional: Check "Generate AI Summaries for Top Topics"
- Click "Generate My Smart Plan"
- View your personalized study schedule in tabs
- Download CSV files from the `outputs/` folder

---

## 🧠 How It Works

### RAG Pipeline
1. Upload PDF → Extract text
2. Split into chunks (800 tokens, 100 overlap)
3. Generate embeddings using sentence-transformers
4. Store in FAISS vector database
5. Retrieve relevant topics based on queries

### Study Plan Generation
1. Extract topics from PDF using LLM + RAG
2. Assign difficulty levels (Easy/Medium/Hard)
3. Calculate priority based on student level
4. Distribute hours across days:
   - **Easy topics**: 100% Reading
   - **Medium topics**: 50% Reading + 50% Practice
   - **Hard topics**: 33% Reading + 67% Practice
5. Reserve 25% of time for Revision
6. Add "Final Exam Preparation" before exam

