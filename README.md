# 🎓 GenAI Curriculum Generator

**AI-Powered Educational Curriculum Design with RAG, ChromaDB, and Free-Tier Services**

Generate professional, comprehensive educational curricula for any subject using Retrieval-Augmented Generation (RAG) and Google Gemini's free tier.

![Tech Stack](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-purple)
![Gemini](https://img.shields.io/badge/Google-Gemini%201.5%20Pro-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- 🤖 **RAG-Powered Generation**: Uses similar curriculum examples for context-aware generation
- 💰 **100% Free Tier**: Google Gemini (15 req/min, 1500/day) + local ChromaDB
- 🗄️ **Local Vector Store**: ChromaDB for persistent curriculum knowledge base
- 📄 **Professional PDFs**: University-grade curriculum documents with ReportLab
- ✅ **Validation**: Automatic curriculum quality checks
- 🎨 **Beautiful UI**: Modern Streamlit interface with no frontend code
- 🔧 **Structured Output**: Pydantic models ensure data quality

## 📖 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete usage guide: RAG system, adding documents, customization
- **[QUICKSTART.md](QUICKSTART.md)** - Quick 3-step setup guide
- **[ERROR_RESOLUTION.md](ERROR_RESOLUTION.md)** - API errors and solutions
- **[.env.example](.env.example)** - Configuration template

## 🏗️ Architecture

```
User Input → RAG Retrieval (ChromaDB) → Context + Prompt → Gemini LLM → Validation → PDF
```

**Tech Stack:**
- **Frontend:** Streamlit (zero-code UI)
- **LLM:** Google Gemini 1.5 Pro (free tier)
- **Vector DB:** ChromaDB (local, persistent)
- **Embeddings:** Sentence Transformers (free, local)
- **PDF:** ReportLab
- **Orchestration:** LangChain

## 🚀 Quick Start

### One-Command Setup ⚡

```bash
python setup.py
```

This **single command** does everything:
1. ✅ Creates virtual environment (`venv/`)
2. ✅ Installs all dependencies
3. ✅ Populates ChromaDB knowledge base
4. ✅ Asks if you want to launch the app
5. ✅ Runs Streamlit automatically

**Then just add your Google API key** (see Configuration below).

---

### Manual Setup (Alternative)

#### 1. Prerequisites

- Python 3.8 or higher
- Google API Key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

#### 2. Installation

```bash
# Clone the repository
cd faux-repo

# Create and activate virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configuration

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Or create manually with:
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get your free API key from: https://makersuite.google.com/app/apikey

#### 4. Initialize Knowledge Base

Populate ChromaDB with curriculum examples:

```bash
python populate_knowledge_base.py
```

This automatically scans **all folders** under `data/knowledge_base/` for `.md` files.

#### 5. Verify API (Optional)

Check if your API key has available quota:

```bash
python check_quota.py
```

### 6. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Enter Curriculum Parameters:**
   - Subject/Skill Area (e.g., "Machine Learning", "Data Science")
   - Education Level (BTech, Masters, Diploma, Certification)
   - Duration in semesters
   - Optional: Specialization and focus areas

2. **Generate Curriculum:**
   - Click "Generate Curriculum"
   - RAG retrieves similar examples from ChromaDB
   - Gemini generates structured curriculum with context
   - Validation checks ensure quality

3. **Review and Download:**
   - View curriculum in organized tabs
   - Check validation results
   - Download professional PDF

## 📁 Project Structure

```
faux-repo/
├── app.py                          # Main Streamlit application
├── populate_knowledge_base.py      # Initialize vector store
├── requirements.txt                # Dependencies
├── .env.example                    # Environment template
├── .streamlit/
│   └── config.toml                 # Streamlit config
├── src/
│   ├── rag/
│   │   ├── vector_store.py        # ChromaDB wrapper
│   │   ├── embeddings.py          # Sentence Transformers
│   │   └── retriever.py           # RAG retrieval logic
│   ├── llm/
│   │   ├── client.py              # Gemini client
│   │   └── prompts.py             # Generation prompts
│   ├── curriculum/
│   │   ├── models.py              # Pydantic models
│   │   ├── generator.py           # Main generator
│   │   └── validator.py           # Validation logic
│   └── pdf/
│       └── generator.py           # PDF generation
└── data/
    ├── knowledge_base/            # Curriculum examples
    │   ├── ml_curricula/
    │   ├── web_dev_curricula/
    │   └── templates/
    └── vector_db/                 # ChromaDB storage (auto-created)
```

## 🎯 Example Curricula

The knowledge base includes:

- **Masters in Machine Learning** (4 semesters)
- **BTech in Artificial Intelligence** (8 semesters)
- **Full-Stack Web Development Bootcamp** (6 months)
- Generic curriculum template

## 💡 How It Works

### RAG Pipeline

1. **User Input**: Subject, level, duration, specialization
2. **Retrieval**: ChromaDB finds 3 most similar curricula
3. **Context**: Similar examples formatted for LLM
4. **Generation**: Gemini creates curriculum with context
5. **Validation**: Check credits, structure, completeness
6. **Output**: Structured JSON → Pydantic models → PDF

### Free Tier Optimization

- **Google Gemini**: 60 requests/min, 1500/day (free)
- **ChromaDB**: Local, persistent, no cost
- **Sentence Transformers**: Local embeddings, no API calls
- **Total Cost**: $0 for development and moderate usage

## 🔧 Customization

### Add Your Own Curricula

1. Create markdown files in `data/knowledge_base/`
2. Follow the template structure
3. Run `python populate_knowledge_base.py`

### Adjust Generation Parameters

Edit `src/llm/prompts.py` to customize:
- System prompts
- Output format
- Credit hour requirements
- Course categories

### Modify PDF Styling

Edit `src/pdf/generator.py` to change:
- Colors and fonts
- Layout and spacing
- Table styles
- Header/footer

## 📊 Validation

The validator checks:
- ✅ Semester count matches duration
- ✅ Credit hours balanced (12-24 per semester)
- ✅ Total credits match sum
- ✅ No duplicate course codes
- ✅ Required fields present

## 🐛 Troubleshooting

### "Knowledge base not initialized"
Run: `python populate_knowledge_base.py`

### "GOOGLE_API_KEY not found"
Create `.env` file with your API key

### "Rate limit exceeded"
Free tier: 60 req/min, 1500/day. Wait and retry.

### Import errors
Run: `pip install -r requirements.txt`

## 🚀 Deployment

### Streamlit Community Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Add `GOOGLE_API_KEY` to secrets
5. Deploy!

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD streamlit run app.py --server.port 8080
```

## 📝 License

MIT License - feel free to use for any purpose!

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional curriculum examples
- More validation rules
- Enhanced PDF templates
- Multi-language support
- Export to other formats (Word, JSON)

## 🙏 Acknowledgments

- **Google Gemini** for free LLM API
- **ChromaDB** for simple vector storage
- **Streamlit** for rapid UI development
- **Sentence Transformers** for local embeddings

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review example curricula in `data/knowledge_base/`
3. Ensure `.env` is configured correctly

---

**Built with ❤️ using 100% free-tier services**

*No credit card required. No hidden costs. Just AI-powered curriculum generation.*
