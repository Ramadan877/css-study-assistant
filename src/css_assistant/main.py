from fastapi import FastAPI
import uvicorn

from schemas import QuestionRequest

app = FastAPI(title="studentAssistant")

@app.get("/health")
def health_check():
    return {"state":"ok"}

@app.post("/questions")
def submit_question(request:QuestionRequest):
    QuestionRequest = request.question
    return {"received_question":QuestionRequest}

def call_answer():
    pass 

def retrieve_curicullum_passage():
    pass 

def generate_answer():
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)