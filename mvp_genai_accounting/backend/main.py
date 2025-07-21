from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .chains import generate_case, search_cases
import logging

app = FastAPI(title="GenAI Accounting PoC API", version="0.1.0")

# ロガー設定（stderr にフル Traceback を出したい場合）
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class GenerateRequest(BaseModel):
    yaml_meta: str

@app.post("/generate")
async def generate_endpoint(req: GenerateRequest):

    """
    YAML メタデータを受け取りケース教材を生成する。
    try/except を外し、例外は FastAPI のデフォルトハンドラに任せる。
    """
    result = generate_case(req.yaml_meta)          # ← ここで失敗すれば Traceback がそのまま出る
    return {"status": "ok", "data": result}

    """
    try:
        result = generate_case(req.yaml_meta)
        return {"status": "ok", "data": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    """


class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search_endpoint(req: SearchRequest):
    try:
        results = search_cases(req.query)
        return {"status": "ok", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))