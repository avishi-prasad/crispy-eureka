from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Optional

# Load CSV data
df = pd.read_json("q-vercel-python.json")

# Clean the 'name' column by stripping whitespace
df["name"] = df["name"].str.strip()

# Initialize FastAPI app
app = FastAPI()

# Enable CORS to allow all origins and methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],
)

@app.get("/api")
def get_marks(name: Optional[List[str]] = Query(None)):  # Allow multiple names
    if not name:
        return {"marks": []}  # Return empty marks if no name is provided

    # Clean query parameters by stripping spaces
    name = [n.strip() for n in name]

    # Filter marks based on the provided names
    marks = df[df["name"].isin(name)]["marks"].tolist()

    return {"marks": marks}
