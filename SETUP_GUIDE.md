# 🚀 Quick Setup Guide

## For New Team Members

### One-Command Setup ⚡
```bash
python setup.py
```

This **single command** automatically:
1. ✅ Creates virtual environment (`venv/`)
2. ✅ Installs all dependencies
3. ✅ Populates ChromaDB knowledge base
4. ✅ Checks for .env configuration
5. ✅ Asks if you want to launch the app
6. ✅ Runs Streamlit if you choose 'y'

---

## Manual Setup (Alternative)

If you prefer step-by-step:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Populate Knowledge Base
```bash
python populate_knowledge_base.py
```
- Creates local ChromaDB vector database
- Processes all curriculum markdown files
- Takes ~30 seconds

### 3. Test RAG System
```bash
python test_rag.py
```

### 4. Run the App
```bash
streamlit run app.py
```

---

## Why Isn't the Vector DB in Git?

**Database is Local** (`data/vector_db/`)
- Large binary files (~MBs)
- Can cause merge conflicts
- Easily regenerated from source

**Source Files are in Git** (`data/knowledge_base/`)
- Small text files
- Easy to version control
- The "source of truth"

**Think of it like:**
- Source code (.md files) → In Git ✅
- Compiled binaries (ChromaDB) → Generated locally 🏠

---

## Common Issues

### "No module named 'chromadb'"
```bash
pip install -r requirements.txt
```

### "Collection is empty"
```bash
python populate_knowledge_base.py
```

### "API key not found"
Create a `.env` file with:
```
GOOGLE_API_KEY=your_key_here
```

---

## File Structure

```
faux-repo/
├── data/
│   ├── knowledge_base/     ← IN GIT (source files)
│   │   ├── ml_curricula/
│   │   ├── web_dev_curricula/
│   │   └── templates/
│   └── vector_db/          ← LOCAL ONLY (generated)
│       ├── chroma.sqlite3
│       └── ...
├── populate_knowledge_base.py
├── setup.py                ← Run this first!
└── app.py
```

---

## Need Help?

- Check [README.md](README.md) for full documentation
- Check [ERROR_RESOLUTION.md](ERROR_RESOLUTION.md) for common errors
- Ask the team! 💬
