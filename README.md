# 2048 Game with Online Leaderboard

A Python implementation of the classic 2048 game with a leaderboard system. Built using Pygame for the game interface and FastAPI for the backend server.

## Features

- Classic 2048 gameplay with smooth animations
- Leaderboard system
- Multiple game screens: Start screen, Game screen, Win screen, Game Over screen, Submit Score screen, and Leaderboard screen
- Score submission and tracking

## Installation

1. Make sure you have Python 3.12+ and Poetry installed
2. Clone this repository
3. Navigate to the project folder and install dependencies:
```bash
cd 2048-project-py3.12
poetry install
```

## Running the Game

1. Start the API server first (from the backend directory):
```bash
cd backend
poetry run uvicorn main:app
```
2. In a new terminal, launch the game (from the project directory):
```bash
cd 2048-project-py3.12
poetry run python main.py
```
