"""
Main FastAPI application for the AI-Powered Talent Scouting Agent.
"""
from functools import lru_cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import TypedDict

from app.agents.jd_parser import JDParser
from app.agents.matcher import CandidateMatcher
from app.agents.scorer import CandidateScorer
from app.agents.outreach_agent import OutreachAgent
from app.services.candidate_service import CandidateService
from app.models.schemas import JobDescription, RankedCandidate, AnalysisResponse

app = FastAPI(
    title="AI-Powered Talent Scouting Agent",
    description="Parse job descriptions, match candidates, and rank them based on fit and interest",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Services(TypedDict):
    candidate_service: CandidateService
    jd_parser: JDParser
    matcher: CandidateMatcher
    scorer: CandidateScorer
    outreach_agent: OutreachAgent


@lru_cache(maxsize=1)
def get_services() -> Services:
    """Lazily initialize heavy services on first analyze request.

    This avoids startup-time memory spikes on small instances (e.g. Render free tier)
    so the web process can bind to PORT quickly.
    """
    return {
        "candidate_service": CandidateService(),
        "jd_parser": JDParser(),
        "matcher": CandidateMatcher(),
        "scorer": CandidateScorer(),
        "outreach_agent": OutreachAgent(),
    }


class JobDescriptionRequest(BaseModel):
    job_description: str


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_job_description(request: JobDescriptionRequest):
    """
    Analyze a job description and return ranked candidates.
    
    Args:
        request: Job description text
        
    Returns:
        Ranked list of candidates with match and interest scores
    """
    services = get_services()

    # Parse job description
    parsed_jd = services["jd_parser"].parse(request.job_description)
    
    # Find matching candidates
    matched_candidates = services["matcher"].find_matches(parsed_jd)
    
    # Score candidates
    scored_candidates = services["scorer"].score_candidates(matched_candidates, parsed_jd)
    
    # Simulate outreach and get interest scores
    final_candidates = []
    for match_result in scored_candidates:
        # Get the actual candidate object
        candidate = services["candidate_service"].get_candidate_by_id(match_result.candidate_id)
        
        # In a real implementation, we would simulate outreach here
        # For now, we'll use a placeholder interest assessment
        interest_assessment = services["outreach_agent"].assess_interest(candidate, parsed_jd)
        
        # Combine scores
        final_score = 0.6 * match_result.match_score + 0.4 * interest_assessment.interest_score
        
        ranked_candidate = RankedCandidate(
            name=candidate.name,
            match_score=match_result.match_score,
            interest_score=interest_assessment.interest_score,
            final_score=final_score,
            match_explanation=match_result.match_explanation,
            interest_explanation=interest_assessment.interest_explanation
        )
        final_candidates.append(ranked_candidate)
    
    # Sort by final score (descending)
    final_candidates.sort(key=lambda x: x.final_score, reverse=True)
    
    return AnalysisResponse(candidates=final_candidates)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/")
async def root():
    """Root endpoint for platform health checks."""
    return {"service": "ai-talent-scout", "status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
