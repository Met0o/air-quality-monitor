from fastapi import FastAPI, Request
from datetime import datetime, timedelta
from typing import List, Dict
from collections import deque
import threading

app = FastAPI()
lock = threading.Lock()

BUFFER: Dict[str, deque] = {}

RETENTION_SECONDS = 24 * 3600

@app.post("/ingest/{measurement}")
async def ingest(measurement: str, payload: Dict):
    now = datetime.now()
    data_point = {"timestamp": now.isoformat(), **payload}
    with lock:
        q = BUFFER.setdefault(measurement, deque())
        q.append(data_point)
        while q and (now - datetime.fromisoformat(q[0]['timestamp'])).total_seconds() > RETENTION_SECONDS:
            q.popleft()
    return {"status": "ok"}

@app.get("/query/{measurement}")
async def query(measurement: str):
    with lock:
        return list(BUFFER.get(measurement, []))

@app.get("/")
async def index():
    return {"endpoints": ["/ingest/{measurement}", "/query/{measurement}"]}
