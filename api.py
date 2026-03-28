from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import io
from analyzer import analyze_sentiment, analyze_multiple

app = FastAPI(
    title="Sentiment Analysis API",
    description="""
## 🧠 Sentiment Analysis REST API
Built with FastAPI + VADER + BERT

### Endpoints
- **GET /health** → API status
- **GET /engines** → Available engines
- **POST /analyze** → Single text
- **POST /analyze-bulk** → Multiple texts
- **POST /analyze-csv** → CSV upload

**Developer:** Arup Das — Brainware University
    """,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Models
class SingleRequest(BaseModel):
    text: str
    engine: Optional[str] = "VADER"

    class Config:
        json_schema_extra = {
            "example": {
                "text": "I love Python programming!",
                "engine": "VADER"
            }
        }

class BulkRequest(BaseModel):
    texts: List[str]
    engine: Optional[str] = "VADER"

    class Config:
        json_schema_extra = {
            "example": {
                "texts": ["I love this!", "This is terrible.", "It was okay."],
                "engine": "VADER"
            }
        }

# ── Health Check
@app.get("/health", tags=["Status"])
def health():
    return {
        "status": "✅ Running",
        "version": "1.0.0",
        "engines": ["VADER", "TextBlob", "BERT"],
        "developer": "Arup Das — Brainware University"
    }

# ── Engines Info
@app.get("/engines", tags=["Info"])
def engines():
    return {
        "engines": [
            {"name": "VADER", "speed": "Fast ⚡", "accuracy": "85%", "best_for": "Social media"},
            {"name": "TextBlob", "speed": "Very Fast ⚡⚡", "accuracy": "70%", "best_for": "Simple text"},
            {"name": "BERT", "speed": "Slow 🐢", "accuracy": "92%", "best_for": "High accuracy"}
        ]
    }

# ── Single Text
@app.post("/analyze", tags=["Analysis"])
def analyze_single(req: SingleRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    if req.engine not in ["VADER", "TextBlob", "BERT"]:
        raise HTTPException(status_code=400, detail="Invalid engine")

    result = analyze_sentiment(req.text, req.engine)
    result["text"] = req.text
    return result

# ── Bulk Text
@app.post("/analyze-bulk", tags=["Analysis"])
def analyze_bulk(req: BulkRequest):
    if not req.texts:
        raise HTTPException(status_code=400, detail="Texts list is empty")
    if len(req.texts) > 100:
        raise HTTPException(status_code=400, detail="Max 100 texts allowed")

    results = analyze_multiple(req.texts, req.engine)
    positive = sum(1 for r in results if r["label"] == "Positive")
    negative = sum(1 for r in results if r["label"] == "Negative")
    neutral  = sum(1 for r in results if r["label"] == "Neutral")

    return {
        "total": len(results),
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "results": results
    }

# ── CSV Upload
@app.post("/analyze-csv", tags=["Analysis"])
async def analyze_csv(file: UploadFile = File(...), engine: str = "VADER"):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode("utf-8")))

    if "text" not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must have 'text' column")

    texts = df["text"].dropna().tolist()[:200]
    results = analyze_multiple(texts, engine)
    positive = sum(1 for r in results if r["label"] == "Positive")
    negative = sum(1 for r in results if r["label"] == "Negative")
    neutral  = sum(1 for r in results if r["label"] == "Neutral")

    return {
        "filename": file.filename,
        "total": len(results),
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "results": results
    }