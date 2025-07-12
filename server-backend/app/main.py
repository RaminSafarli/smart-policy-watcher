from typing import Union

from fastapi import FastAPI, Request

from app.pipeline.preprocessor import preprocess_policy_html

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

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