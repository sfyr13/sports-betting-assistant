from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.analyst import analyze_query
from app.services.agent import run_agent_analysis


router = APIRouter()

class AnalysisRequest(BaseModel):
    query: str
    league: str = "football"

class AnalysisResponse(BaseModel):
    query: str
    analysis: str
    league: str

class AgentAnalysisRequest(BaseModel):
    query: str

class AgentAnalysisResponse(BaseModel):
    query: str
    analysis: str

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


@router.post("/agent-analyze", response_model=AgentAnalysisResponse)
async def agent_analyze(request: AgentAnalysisRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    analysis_result = run_agent_analysis(request.query)

    return AgentAnalysisResponse(
        query=request.query,
        analysis=analysis_result
    )