from pydantic import BaseModel
from typing import List

class AnalyzeChangeRequest(BaseModel):
    old_sentences: List[str]
    new_sentences: List[str]
    
class AnalyzeChangeResponse(BaseModel):
    is_meaningful: bool
    summary: str
    
class FetchRequest(BaseModel):
    url: str