from fastapi import FastAPI
import uvicorn

from schemas import QuestionRequest
from retrieval.database_search import load_database_chunks
from run_search import answer_question


app = FastAPI(title="studentAssistant")


@app.get("/health")
def health_check():
    return {"state": "ok"}


@app.post("/questions")
def submit_question(request: QuestionRequest):
    chunks = load_database_chunks()
    answer = answer_question(request.question, chunks)
    return {"answer": answer}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)