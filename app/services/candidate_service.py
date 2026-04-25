"""
Candidate service for the AI-Powered Talent Scouting Agent.
Manages candidate data operations and retrieval.
"""
import json
from typing import List, Dict
from pathlib import Path

from app.models.schemas import Candidate


class CandidateService:
    """Service for managing candidate data."""
    
    def __init__(self, data_file: str = "./app/data/candidates.json"):
        """Initialize the candidate service."""
        self.data_file = Path(data_file)
        self.candidates = self._load_candidates()
    
    def _load_candidates(self) -> List[Candidate]:
        """Load candidates from JSON file."""
        if not self.data_file.exists():
            return []
        
        with open(self.data_file, 'r') as f:
            data = json.load(f)
        
        candidates = []
        for item in data:
            candidate = Candidate(**item)
            candidates.append(candidate)
        
        return candidates
    
    def get_all_candidates(self) -> List[Candidate]:
        """Get all candidates."""
        return self.candidates
    
    def get_candidate_by_id(self, candidate_id: str) -> Candidate:
        """Get a candidate by ID."""
        for candidate in self.candidates:
            if candidate.id == candidate_id:
                return candidate
        raise ValueError(f"Candidate with ID {candidate_id} not found")
    
    def get_candidates_by_domain(self, domain: str) -> List[Candidate]:
        """Get candidates by domain."""
        return [c for c in self.candidates if c.domain.lower() == domain.lower()]
    
    def get_candidates_with_skills(self, skills: List[str]) -> List[Candidate]:
        """Get candidates who have all the specified skills."""
        matching_candidates = []
        skill_set = set(skill.lower() for skill in skills)
        
        for candidate in self.candidates:
            candidate_skills = set(skill.lower() for skill in candidate.skills)
            if skill_set.issubset(candidate_skills):
                matching_candidates.append(candidate)
        
        return matching_candidates
    
    def filter_candidates_by_experience(self, min_experience: int) -> List[Candidate]:
        """Filter candidates by minimum years of experience."""
        return [c for c in self.candidates if c.years_of_experience >= min_experience]