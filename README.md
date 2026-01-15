# 🔍 Universal Research Assistant

A multi-source research assistant powered by AI that gathers and synthesizes information from:
- Wikipedia (general knowledge)
- arXiv (academic papers)
- NewsAPI (current events)
- OpenAI GPT (synthesis & analysis)

## 🚀 Quick Start

```bash
# 1. Setup environment
conda create -n research-assistant python=3.10
conda activate research-assistant

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Configure API keys
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# 4. Run validation
jupyter notebook notebooks/01_api_validation.ipynb

# 5. Start the app
cd backend
uvicorn app.main:app --reload