from fastapi import FastAPI
import uvicorn

from schemas import QuestionRequest
from ingestion.storage import load_chunks
from run_search import answer_question

app = FastAPI(title="Student Assistant")

@app.get("/health")
def health_check():
    return {"state":"ok"}

@app.post("/questions")
def submit_question(request:QuestionRequest):
    embedded_chunks = load_chunks("data/processed/embedded_chunks.json")
    answer = answer_question(request.question, embedded_chunks)
    return {"answer" : answer}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)