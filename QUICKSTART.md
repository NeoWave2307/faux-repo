# 🚀 Quick Start Guide - GenAI Curriculum Generator

## What You Have

A complete **RAG-powered curriculum generator** that creates professional educational curricula using:
- **Google Gemini 1.5 Pro** (Free tier)
- **ChromaDB** (Local vector database)
- **Streamlit** (Web interface)

**Cost: $0** for development and moderate usage!

---

## ⚡ Super Quick Setup - One Command!

### Automated Setup (Recommended)

```bash
python setup.py
```

That's it! This single command:
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Populates the knowledge base
- ✅ Launches the Streamlit app

---

## 🔧 Manual Setup (Alternative)

### Step 0: Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
# source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 1: Get Google API Key (Free)

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key

### Step 2: Configure Environment

Create a `.env` file in the project root:

```bash
# Copy the example file (recommended)
cp .env.example .env

# Then edit .env and add your API key
GOOGLE_API_KEY=paste_your_key_here
```

### Step 3: Initialize Knowledge Base

```bash
python populate_knowledge_base.py
```

This automatically scans **all folders** under `data/knowledge_base/` and loads all `.md` files.

Current curriculum files:
- CSE Core Curriculum
- Civil Engineering (CE) AR22
- Electronics & Communication (ECE) AR22
- Mechanical Engineering (ME) AR22
- ML/AI programs (BTech AI, Masters ML)
- Web Development bootcamp
- Templates

---

## 🎯 Run the Application

```bash
streamlit run app.py
```

The app will open at: **http://localhost:8501**

---

## 📝 How to Use

1. **Enter Parameters:**
   - Subject: "Machine Learning", "Data Science", "Web Development", etc.
   - Level: BTech, Masters, Diploma, or Certification
   - Duration: Number of semesters (1-12)
   - Optional: Specialization and focus areas

2. **Generate:**
   - Click "🚀 Generate Curriculum"
   - Wait 30-60 seconds for AI generation

3. **Review:**
   - View in organized tabs (Overview, Semesters, Outcomes, Validation)
   - Check validation results

4. **Download:**
   - Click "📥 Download PDF"
   - Get professional curriculum document

---

## 🎓 Example Subjects to Try

- Machine Learning
- Data Science
- Artificial Intelligence
- Web Development
- Cloud Computing
- Cybersecurity
- Blockchain
- DevOps
- Mobile App Development
- Game Development

---

## 📦 What's Included

### Knowledge Base (4 Examples)
- ✅ Masters in Machine Learning (4 semesters)
- ✅ BTech in Artificial Intelligence (8 semesters)
- ✅ Full-Stack Web Development Bootcamp (6 months)
- ✅ Generic Curriculum Template

### Features
- ✅ RAG-powered generation (uses similar examples)
- ✅ Professional PDF export
- ✅ Curriculum validation
- ✅ Beautiful Streamlit UI
- ✅ 100% free tier

---

## 🔧 Troubleshooting

### "GOOGLE_API_KEY not found"
- Create `.env` file with your API key
- Make sure it's in the project root directory

### "Knowledge base not initialized"
- Run: `python populate_knowledge_base.py`

### "Module not found"
- Run: `pip install -r requirements.txt`

### Rate limit errors
- Free tier: 60 requests/min, 1500/day
- Wait a minute and try again

---

## 📊 Free Tier Limits

**Google Gemini:**
- 60 requests per minute
- 1500 requests per day
- No credit card required

**Perfect for:**
- Development
- Testing
- Personal projects
- Small-scale usage

---

## 🎯 Next Steps

1. **Get your API key** from Google AI Studio
2. **Create `.env` file** with your key
3. **Run the app**: `streamlit run app.py`
4. **Generate your first curriculum!**

---

## 📚 Documentation

- **Full README**: [README.md](file:///c:/Users/sparg/Documents/faux-repo/README.md)
- **Implementation Plan**: See artifacts
- **Walkthrough**: Complete implementation details

---

**Ready to generate professional curricula in seconds!** 🎓✨
