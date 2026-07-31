from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.fetcher import get_fixtures, get_team_statistics, get_head_to_head
from app.services.embedder import embed_fixtures, embed_team_statistics, embed_head_to_head

router = APIRouter()

class IngestFixturesRequest(BaseModel):
    league_id: int
    season: int
    next: int = None
    from_date: str = None
    to_date: str = None

class IngestTeamStatsRequest(BaseModel):
    league_id: int
    season: int
    team_id: int

class IngestH2HRequest(BaseModel):
    team1_id: int
    team2_id: int
    last: int = 5

@router.post("/ingest/fixtures")
async def ingest_fixtures(request: IngestFixturesRequest):
    fixtures = get_fixtures(
        request.league_id,
        request.season,
        request.next,
        request.from_date,
        request.to_date
    )

    if not fixtures:
        raise HTTPException(status_code=404, detail="No fixtures found for these parameters")

    embed_fixtures(fixtures)

    return {"message": f"Ingested {len(fixtures)} fixtures"}

@router.post("/ingest/team-stats")
async def ingest_team_stats(request: IngestTeamStatsRequest):
    stats = get_team_statistics(request.league_id, request.season, request.team_id)

    if not stats:
        raise HTTPException(status_code=404, detail="No statistics found for this team")

    embed_team_statistics(stats, request.team_id)

    return {"message": f"Ingested statistics for team {request.team_id}"}

@router.post("/ingest/head-to-head")
async def ingest_head_to_head(request: IngestH2HRequest):
    fixtures = get_head_to_head(request.team1_id, request.team2_id, request.last)

    if not fixtures:
        raise HTTPException(status_code=404, detail="No head-to-head data found")

    embed_head_to_head(fixtures, request.team1_id, request.team2_id)

    return {"message": f"Ingested {len(fixtures)} head-to-head fixtures"}