import requests
from app.config import settings
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": settings.API_FOOTBALL_KEY
}

def get_fixtures(league_id: int, season: int, next: int = None, from_date: str = None, to_date: str = None):
    try:
        params = {
            "league": league_id,
            "season": season
        }
        if next:
            params["next"] = next
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = requests.get(
            f"{BASE_URL}/fixtures",
            headers=headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", [])
    except requests.exceptions.Timeout:
        logger.error("Request timed out while fetching fixtures")
        return []
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error while fetching fixtures: {e}")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching fixtures: {e}")
        return []

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