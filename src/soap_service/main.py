from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pydantic import BaseModel
from typing import List, Optional
import json
from src.database.queries import (
    get_teams,
    get_players_by_position,
    get_players_by_team,
    get_position_stats,
    get_team_points
)

app = FastAPI(title="NFL Stats Service")

# Enable CORS with specific configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Get the absolute path to the web_ui directory
web_ui_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web_ui")

# Mount the static files directory
app.mount("/static", StaticFiles(directory=web_ui_dir), name="static")

@app.get("/")
async def root():
    """Serve the main index.html file"""
    return FileResponse(os.path.join(web_ui_dir, "index.html"))

@app.get("/api/teams")
async def list_teams():
    """List all teams"""
    try:
        teams = get_teams()
        return teams
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/players/{position}")
async def get_players(position: str):
    """Get players by position (QB, RB, WR, TE, K, DB, DL, LB)"""
    try:
        position = position.upper()
        if position not in ["QB", "RB", "WR", "TE", "K", "DB", "DL", "LB"]:
            raise HTTPException(status_code=400, detail=f"Invalid position: {position}")
            
        players = get_players_by_position(position)
        # Ensure each player has their position and team set
        for player in players:
            player['position'] = position
            if 'team' not in player or not player['team']:
                player['team'] = 'Unknown'
            if 'playername' not in player or not player['playername']:
                continue  # Skip players without names
        return [p for p in players if 'playername' in p and p['playername']]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/players/team/{team}")
async def get_team_players(team: str):
    """Get all players for a specific team"""
    try:
        players = get_players_by_team(team.upper())
        return players
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats/{position}")
async def get_stats(position: str):
    """Get detailed statistics for a position"""
    try:
        position = position.upper()
        if position not in ["QB", "RB", "WR", "TE", "DB", "DL", "LB", "K"]:
            raise HTTPException(status_code=400, detail=f"Invalid position: {position}")
            
        stats = get_position_stats(position)
        # Ensure all stats have numeric values
        for stat in stats:
            for key in stat:
                if key != 'playerid' and key != 'playername' and key != 'team' and key != 'position':
                    stat[key] = float(stat[key] if stat[key] is not None else 0)
            stat['position'] = position
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/team/points/{team}")
async def get_points(team: str):
    """Get total points for a team"""
    try:
        points = get_team_points(team.upper())
        return {"team": team, "points": points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 