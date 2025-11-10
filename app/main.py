# app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import Table, Column, Integer, String, Float, MetaData
from app.db import database

# Step 1: Initialize FastAPI app
app = FastAPI(title="Data Ingestion Microservice")

# Step 2: Enable CORS (so frontend can talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace * with ["http://127.0.0.1:5500"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Step 3: Define database schema
metadata = MetaData()

records_table = Table(
    "records",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("value", Float),
)

# Step 4: Define Pydantic model
class Record(BaseModel):
    id: int = Field(..., description="Unique record ID")
    name: str = Field(..., min_length=1, max_length=50)
    value: float = Field(..., gt=0)

# Step 5: Database connection events
@app.on_event("startup")
async def startup():
    await database.connect()
    await database.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            value REAL NOT NULL
        );
    """)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Step 6: POST endpoint — /ingest
@app.post("/ingest")
async def ingest_data(record: Record):
    existing = await database.fetch_one(
        "SELECT * FROM records WHERE id = :id",
        {"id": record.id},
    )
    if existing:
        raise HTTPException(status_code=400, detail="Duplicate record ID (idempotency check failed)")

    query = "INSERT INTO records (id, name, value) VALUES (:id, :name, :value)"
    await database.execute(query, record.dict())
    return {"message": "✅ Record stored successfully", "record": record}

# Step 7: GET endpoint — /records
@app.get("/records")
async def get_records():
    results = await database.fetch_all("SELECT * FROM records")
    return {"count": len(results), "records": results}

# Step 8: Root
@app.get("/")
def root():
    return {"message": "Welcome to the Data Ingestion Microservice 👋"}
