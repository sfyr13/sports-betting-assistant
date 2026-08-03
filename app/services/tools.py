import logging
from langchain_core.tools import tool
from app.services.fetcher import get_fixtures, get_team_statistics, get_head_to_head,search_team
from app.services.embedder import embed_fixtures, embed_team_statistics, embed_head_to_head
from app.db.vector_store import query_documents

logger = logging.getLogger(__name__)

@tool
def find_team_id(team_name: str) -> str:
    """
    Search for a football team by name and return its ID and basic info.
    ALWAYS use this tool first when you need a team's ID and don't already
    know it for certain, before calling any other tool that requires a team_id.
    Never guess a team ID.
    """
    teams = search_team(team_name)
    if not teams:
        return f"No team found matching '{team_name}'."

    results = []
    for entry in teams[:5]:
        team = entry["team"]
        results.append(f"{team['name']} (ID: {team['id']}, Country: {team['country']})")

    return "\n".join(results)

@tool
def search_existing_data(query: str) -> str:
    """
    Search the vector database for existing sports data relevant to the query.
    Use this FIRST before fetching new data, to check what's already available.
    Returns relevant context if found, or a message saying nothing was found.
    """
    results = query_documents(query_text=query, n_results=5)
    if not results:
        return "No relevant data found in the existing database."
    return "\n".join(results)


@tool
def fetch_and_store_fixtures(league_id: int, season: int, from_date: str, to_date: str) -> str:
    """
    Fetch fixtures for a given league, season, and date range from API-Football,
    then store them in the vector database. Use this when existing data is
    insufficient and you need fresh fixture/match results.
    Dates must be in YYYY-MM-DD format.
    """
    fixtures = get_fixtures(league_id, season, from_date=from_date, to_date=to_date)
    if not fixtures:
        return "No fixtures found for these parameters."

    embed_fixtures(fixtures)
    return f"Fetched and stored {len(fixtures)} fixtures."


@tool
def fetch_and_store_team_stats(league_id: int, season: int, team_id: int) -> str:
    """
    Fetch season statistics for a specific team (wins, losses, goals, form)
    from API-Football, then store them in the vector database.
    Use this when you need a team's overall performance data.
    """
    stats = get_team_statistics(league_id, season, team_id)
    if not stats:
        return "No statistics found for this team."

    embed_team_statistics(stats, team_id)
    return f"Fetched and stored statistics for team {team_id}."


@tool
def fetch_and_store_head_to_head(team1_id: int, team2_id: int, from_date: str = None, to_date: str = None) -> str:
    """
    Fetch head-to-head match history between two teams from API-Football within
    a date range, then store it in the vector database. Use this when the question
    involves comparing two specific teams' past matchups. Dates must be YYYY-MM-DD.
    If you don't know a good date range, use a wide one like the last 1-2 years.
    """
    fixtures = get_head_to_head(team1_id, team2_id, from_date, to_date)
    if not fixtures:
        return "No head-to-head data found for these teams in this date range."

    embed_head_to_head(fixtures, team1_id, team2_id)
    return f"Fetched and stored {len(fixtures)} head-to-head fixtures."