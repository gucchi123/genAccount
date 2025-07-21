# MVP — Generative AI Accounting Learning Platform

Minimal working prototype combining a FastAPI backend (LLM pipelines) and a Streamlit frontend.

## Prerequisites
- Python 3.10+
- OpenAI API key

## Quick Start

```bash
# backend
cd backend
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
uvicorn backend.main:app --reload  # serves at http://localhost:8000
```

```bash
# frontend
cd ../frontend
pip install streamlit requests pyyaml
streamlit run app.py
```

## File Structure
```
mvp_genai_accounting/
├── backend/
│   ├── main.py          # FastAPI endpoints
│   ├── chains.py        # LangChain generation logic
│   └── requirements.txt
├── frontend/
│   └── app.py           # Streamlit UI
└── README.md
```

## Next Steps
1. Replace in‑memory search with Pinecone or Qdrant.
2. Add authentication (Supabase, Auth0).
3. Containerize with Docker for production.