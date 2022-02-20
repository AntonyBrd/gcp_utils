import uvicorn
import os
import time
from typing import Any, Callable

from fastapi import FastAPI, Request

app = FastAPI(
    title="Fast CR",
    description="Fast API Running on Cloud Run.",
    version="0.0.1",
    docs_url='/docs')


@app.get("/")
async def root():
    return {"message": "Hello World !!!"}

@app.get("/weather")
async def root():
    return {"message": "Here is the default weather: Sunny !"}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable) -> Any:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("pocrapi.main:app", host="0.0.0.0", port=8000, reload=True)
