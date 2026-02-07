# 📚 Knowledge Base - Curriculum Repository

This folder contains all curriculum and syllabus documents that feed into the RAG system.

## 🚀 Quick Start

**Just create a folder and add .md files - it works automatically!**

```
data/knowledge_base/
├── cse_courses/          ← Your CSE courses here
│   ├── data_structures.md
│   └── algorithms.md
├── aiml_courses/         ← Your AIML courses here
│   ├── machine_learning.md
│   └── deep_learning.md
└── any_folder_name/      ← Any structure you want!
    └── your_file.md
```

Then run:
```bash
python populate_knowledge_base.py
```

The script **automatically**:
- ✅ Scans all folders recursively
- ✅ Finds all .md files
- ✅ Extracts metadata from content
- ✅ Populates ChromaDB

---

## 📁 Suggested Folder Structure

Organize by whatever makes sense for you:

### By Department/Stream
```
knowledge_base/
├── cse_courses/          # Computer Science
├── aiml_courses/         # AI & Machine Learning
├── ece_courses/          # Electronics
├── mech_courses/         # Mechanical
└── civil_courses/        # Civil Engineering
```

### By Level
```
knowledge_base/
├── btech_programs/       # Undergraduate
├── mtech_programs/       # Postgraduate
├── diploma_programs/     # Diploma
└── certification/        # Short courses
```

### By Subject Area
```
knowledge_base/
├── programming/
├── mathematics/
├── data_science/
├── web_development/
└── cybersecurity/
```

**Pick any structure - the script handles it all!**

---

## 📝 File Format

Use markdown (.md) files with this suggested format:

```markdown
# Course Name or Program Title

**Level:** BTech / MTech / Masters / Certification
**Duration:** 4 Years / 2 Years / 6 Months
**Department:** CSE / AIML / ECE
**Credits:** 160

## Overview
Brief description of the course/program...

## Semester 1 (Credits)
- Course Code - Course Name (Credits) - Type
- CS101 - Programming Fundamentals (4) - Core
- MA101 - Calculus (4) - Core

## Semester 2
...
```

**The script auto-extracts:**
- Level (from "Level:" line)
- Title (from # heading)
- Duration (from "Duration:" line)
- Category (from folder name)

---

## 🔄 Workflow

### Adding New Curriculum

1. **Create a folder** (if needed):
   ```bash
   mkdir data/knowledge_base/cse_courses
   ```

2. **Add your .md file**:
   ```
   data/knowledge_base/cse_courses/ds_algo_btech.md
   ```

3. **Repopulate the database**:
   ```bash
   python populate_knowledge_base.py
   ```
   - Choose 'y' to replace all data
   - Choose 'n' to add to existing data

4. **Test it**:
   ```bash
   python test_rag.py
   ```

### Updating Existing Files

1. Edit the .md file
2. Run `python populate_knowledge_base.py`
3. Choose 'y' to refresh the database

---

## 💡 Tips

- **Descriptive filenames**: Use clear names like `btech_cse_4year.md`
- **Rich metadata**: Include Level, Duration, Credits in your files
- **Consistent format**: Similar structures help the AI learn better
- **Examples matter**: More varied examples = better AI responses
- **Organize logically**: Use folders that make sense to you

---

## 📊 Current Structure

```
knowledge_base/
├── cse_courses/              # Computer Science
│   └── cse_core_curriculum.md
├── aiml_courses/             # AI & Machine Learning (add files here)
├── ce_courses/               # Civil Engineering
│   └── ce_ar22_curriculum.md
├── ece_courses/              # Electronics & Communication
│   └── ece_ar22_curriculum.md
├── me_courses/               # Mechanical Engineering
│   └── me_ar22_curriculum.md
├── ml_curricula/             # ML programs
│   ├── btech_ai.md
│   └── masters_ml.md
├── web_dev_curricula/        # Web Development courses
│   └── fullstack_bootcamp.md
├── templates/                # Generic templates
│   └── curriculum_template.md
└── README.md                 # This file
```

**Add your own folders anytime! The populate script handles them automatically.**

---

## ❓ Common Questions

**Q: What if I have deeply nested folders?**  
A: No problem! The script scans recursively.

**Q: Can I use different file formats?**  
A: Currently only .md (markdown) files are supported.

**Q: What if two files have the same name in different folders?**  
A: They get unique IDs: `foldername_filename`

**Q: Do I need to restart the app after adding files?**  
A: No, just re-run `populate_knowledge_base.py`

---

## 🎯 Examples

### Example 1: CSE 4-Year BTech
`cse_courses/btech_cse_core.md`

### Example 2: AIML Specialization
`aiml_courses/aiml_specialization.md`

### Example 3: Short Certificate Course
`certifications/python_bootcamp.md`

All work automatically! 🎉
