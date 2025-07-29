from fastapi import APIRouter, HTTPException, Query
from app.pipeline.fetcher import fetch_wayback_snapshot

router = APIRouter()

@router.get("/fetch_wayback_html")
def fetch_wayback_html(url: str = Query(...)):
    try:
        html = fetch_wayback_snapshot(url)
        return {"html": html}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 