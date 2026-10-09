
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Existing students API
csv_file = Path(__file__).parent / "q-fastapi.csv"
df = pd.read_csv(csv_file)

@app.get("/api")
def get_students(
    classes: list[str] | None = Query(default=None, alias="class")
):
    data = df
    if classes:
        data = df[df["class"].isin(classes)]
    return {"students": data.to_dict(orient="records")}


# Batch sentiment analysis API
class SentimentRequest(BaseModel):
    sentences: list[str]


analyzer = SentimentIntensityAnalyzer()

def classify_sentiment(sentence: str) -> str:
    score = analyzer.polarity_scores(sentence)["compound"]

    if score >= 0.05:
        return "happy"
    elif score <= -0.05:
        return "sad"
    else:
        return "neutral"


@app.post("/sentiment")
def analyze_sentiments(request: SentimentRequest):
    results = []

    for sentence in request.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": classify_sentiment(sentence)
        })

    return {"results": results}

@app.post("/")
def analyze_sentiments_root(request: SentimentRequest):
    return analyze_sentiments(request)
