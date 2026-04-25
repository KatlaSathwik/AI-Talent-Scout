"""
Candidate Matcher Agent for the AI-Powered Talent Scouting Agent.
Matches candidates to job descriptions using embeddings and filtering.
"""
import numpy as np
from typing import List, Tuple

from app.models.schemas import JobDescription, Candidate, MatchResult
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.candidate_service import CandidateService


class CandidateMatcher:
    """Agent for matching candidates to job descriptions."""
    
    def __init__(self):
        """Initialize the candidate matcher."""
        self.embedding_service = EmbeddingService()
        self.candidate_service = CandidateService()
        self.vector_store = None
    
    def find_matches(self, job_description: JobDescription, k: int = 10) -> List[Tuple[Candidate, float]]:
        """
        Find matching candidates for a job description.
        
        Args:
            job_description: Parsed job description
            k: Number of candidates to return
            
        Returns:
            List of (candidate, similarity_score) tuples
        """
        # Get all candidates
        candidates = self.candidate_service.get_all_candidates()
        
        # Filter candidates by minimum experience
        filtered_candidates = [
            c for c in candidates 
            if c.years_of_experience >= job_description.experience_years
        ]
        
        # Further filter by required skills
        required_skills = set(skill.lower() for skill in job_description.skills_required)
        skill_filtered_candidates = []
        
        for candidate in filtered_candidates:
            candidate_skills = set(skill.lower() for skill in candidate.skills)
            # Check if candidate has all required skills
            if required_skills.issubset(candidate_skills):
                skill_filtered_candidates.append(candidate)
        
        # If we have too few candidates after filtering, relax the skill filter
        if len(skill_filtered_candidates) < 3:
            skill_filtered_candidates = filtered_candidates
        
        # Create embeddings for job description and candidates
        job_text = self._create_job_text(job_description)
        job_embedding = self.embedding_service.get_embedding(job_text)
        
        candidate_texts = [self._create_candidate_text(c) for c in skill_filtered_candidates]
        
        # Calculate similarities
        similarities = []
        for i, candidate in enumerate(skill_filtered_candidates):
            if i < len(candidate_texts):
                candidate_embedding = self.embedding_service.get_embedding(candidate_texts[i])
                similarity = self.embedding_service.cosine_similarity(job_embedding, candidate_embedding)
                similarities.append((candidate, similarity))
        
        # Sort by similarity score (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k candidates
        return similarities[:k]
    
    def _create_job_text(self, job_description: JobDescription) -> str:
        """Create a text representation of the job description for embedding."""
        skills_text = ", ".join(job_description.skills_required + job_description.skills_optional)
        return f"{job_description.role} in {job_description.domain} requiring {skills_text}"
    
    def _create_candidate_text(self, candidate: Candidate) -> str:
        """Create a text representation of the candidate for embedding."""
        skills_text = ", ".join(candidate.skills)
        roles_text = ", ".join(candidate.past_roles)
        return f"{candidate.name}: {skills_text}. Past roles: {roles_text}"