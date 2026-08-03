from fastapi import FastAPI
from app.api.routes import analysis, ingestion

app = FastAPI(
    title="MatchSense",
    description="AI-powered sports betting analysis",
    version="1.0.0"
)

app.include_router(analysis.router, prefix="/api/v1")
app.include_router(ingestion.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}