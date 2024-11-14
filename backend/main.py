from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Score(BaseModel):
    username: str
    score: int

leaderboard = []

@app.post("/submit_score")
def submit_score(score: Score):
    global leaderboard
    leaderboard.append({"username": score.username, "score": score.score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    return {"message": "Score submitted"}

@app.get("/get_leaderboard")
def get_leaderboard():
    return leaderboard