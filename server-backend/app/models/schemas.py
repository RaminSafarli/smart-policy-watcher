from pydantic import BaseModel, AnyHttpUrl
from typing import List, Dict

from pydantic import BaseModel

class Summary(BaseModel):
    short_summary: str
    detailed_summary: str

class AnalyzeChangeResponse(BaseModel):
    is_meaningful: bool
    summary: Summary


class AnalyzeChangeRequest(BaseModel):
    old_sentences: List[str]
    new_sentences: List[str]

# class AnalyzeChangeRequest(BaseModel):
#     old_sentences: List[str]
#     new_sentences: List[str]
    
# class AnalyzeChangeResponse(BaseModel):
#     is_meaningful: bool
#     summary: str
    
    
class FetchAndPreprocessReq(BaseModel):
    url: AnyHttpUrl

class FetchAndPreprocessRes(BaseModel):
    requested_url: AnyHttpUrl
    final_url: str
    fetched_at: str
    content_type: str
    html_sha256: str
    sentence_count: int
    sentences: list[str]
    source: str = "live"
    truncated: bool = False
    

class FetchRequest(BaseModel):
    url: str