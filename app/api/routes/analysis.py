from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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
    
    # placeholder for now — we'll replace this with real logic soon
    return AnalysisResponse(
        query=request.query,
        analysis="Analysis coming soon...",
        league=request.league
    )