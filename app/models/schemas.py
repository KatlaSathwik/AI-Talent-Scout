"""
Data models and schemas for the AI-Powered Talent Scouting Agent.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel


class JobDescription(BaseModel):
    """Structured representation of a job description."""
    role: str
    skills_required: List[str]
    skills_optional: List[str]
    experience_years: int
    seniority: str
    domain: str
    signals: List[str]


class Candidate(BaseModel):
    """Representation of a candidate."""
    id: str
    name: str
    skills: List[str]
    years_of_experience: int
    domain: str
    past_roles: List[str]
    activity_signals: Dict[str, bool]


class MatchResult(BaseModel):
    """Result of matching a candidate to a job."""
    candidate_id: str
    match_score: float  # 0-100
    match_explanation: List[str]


class InterestAssessment(BaseModel):
    """Assessment of candidate interest."""
    candidate_id: str
    interest_score: float  # 0-100
    interest_explanation: List[str]
    status: str  # "interested", "not_interested", "unknown"
    engagement_level: str  # "high", "medium", "low"


class RankedCandidate(BaseModel):
    """Final ranked candidate with scores and explanations."""
    name: str
    match_score: float
    interest_score: float
    final_score: float
    match_explanation: List[str]
    interest_explanation: List[str]


class AnalysisResponse(BaseModel):
    """Response model for the /analyze endpoint."""
    candidates: List[RankedCandidate]