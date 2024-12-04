from fastapi import FastAPI
import json
from pydantic import BaseModel
import os

app = FastAPI()

LEADERBOARD_FILE = "leaderboard.json"


class ScoreSubmit(BaseModel):
    name: str
    score: int


def load_scores():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


@app.get("/get-best-score/")
def get_best_score():
    scores = load_scores()
    if not scores:
        return {"best_score": 0}
    return {"best_score": scores[0]["score"]}


def save_scores(scores):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(scores, f, indent=2)


@app.get("/get-leaderboard/")
def get_leaderboard(skip: int = 0, limit: int = 10):
    scores = load_scores()
    return scores[skip : skip + limit]


@app.post("/submit-score/")
def submit_score(score: ScoreSubmit):
    scores = load_scores()
    new_score = {"name": score.name, "score": score.score}
    scores.append(new_score)
    scores.sort(key=lambda x: x["score"], reverse=True)
    save_scores(scores)
    return new_score
