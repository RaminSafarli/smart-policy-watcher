from fastapi import APIRouter, HTTPException
from app.models.schemas import FetchRequest

from app.pipeline.preprocessor import preprocess_policy_html

router = APIRouter()

@router.post("/fetch_html")
def fetch_html(req: FetchRequest):
    try:
        print(req.url)
        html_sentences = preprocess_policy_html(req.url)
        return html_sentences
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))