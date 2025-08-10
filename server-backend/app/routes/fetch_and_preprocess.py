# app/routers/fetch_and_preprocess.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import FetchAndPreprocessReq, FetchAndPreprocessRes
import httpx

from app.services.fetcher import fetch_live_html
from app.pipeline.preprocessor import preprocess_policy_html_string

router = APIRouter()

@router.post("/fetch_and_preprocess", response_model=FetchAndPreprocessRes)
async def fetch_and_preprocess(req: FetchAndPreprocessReq):
    try:
        meta = await fetch_live_html(req.url)
        sents = preprocess_policy_html_string(meta["html"])
        return FetchAndPreprocessRes(
            requested_url=req.url,
            final_url=meta["final_url"],
            fetched_at=meta["fetched_at"],
            content_type=meta["content_type"],
            html_sha256=meta["html_sha256"],
            sentence_count=len(sents),
            sentences=sents,
            source="live",
            truncated=meta["truncated"],
        )
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Fetch timed out")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error")
