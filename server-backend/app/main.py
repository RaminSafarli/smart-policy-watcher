from typing import Union

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routes import analyze_change
from app.pipeline.preprocessor import preprocess_policy_html

app = FastAPI()
app.include_router(analyze_change.router)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/preprocess/")
async def preprocess_html(request: Request):
    """
    Preprocess HTML content to extract visible text.
    
    Args:
        html_content (str): The HTML content as a string.
        
    Returns:
        str: The extracted visible text.
    """
    body = await request.json()
    html = body.get("html", "")
    # sentences = extract_text_from_html(html)
    sentences = preprocess_policy_html(html)
    return {"sentences": sentences}