from typing import Union

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routes import analyze_change, fetch_and_preprocess
from app.pipeline.preprocessor import preprocess_policy_html

app = FastAPI()
app.include_router(analyze_change.router)
app.include_router(fetch_and_preprocess.router)


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

