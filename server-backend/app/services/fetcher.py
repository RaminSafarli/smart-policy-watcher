# app/services/fetcher.py
from __future__ import annotations
import datetime, hashlib
import httpx
from pydantic import AnyHttpUrl

UA = "SmartPolicyWatcher/1.0 (+research contact)"
MAX_BYTES = 2_000_000  # 2 MB cap

async def fetch_live_html(url: AnyHttpUrl) -> dict:
    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=httpx.Timeout(10.0, read=20.0),
        headers={"User-Agent": UA, "Accept": "text/html,*/*"}
    ) as client:
        r = await client.get(str(url))

    ct = (r.headers.get("content-type") or "").split(";")[0].strip().lower()
    if not ct.startswith("text/html"):
        raise ValueError(f"Non-HTML content-type: {ct or 'unknown'}")

    content = r.content[:MAX_BYTES]
    return {
        "requested_url": str(url),
        "final_url": str(r.url),
        "status_code": r.status_code,
        "content_type": ct,
        "fetched_at": datetime.datetime.utcnow().isoformat() + "Z",
        "html": content.decode(r.encoding or "utf-8", errors="replace"),
        "html_sha256": hashlib.sha256(content).hexdigest(),
        "truncated": len(r.content) > MAX_BYTES,
    }
