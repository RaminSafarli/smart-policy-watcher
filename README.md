# Smart Policy Watcher  

Smart Policy Watcher is a browser extension + backend service that automatically monitors privacy policy pages, detects meaningful changes, and notifies users in simple, understandable language.  

This project was developed as part of an MSc dissertation at the University of Edinburgh.

---

## Features
- **Automated Monitoring** – Periodic checks of privacy policy URLs.  
- **Semantic Change Detection** – Uses Sentence-BERT alignment and LLM-based filtering.  
- **Summarisation** – Generates short and detailed natural language summaries of changes.  
- **Browser Notifications** – Simple UI with popups and badges to alert users.  
- **Local Inference** – Runs with a local Llama 2 model, no cloud API required.  

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/RaminSafarli/smart-policy-watcher.git
cd smart-policy-watcher
```

### 2. Backend (FastAPI)

Create a virtual environment and install dependencies:
```bash
cd server-backend
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run the backend
```bash
uvicorn app.main:app --reload
```

### 3. Frontend (Browser Extension)
```bash
cd client-extension
npm install
npm run build
```
Then load the extension in Chrome:

1. Open chrome://extensions
2. Enable Developer mode
3. Click Load unpacked
4. Select the extension/dist folder


## Model Setup (Required)

The project uses a **local LLaMA 2 model** for change detection and summarisation.  
Since the model is too large to be included in this repository, you must download it manually to **models** folder that should be added to **server-backend**.

### 1. Download the model
You need the file: llama-2-7b-chat.Q5_K_M.gguf


**Recommended source:** [TheBloke on Hugging Face](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_M.gguf)

### 3. Confirm llama.cpp integration

The backend loads this model automatically from the models/ directory.


