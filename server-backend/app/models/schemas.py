from pydantic import BaseModel

class AnalyzeChangeRequest(BaseModel):
    old_html: str
    new_html: str
    
class AnalyzeChangeResponse(BaseModel):
    is_meaningful: bool
    summary: str