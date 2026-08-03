import logging
from app.db.vector_store import add_documents

logger = logging.getLogger(__name__)

def format_fixture(fixture: dict) -> str:
    try:
        home_team = fixture["teams"]["home"]["name"]
        away_team = fixture["teams"]["away"]["name"]
        date = fixture["fixture"]["date"]
        league = fixture["league"]["name"]
        venue = fixture["fixture"]["venue"]["name"]
        status = fixture["fixture"]["status"]["short"]
        home_goals = fixture["goals"]["home"]
        away_goals = fixture["goals"]["away"]

        if status == "FT":
            score_text = f"Final Score: {home_team} {home_goals} - {away_goals} {away_team}"
        else:
            score_text = "Match not yet played"

        return (
            f"{home_team} vs {away_team} | "
            f"League: {league} | "
            f"Date: {date} | "
            f"Venue: {venue} | "
            f"{score_text}"
        )
    except KeyError as e:
        logger.error(f"Missing field in fixture data: {e}")
        return ""

def format_team_statistics(stats: dict) -> str:
    try:
        team = stats["team"]["name"]
        played = stats["fixtures"]["played"]["total"]
        wins = stats["fixtures"]["wins"]["total"]
        losses = stats["fixtures"]["loses"]["total"]
        draws = stats["fixtures"]["draws"]["total"]
        goals_for = stats["goals"]["for"]["total"]["total"]
        goals_against = stats["goals"]["against"]["total"]["total"]

        return (
            f"Team: {team} | "
            f"Played: {played} | "
            f"Wins: {wins} | "
            f"Draws: {draws} | "
            f"Losses: {losses} | "
            f"Goals For: {goals_for} | "
            f"Goals Against: {goals_against}"
        )
    except KeyError as e:
        logger.error(f"Missing field in team statistics: {e}")
        return ""

def format_head_to_head(fixtures: list) -> list[str]:
    results = []
    for fixture in fixtures:
        try:
            home_team = fixture["teams"]["home"]["name"]
            away_team = fixture["teams"]["away"]["name"]
            home_goals = fixture["goals"]["home"]
            away_goals = fixture["goals"]["away"]
            date = fixture["fixture"]["date"]

            results.append(
                f"{home_team} {home_goals} - {away_goals} {away_team} | "
                f"Date: {date}"
            )
        except KeyError as e:
            logger.error(f"Missing field in h2h fixture: {e}")
            continue
    return results

def embed_fixtures(fixtures: list[dict]):
    documents = []
    ids = []
    metadatas = []

    for fixture in fixtures:
        text = format_fixture(fixture)
        if not text:
            continue

        fixture_id = str(fixture["fixture"]["id"])
        home_team = fixture["teams"]["home"]["name"]
        away_team = fixture["teams"]["away"]["name"]

        documents.append(text)
        ids.append(f"fixture_{fixture_id}")
        metadatas.append({
            "type": "fixture",
            "home_team": home_team,
            "away_team": away_team
        })

    if documents:
        add_documents(documents, ids, metadatas)
        logger.info(f"Embedded {len(documents)} fixtures")

def embed_team_statistics(stats: dict, team_id: int):
    text = format_team_statistics(stats)
    if not text:
        return

    add_documents(
        documents=[text],
        ids=[f"stats_{team_id}"],
        metadatas=[{"type": "team_statistics", "team_id": str(team_id)}]
    )
    logger.info(f"Embedded statistics for team {team_id}")

def embed_head_to_head(fixtures: list, team1_id: int, team2_id: int):
    documents = format_head_to_head(fixtures)
    if not documents:
        return

    ids = [f"h2h_{team1_id}_{team2_id}_{i}" for i, _ in enumerate(documents)]
    metadatas = [{"type": "h2h", "team1_id": str(team1_id), "team2_id": str(team2_id)} for _ in documents]

    add_documents(documents, ids, metadatas)
    logger.info(f"Embedded {len(documents)} h2h fixtures")


