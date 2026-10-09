
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load the CSV file from the same folder as main.py
csv_file = Path(__file__).parent / "q-fastapi.csv"
df = pd.read_csv(csv_file)

# Return all students or filter by one or more classes
@app.get("/api")
def get_students(
    classes: list[str] | None = Query(default=None, alias="class")
):
    data = df

    if classes:
        data = df[df["class"].isin(classes)]

    return {"students": data.to_dict(orient="records")}
