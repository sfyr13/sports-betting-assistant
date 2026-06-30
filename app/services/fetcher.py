import requests
from app.config import settings

BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": settings.API_FOOTBALL_KEY
}

def get_fixtures(league_id: int, season: int, next: int = 10):
    response = requests.get(
        f"{BASE_URL}/fixtures",
        headers=headers,
        params={
            "league": league_id,
            "season": season,
            "next": next
        }
    )
    data = response.json()
    return data.get("response", [])

def get_team_statistics(league_id: int, season: int, team_id: int):
    response = requests.get(
        f"{BASE_URL}/teams/statistics",
        headers=headers,
        params={
            "league": league_id,
            "season": season,
            "team": team_id
        }
    )
    data = response.json()
    return data.get("response", {})

def get_head_to_head(team1_id: int, team2_id: int, last: int = 5):
    response = requests.get(
        f"{BASE_URL}/fixtures/headtohead",
        headers=headers,
        params={
            "h2h": f"{team1_id}-{team2_id}",
            "last": last
        }
    )
    data = response.json()
    return data.get("response", [])