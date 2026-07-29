from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.analyst import analyze_query

router = APIRouter()

class AnalysisRequest(BaseModel):
    query: str
    league: str = "football"

class AnalysisResponse(BaseModel):
    query: str
    analysis: str
    league: str

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    analysis_result = analyze_query(request.query)

    return AnalysisResponse(
        query=request.query,
        analysis=analysis_result,
        league=request.league
    )