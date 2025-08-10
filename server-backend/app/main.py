from typing import Union

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routes import analyze_change, fetch_wayback, fetch_and_preprocess
from app.pipeline.preprocessor import preprocess_policy_html

import requests

app = FastAPI()
app.include_router(analyze_change.router)
app.include_router(fetch_wayback.router)
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

@app.get("/fb-fetch")
def fb_fetch():
    response = requests.get("https://www.facebook.com/privacy/policy", headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return response.text
