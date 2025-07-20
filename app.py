from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import re
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your dataset
with open("sales_data.json", "r") as f:
    sales_data = json.load(f)

@app.get("/query")
async def query(request: Request, q: str):
    result = process_question(q)
    response = JSONResponse(content={"answer": result})
    response.headers["X-Email"] = "24f2004922@ds.study.iitm.ac.in"
    return response

def process_question(q: str):
    q = q.lower()

    # total sales of X in Y
    match = re.match(r"what is the total sales of (\w+) in ([\w\s]+)", q)
    if match:
        product, city = match.groups()
        total = sum(r["sales"] for r in sales_data if r["product"].lower() == product and r["city"].lower() == city.strip())
        return total

    # how many sales reps are there in Y
    match = re.match(r"how many sales reps are there in ([\w\s]+)", q)
    if match:
        region = match.group(1).strip()
        reps = {r["rep"] for r in sales_data if r["region"].lower() == region}
        return len(reps)

    # average sales for X in Y
    match = re.match(r"what is the average sales for (\w+) in ([\w\s]+)", q)
    if match:
        product, region = match.groups()
        amounts = [r["sales"] for r in sales_data if r["product"].lower() == product and r["region"].lower() == region.strip()]
        return round(sum(amounts) / len(amounts), 2) if amounts else 0

    # highest sale date by rep in city
    match = re.match(r"on what date did (.+) make the highest sale in ([\w\s]+)", q)
    if match:
        rep, city = match.groups()
        records = [r for r in sales_data if r["rep"].lower() == rep.lower().strip() and r["city"].lower() == city.strip()]
        if not records:
            return "No data"
        highest = max(records, key=lambda x: x["sales"])
        return highest["date"]

    return "Question not recognized"
