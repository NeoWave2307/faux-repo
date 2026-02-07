"""
Complete automated setup script for Curriculum RAG System.
Creates virtual environment, installs dependencies, populates database, and runs the app.

Usage: python setup.py
"""
import subprocess
import sys
import os
import platform


def run_command(command, description, check=True, shell=True):
    """Run a command and display progress."""
    print(f"\n{'='*70}")
    print(f"📋 {description}")
    print(f"{'='*70}")
    print(f"▶️  Command: {command}\n")
    
    result = subprocess.run(command, shell=shell)
    if check and result.returncode != 0:
        print(f"\n❌ Error: {description} failed")
        return False
    
    print(f"\n✅ {description} completed")
    return True


def main():
    print("""
╔════════════════════════════════════════════════════════════════════╗
║           🎓 Curriculum RAG System - Automated Setup              ║
╚════════════════════════════════════════════════════════════════════╝

This will:
  1. ✅ Create Python virtual environment (venv)
  2. ✅ Activate virtual environment
  3. ✅ Install all dependencies
  4. ✅ Populate ChromaDB knowledge base
  5. ✅ Launch Streamlit application

""")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    
    # Detect OS
    is_windows = platform.system() == "Windows"
    print(f"✅ Operating System: {platform.system()}")
    
    # Step 1: Create virtual environment
    venv_path = "venv"
    if not os.path.exists(venv_path):
        if not run_command(
            "python -m venv venv",
            "Creating virtual environment",
            check=True
        ):
            sys.exit(1)
    else:
        print(f"\n{'='*70}")
        print("📋 Virtual environment already exists")
        print(f"{'='*70}")
        print("✅ Skipping venv creation")
    
    # Step 2: Determine activation script and python paths
    if is_windows:
        activate_script = os.path.join(venv_path, "Scripts", "activate")
        python_exe = os.path.join(venv_path, "Scripts", "python.exe")
        pip_exe = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")
        python_exe = os.path.join(venv_path, "bin", "python")
        pip_exe = os.path.join(venv_path, "bin", "pip")
    
    print(f"\n{'='*70}")
    print("📋 Virtual environment activated")
    print(f"{'='*70}")
    print(f"✅ Using: {python_exe}")
    
    # Step 3: Upgrade pip
    run_command(
        f'"{python_exe}" -m pip install --upgrade pip',
        "Upgrading pip",
        check=False
    )
    
    # Step 4: Install requirements
    if not run_command(
        f'"{pip_exe}" install -r requirements.txt',
        "Installing Python dependencies",
        check=True
    ):
        sys.exit(1)
    
    # Step 5: Populate knowledge base
    print(f"\n{'='*70}")
    print("📋 Populating ChromaDB vector database")
    print(f"{'='*70}")
    print("⚠️  You'll be asked if you want to clear existing data")
    print("    - Press 'y' to start fresh")
    print("    - Press 'n' to keep existing data\n")
    
    result = subprocess.run(f'"{python_exe}" populate_knowledge_base.py', shell=True)
    if result.returncode != 0:
        print("\n⚠️  Population had issues, but continuing...")
    
    # Step 6: Check for .env file
    print(f"\n{'='*70}")
    print("📋 Checking environment configuration")
    print(f"{'='*70}")
    
    if not os.path.exists(".env"):
        print("⚠️  No .env file found")
        print("\n📝 Create a .env file with your API keys:")
        print("   GOOGLE_API_KEY=your_google_api_key_here")
        print("\n   You can create it now or later before using AI features")
    else:
        print("✅ .env file found")
    
    # Step 7: Final summary
    print(f"\n{'='*70}")
    print("🎉 Setup Complete!")
    print(f"{'='*70}")
    
    # Step 8: Ask if user wants to run the app
    print("\n🚀 Would you like to launch the Streamlit app now? (y/n): ", end="")
    response = input().strip().lower()
    
    if response == 'y':
        print(f"\n{'='*70}")
        print("📋 Launching Streamlit application")
        print(f"{'='*70}")
        print("🌐 App will open in your browser at http://localhost:8501")
        print("⚠️  Press Ctrl+C to stop the server\n")
        
        # Run streamlit
        subprocess.run(f'"{python_exe}" -m streamlit run app.py', shell=True)
    else:
        print(f"\n{'='*70}")
        print("📝 To run the app later, use:")
        print(f"{'='*70}")
        
        if is_windows:
            print("\n   venv\\Scripts\\activate")
            print("   streamlit run app.py")
        else:
            print("\n   source venv/bin/activate")
            print("   streamlit run app.py")
        
        print("\n   OR simply run: python setup.py")
        print("\n🚀 Happy coding!\n")


if __name__ == "__main__":
    main()
