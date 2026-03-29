from fastapi import FastAPI
from schemas import LocationRequest
from agent import run_agent

app = FastAPI()
@app.get("/")
def home():
    return {"message": "AI Logistics Agent Running"}

@app.post("/ask")
def ask_agent(req: LocationRequest):
    result = run_agent(req.query, req.locations)
    return {"response": result}