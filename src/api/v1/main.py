import uvicorn

from fastapi import FastAPI
from src.api.v1.chat import api_router as chat_router

app = FastAPI(
    title="Dataset Routing API",
    version="1.0.0",
    description="An API to answer user questions with the appropiate dataset"
)

app.include_router(chat_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Dataset Routing API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
