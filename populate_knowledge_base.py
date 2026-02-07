"""
Populate ChromaDB vector store with curriculum examples.
Run this once to initialize the knowledge base.

Automatically scans ALL folders under data/knowledge_base/
Just create folders and drop your .md files - it works automatically!
"""
import os
import glob
import re
from pathlib import Path
from src.rag.vector_store import CurriculumVectorStore


def extract_metadata_from_content(content, filepath):
    """
    Extract metadata from markdown content.
    Looks for common patterns in the first 20 lines.
    """
    lines = content.split('\n')[:20]
    metadata = {}
    
    # Try to find level (BTech, MTech, Masters, Certification, etc.)
    for line in lines:
        if 'level:' in line.lower() or 'degree:' in line.lower():
            level_match = re.search(r'[:\*]+\s*(.+)', line, re.IGNORECASE)
            if level_match:
                metadata['level'] = level_match.group(1).strip()
                break
    
    # Try to find subject/program name from title or header
    for line in lines:
        if line.startswith('#') and not line.startswith('##'):
            # First H1 heading is usually the title
            title = line.lstrip('#').strip()
            metadata['title'] = title
            break
    
    # Try to find duration
    for line in lines:
        if 'duration:' in line.lower() or 'years:' in line.lower():
            duration_match = re.search(r'[:\*]+\s*(.+)', line, re.IGNORECASE)
            if duration_match:
                metadata['duration'] = duration_match.group(1).strip()
                break
    
    return metadata


def load_curriculum_documents():
    """
    Load ALL curriculum documents from knowledge base.
    Automatically scans any folder structure under data/knowledge_base/
    """
    documents = []
    metadatas = []
    ids = []
    
    knowledge_base_path = "data/knowledge_base"
    
    # Find all .md files recursively
    all_md_files = glob.glob(f"{knowledge_base_path}/**/*.md", recursive=True)
    
    if not all_md_files:
        print(f"⚠️  No .md files found in {knowledge_base_path}")
        print("   Create folders and add .md files to get started!")
        return documents, metadatas, ids
    
    print(f"\n📁 Scanning {knowledge_base_path}...")
    print(f"   Found {len(all_md_files)} markdown files\n")
    
    # Group files by folder for better display
    files_by_folder = {}
    for filepath in all_md_files:
        folder = os.path.dirname(filepath)
        if folder not in files_by_folder:
            files_by_folder[folder] = []
        files_by_folder[folder].append(filepath)
    
    # Process each file
    for folder, files in sorted(files_by_folder.items()):
        # Extract category from folder name (last part of path)
        folder_name = os.path.basename(folder)
        category = folder_name.replace('_', ' ').title()
        
        print(f"📂 {folder_name}/ ({len(files)} files)")
        
        for filepath in sorted(files):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content.strip():
                    print(f"   ⚠️  Skipped (empty): {os.path.basename(filepath)}")
                    continue
                
                # Extract metadata from content
                content_metadata = extract_metadata_from_content(content, filepath)
                
                # Build metadata dictionary
                filename = os.path.basename(filepath)
                file_id = filename.replace('.md', '').replace(' ', '_')
                
                metadata = {
                    'source': filepath,
                    'category': category,
                    'folder': folder_name,
                    'filename': filename,
                    **content_metadata  # Merge extracted metadata
                }
                
                # Add to collections
                documents.append(content)
                metadatas.append(metadata)
                ids.append(f"{folder_name}_{file_id}")
                
                print(f"   ✅ {filename}")
                
            except Exception as e:
                print(f"   ❌ Error reading {filepath}: {e}")
    
    print(f"\n{'='*60}")
    print(f"📊 Summary: Loaded {len(documents)} documents successfully")
    print(f"{'='*60}")
    
    return documents, metadatas, ids


def main():
    """Initialize vector store with curriculum examples."""
    print("Initializing Curriculum Knowledge Base...")
    print("=" * 60)
    
    # Initialize vector store
    vector_store = CurriculumVectorStore()
    
    # Clear existing data (optional - comment out to keep existing data)
    if vector_store.get_count() > 0:
        print(f"\nFound {vector_store.get_count()} existing documents")
        response = input("Clear existing data? (y/n): ")
        if response.lower() == 'y':
            vector_store.clear()
            print("Cleared existing data")
    
    # Load documents
    print("\nLoading curriculum documents...")
    documents, metadatas, ids = load_curriculum_documents()
    print(f"Loaded {len(documents)} documents")
    
    # Add to vector store
    print("\nAdding documents to vector store...")
    vector_store.add_documents(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print("\n" + "=" * 60)
    print("Knowledge base initialized successfully!")
    print(f"   Total documents: {vector_store.get_count()}")
    print(f"   Storage location: {vector_store.persist_directory}")
    print("\nYou can now run the Streamlit app: streamlit run app.py")


if __name__ == "__main__":
    main()
