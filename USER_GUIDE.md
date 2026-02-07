# 📚 Complete User Guide - RAG-Powered Curriculum Generator

## Table of Contents
1. [Understanding the System](#understanding-the-system)
2. [How RAG Works Here](#how-rag-works-here)
3. [Adding Documents to Knowledge Base](#adding-documents-to-knowledge-base)
4. [Using the System](#using-the-system)
5. [Improving & Customizing](#improving--customizing)
6. [Troubleshooting](#troubleshooting)

---

## Understanding the System

### What This Does
This application generates complete educational curricula (course plans) using:
- **RAG (Retrieval-Augmented Generation)**: Finds similar curriculum examples from your knowledge base
- **Vector Database (ChromaDB)**: Stores and searches curriculum examples using semantic similarity
- **LLM (Google Gemini)**: Generates new curricula based on retrieved examples and your input

### Architecture Flow
```
User Input → Vector Search (ChromaDB) → Retrieve Similar Examples → 
→ LLM Prompt with Context → Gemini Generates Curriculum → 
→ Validation → PDF Output
```

### Key Components
- **`data/knowledge_base/`** - Your curriculum examples (Markdown files)
- **`data/vector_db/`** - ChromaDB vector database (auto-generated)
- **`src/rag/`** - RAG pipeline (embeddings, retrieval, vector store)
- **`src/llm/`** - Gemini API client and prompts
- **`src/curriculum/`** - Curriculum models, generator, validator
- **`app.py`** - Streamlit web interface

---

## How RAG Works Here

### Step-by-Step Process

#### 1. **Document Ingestion** (One-time setup)
```bash
python populate_knowledge_base.py
```
What happens:
- Reads all `.md` files from `data/knowledge_base/`
- Converts text into vector embeddings (numerical representations)
- Stores in ChromaDB with metadata (subject, level, category)

#### 2. **Query Time** (When you generate a curriculum)
```
User: "Create a BTech Machine Learning curriculum"
↓
1. Vector Search: Finds similar curricula by semantic meaning
   - Searches: "BTech" + "Machine Learning" + "AI" related docs
   - Returns: Top 3 most similar examples
↓
2. Context Building: Formats examples for LLM
   - Example 1: Masters ML curriculum
   - Example 2: BTech AI curriculum  
   - Example 3: Generic template
↓
3. LLM Generation: Gemini creates new curriculum
   - Uses examples as reference
   - Follows the same structure
   - Customizes for your specific request
↓
4. Output: Structured curriculum with semesters, courses, outcomes
```

### Why RAG is Better Than Plain LLM
- ✅ **Consistency**: Follows your organization's format
- ✅ **Domain-specific**: Uses your actual curriculum examples
- ✅ **Accuracy**: Grounds generation in real data
- ✅ **Customizable**: Add your own curriculum templates

---

## Adding Documents to Knowledge Base

### Current Knowledge Base Structure
```
data/knowledge_base/
├── cse_courses/
│   └── cse_core_curriculum.md       # CSE Core Curriculum
├── ce_courses/
│   └── ce_ar22_curriculum.md        # Civil Engineering AR22
├── ece_courses/
│   └── ece_ar22_curriculum.md       # Electronics & Comm AR22
├── me_courses/
│   └── me_ar22_curriculum.md        # Mechanical Engineering AR22
├── aiml_courses/                    # (Add AIML courses here)
├── ml_curricula/
│   ├── btech_ai.md                  # BTech AI (8 semesters)
│   └── masters_ml.md                # Masters ML (4 semesters)
├── web_dev_curricula/
│   └── fullstack_bootcamp.md        # Full-Stack Bootcamp
└── templates/
    └── curriculum_template.md       # Generic template
```

**You can create ANY folder structure** - the populate script scans recursively!

### How to Add New Curriculum Documents

#### Option 1: Add New Markdown Files (Recommended)

**Step 1:** Create a new `.md` file in any folder (or create a new folder!)
```bash
# Create a new department folder
mkdir data/knowledge_base/biotech_courses

# Or use existing folders like:
data/knowledge_base/ml_curricula/your_curriculum.md

# For Web Development
data/knowledge_base/web_dev_curricula/your_curriculum.md

# For other subjects - create new folder
data/knowledge_base/data_science_curricula/your_curriculum.md
```

**Step 2:** Write curriculum in this format
```markdown
# Program Title

**Level:** BTech/Masters/Diploma/Certification
**Duration:** X semesters/months
**Total Credits:** XX

## Overview
Brief description of the program...

## Semester 1
### Course 1: Course Name (Code: XXX101)
- Credits: 3
- Description: ...
- Prerequisites: None

### Course 2: Another Course (Code: XXX102)
- Credits: 4
- Description: ...

## Learning Outcomes
1. Outcome 1
2. Outcome 2
...

## Career Paths
- Path 1
- Path 2
```

**Step 3:** Re-populate the vector database
```bash
python populate_knowledge_base.py
```

This will:
- Scan all markdown files
- Extract metadata (level, subject, category)
- Generate embeddings
- Update ChromaDB

#### Option 2: Programmatically Add Documents

Edit `populate_knowledge_base.py`:

```python
# Add this at the end of load_curriculum_documents() function

# Custom curriculum
custom_curricula = [
    {
        "content": """Your full curriculum text here...""",
        "metadata": {
            "source": "custom_input",
            "level": "BTech",
            "subject": "Blockchain",
            "category": "technology"
        },
        "id": "custom_blockchain_btech"
    }
]

for curriculum in custom_curricula:
    documents.append(curriculum["content"])
    metadatas.append(curriculum["metadata"])
    ids.append(curriculum["id"])
```

Then run:
```bash
python populate_knowledge_base.py
```

### Best Practices for Knowledge Base

1. **Quality over Quantity**: 5-10 high-quality examples > 100 poor ones
2. **Consistent Format**: Keep similar structure across documents
3. **Rich Metadata**: Add detailed metadata for better retrieval
4. **Domain Grouping**: Organize by subject area (ML, Web Dev, etc.)
5. **Update Regularly**: Re-run `populate_knowledge_base.py` after adding files

---

## Using the System

### Quick Start

#### 1. **Setup (One-time)**
```bash
# Install dependencies
pip install -r requirements.txt

# Add your API key to .env
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Populate knowledge base
python populate_knowledge_base.py

# Verify API quota (optional)
python check_quota.py
```

#### 2. **Run the Application**
```bash
streamlit run app.py
```

Opens at: `http://localhost:8501`

#### 3. **Generate a Curriculum**

**In the Web Interface:**
1. **Subject/Skill Area**: Enter topic (e.g., "Data Science", "Cybersecurity")
2. **Education Level**: Select BTech/Masters/Diploma/Certification
3. **Duration**: Number of semesters (1-12)
4. **Specialization** (Optional): e.g., "Deep Learning"
5. **Focus Areas** (Optional): e.g., "TensorFlow, PyTorch, Computer Vision"
6. Click **"🚀 Generate Curriculum"**
7. Wait 30-60 seconds
8. Review generated curriculum
9. Download PDF

### Command-Line Testing

#### Check API Quota
```bash
python check_quota.py
```
Checks if your API key works and has available quota.

#### Test with Custom Input
```python
from src.curriculum.generator import CurriculumGenerator
from src.curriculum.models import CurriculumRequest
from src.rag.vector_store import CurriculumVectorStore
from src.llm.client import GeminiClient

# Initialize
vs = CurriculumVectorStore()
llm = GeminiClient()
generator = CurriculumGenerator(vs, llm)

# Create request
request = CurriculumRequest(
    skill="Your Subject Here",
    level="BTech",
    duration_semesters=8,
    specialization="Your Specialization",
    focus_areas=["Topic 1", "Topic 2"]
)

# Generate
curriculum = generator.generate(request)
print(curriculum.title)
```

---

## Improving & Customizing

### 1. Improve Generation Quality

#### Add More Examples
More diverse examples = better generation
```bash
# Add 3-5 curricula per subject area you care about
data/knowledge_base/
├── cybersecurity/
│   ├── btech_cyber.md
│   ├── certification_cyber.md
│   └── masters_cyber.md
```

#### Tune the Prompts
Edit `src/llm/prompts.py`:
```python
def get_curriculum_generation_prompt(...):
    # Modify instructions to LLM
    # Add more specific requirements
    # Change output format
```

#### Adjust RAG Parameters
Edit `src/rag/retriever.py`:
```python
# Change number of examples retrieved
def retrieve_similar_curricula(self, skill, level, k=3):  # Change k
    ...

# Add metadata filtering
results = self.vector_store.similarity_search(
    query=query,
    k=k,
    filter_metadata={"level": level}  # Only match same level
)
```

### 2. Change the Model

#### Use More Powerful Model
Edit `src/llm/client.py` line 14:
```python
def __init__(self, model_name: str = "models/gemini-2.5-pro"):  # More capable
```

Trade-offs:
- `gemini-2.5-flash` ⚡ - Fast, efficient, good quality
- `gemini-2.5-pro` 🧠 - Slower, more capable, best quality

#### Adjust Generation Parameters
```python
# In src/llm/client.py, generate() method
response = self.client.models.generate_content(
    model=self.model_name,
    contents=prompt,
    config={
        "temperature": 0.7,  # 0.0 = deterministic, 1.0 = creative
        "max_output_tokens": 8192,  # Increase for longer output
        "top_p": 0.95,  # Nucleus sampling
        "top_k": 40     # Top-k sampling
    }
)
```

### 3. Customize Output Format

#### Modify Pydantic Models
Edit `src/curriculum/models.py`:
```python
class Curriculum(BaseModel):
    title: str
    level: str
    # Add new fields
    accreditation_body: Optional[str] = None
    industry_partners: Optional[List[str]] = None
    internship_requirements: Optional[str] = None
```

#### Adjust PDF Generation
Edit `src/pdf/generator.py` to change PDF layout, styling, sections.

### 4. Add Validation Rules

Edit `src/curriculum/validator.py`:
```python
def validate_curriculum(self, curriculum: Curriculum) -> Dict:
    # Add custom validation rules
    if curriculum.total_credits < 120:  # Example: minimum credits
        issues.append("Total credits below minimum requirement")
```

### 5. Extend Web Interface

Edit `app.py`:
```python
# Add new input fields
subject_area = st.selectbox(
    "Subject Area",
    ["Engineering", "Business", "Arts", "Science"]
)

# Add new tabs
tab1, tab2, tab3, tab4 = st.tabs([...])

# Add visualizations
st.plotly_chart(create_credit_distribution_chart(curriculum))
```

---

## Troubleshooting

### Common Issues

#### "RESOURCE_EXHAUSTED" / 429 Error
**Problem:** Hit API rate limit  
**Solution:**
```bash
# Check quota
python check_quota.py

# Wait 1 minute (rate limit reset)
# Or wait until tomorrow (daily limit reset)
# Or create new API key at https://aistudio.google.com/apikey
```

#### "Knowledge base is empty"
**Problem:** Vector database not populated  
**Solution:**
```bash
python populate_knowledge_base.py
```

#### Poor Quality Output
**Solutions:**
1. Add more relevant examples to knowledge base
2. Use `models/gemini-2.5-pro` instead of `flash`
3. Provide more detailed specialization/focus areas
4. Tune temperature parameter (lower = more conservative)

#### Import Errors
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # macOS/Linux
```

#### Vector DB Corruption
**Solution:**
```bash
# Delete and recreate
Remove-Item -Recurse -Force data/vector_db
python populate_knowledge_base.py
```

---

## Advanced: Understanding the Code

### Key Files Explained

#### `populate_knowledge_base.py`
- Loads markdown files from `data/knowledge_base/`
- Extracts metadata (level, subject, category)
- Adds to ChromaDB with automatic embedding generation

#### `src/rag/vector_store.py`
- Wraps ChromaDB for persistent storage
- Auto-generates embeddings using sentence transformers
- Provides similarity search interface

#### `src/rag/retriever.py`
- Builds search queries from user input
- Retrieves similar curricula
- Formats context for LLM prompt

#### `src/llm/client.py`
- Google Gemini API wrapper
- Handles retries and error handling
- Configures generation parameters

#### `src/llm/prompts.py`
- Prompt engineering for curriculum generation
- Injects RAG context
- Specifies output format (JSON)

#### `src/curriculum/generator.py`
- Orchestrates RAG + LLM pipeline
- Parses JSON response into Pydantic models
- Error handling and validation

#### `src/curriculum/models.py`
- Pydantic models for type safety
- Defines curriculum structure
- Automatic validation

---

## Performance & Scaling

### Current Limits (Free Tier)
- **API Calls:** 15/minute, 1500/day
- **Vector DB:** Unlimited local storage
- **Examples:** Recommend 20-50 curriculum documents
- **Concurrent Users:** 1 (local Streamlit)

### For Production Use
1. **API Upgrade:** Get paid Gemini API for higher limits
2. **Deploy Streamlit:** Use Streamlit Cloud or AWS/Azure
3. **Add Caching:** Cache common curriculum requests
4. **Database:** Move ChromaDB to persistent cloud storage
5. **Authentication:** Add user authentication
6. **Rate Limiting:** Implement per-user rate limits

---

## Summary Checklist

**To Use This System:**
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Add API key to `.env` file
- [ ] Populate knowledge base: `python populate_knowledge_base.py`
- [ ] Verify setup: `python preflight_check.py`
- [ ] Run app: `streamlit run app.py`

**To Improve Quality:**
- [ ] Add 5-10 high-quality curriculum examples per subject
- [ ] Use consistent markdown format
- [ ] Check quota: `python check_quotar quality
- [ ] Tune prompts in `src/llm/prompts.py`
- [ ] Adjust RAG retrieval parameters

**To Customize:**
- [ ] Modify Pydantic models for new fields
- [ ] Update PDF generator for custom styling
- [ ] Add validation rules
- [ ] Extend Streamlit interface

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `streamlit run app.py` | Start web application |
| `python populate_knowledge_base.py` | Update vector database |
| `python check_quota.py` | Check API quota |

| File Path | What It Does |
|-----------|--------------|
| `data/knowledge_base/*.md` | Your curriculum examples |
| `src/llm/prompts.py` | LLM prompt templates |
| `src/rag/retriever.py` | RAG search logic |
| `src/curriculum/models.py` | Data structure definitions |
| `.env` | API key configuration |

---

**Need Help?** Check:
1. Error messages in terminal
2. `python preflight_check.py` output
3. This guide's Troubleshooting section
4. Test witcheck_quota.py` for API issues
3. This guide's Troubleshooting section
4. [ERROR_RESOLUTION.md](ERROR_RESOLUTION.md) for common error