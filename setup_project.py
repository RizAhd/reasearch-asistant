import os

# Define folder structure
folders = [
    "backend/app/routes",
    "backend/app/services",
    "backend/app/schemas",
    "backend/app/utils",
    "frontend",
    "notebooks",
    "tests",
    "docs",
    "scripts",
    "data/raw",
    "data/processed"
]

# Define files to create
files = [
    # Backend files
    "backend/app/main.py",
    "backend/app/config.py",
    "backend/app/__init__.py",
    "backend/app/routes/__init__.py",
    "backend/app/routes/summarize.py",
    "backend/app/routes/research.py",
    "backend/app/services/__init__.py",
    "backend/app/services/youtube.py",
    "backend/app/services/ai_service.py",
    "backend/app/services/wikipedia_service.py",
    "backend/app/services/arxiv_service.py",
    "backend/app/services/news_service.py",
    "backend/app/schemas/__init__.py",
    "backend/app/schemas/request.py",
    "backend/app/schemas/response.py",
    "backend/app/utils/__init__.py",
    "backend/app/utils/helpers.py",
    "backend/app/utils/validators.py",
    "backend/requirements.txt",
    "backend/.env",
    "backend/.gitignore",
    
    # Frontend files (for later)
    "frontend/index.html",
    "frontend/style.css",
    "frontend/script.js",
    
    # Jupyter Notebooks for validation
    "notebooks/01_api_validation.ipynb",
    "notebooks/02_openai_test.ipynb",
    "notebooks/03_integration_test.ipynb",
    
    # Tests
    "tests/test_openai.py",
    "tests/test_apis.py",
    "tests/test_integration.py",
    "tests/__init__.py",
    
    # Documentation
    "docs/api_docs.md",
    "docs/setup_guide.md",
    
    # Scripts
    "scripts/setup.sh",
    "scripts/run_dev.sh",
    
    # Root files
    "README.md",
    "main.py",  # Quick entry point
    "setup.py"
]

# Create all folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"📁 Created folder: {folder}")

# Create all files
for file in files:
    with open(file, 'a') as f:
        pass  # Just create empty file
    print(f"📄 Created file: {file}")

print("\n" + "="*50)
print("✅ Project structure created successfully!")
print("="*50)
print(f"\n📦 Total folders created: {len(folders)}")
print(f"📦 Total files created: {len(files)}")
print(f"\n📍 Project root: {os.getcwd()}")