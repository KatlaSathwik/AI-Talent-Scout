"""
Candidate Scorer Agent for the AI-Powered Talent Scouting Agent.
Calculates match scores for candidates based on job requirements.
"""
from typing import List, Tuple
from app.models.schemas import JobDescription, Candidate, MatchResult


class CandidateScorer:
    """Agent for scoring candidates based on job requirements."""
    
    def __init__(self):
        """Initialize the candidate scorer."""
        pass
    
    def score_candidates(self, matched_candidates: List[Tuple[Candidate, float]], 
                        job_description: JobDescription) -> List[MatchResult]:
        """
        Score matched candidates based on job requirements.
        
        Args:
            matched_candidates: List of (candidate, similarity_score) tuples
            job_description: Parsed job description
            
        Returns:
            List of MatchResult objects with scores and explanations
        """
        results = []
        
        for candidate, similarity_score in matched_candidates:
            match_result = self._score_candidate(candidate, job_description, similarity_score)
            results.append(match_result)
        
        return results
    
    def _score_candidate(self, candidate: Candidate, job_description: JobDescription, 
                        similarity_score: float) -> MatchResult:
        """
        Score a single candidate based on job requirements.
        
        Args:
            candidate: Candidate to score
            job_description: Parsed job description
            similarity_score: Embedding similarity score
            
        Returns:
            MatchResult with score and explanations
        """
        explanations = []
        
        # 1. Skills match (40% weight)
        skills_score, skills_explanation = self._calculate_skills_score(
            candidate.skills, 
            job_description.skills_required, 
            job_description.skills_optional
        )
        explanations.extend(skills_explanation)
        
        # 2. Experience alignment (20% weight)
        experience_score, exp_explanation = self._calculate_experience_score(
            candidate.years_of_experience, 
            job_description.experience_years
        )
        explanations.extend(exp_explanation)
        
        # 3. Domain match (15% weight)
        domain_score, domain_explanation = self._calculate_domain_score(
            candidate.domain, 
            job_description.domain
        )
        explanations.extend(domain_explanation)
        
        # 4. Seniority level match (15% weight)
        seniority_score, seniority_explanation = self._calculate_seniority_score(
            candidate, 
            job_description
        )
        explanations.extend(seniority_explanation)
        
        # 5. Bonus signals (10% weight)
        bonus_score, bonus_explanation = self._calculate_bonus_score(
            candidate.activity_signals
        )
        explanations.extend(bonus_explanation)
        
        # Calculate weighted score
        match_score = (
            skills_score * 0.4 +
            experience_score * 0.2 +
            domain_score * 0.15 +
            seniority_score * 0.15 +
            bonus_score * 0.1
        )
        
        # Adjust score based on similarity
        match_score = match_score * 0.7 + similarity_score * 30 * 0.3  # Scale similarity to 0-100
        
        return MatchResult(
            candidate_id=candidate.id,
            match_score=match_score,
            match_explanation=explanations
        )
    
    def _calculate_skills_score(self, candidate_skills: List[str], 
                               required_skills: List[str], 
                               optional_skills: List[str]) -> Tuple[float, List[str]]:
        """Calculate skills match score."""
        explanations = []
        
        candidate_skill_set = set(skill.lower() for skill in candidate_skills)
        required_skill_set = set(skill.lower() for skill in required_skills)
        optional_skill_set = set(skill.lower() for skill in optional_skills)
        
        # Count matching required skills
        matching_required = required_skill_set.intersection(candidate_skill_set)
        required_match_ratio = len(matching_required) / len(required_skill_set) if required_skill_set else 1.0
        
        # Count matching optional skills
        matching_optional = optional_skill_set.intersection(candidate_skill_set)
        optional_match_ratio = len(matching_optional) / len(optional_skill_set) if optional_skill_set else 0.0
        
        # Calculate score: 80% for required skills, 20% for optional skills
        skills_score = (required_match_ratio * 0.8 + optional_match_ratio * 0.2) * 100
        
        # Add explanations
        if matching_required:
            explanations.append(f"Has {len(matching_required)} out of {len(required_skill_set)} required skills")
        if matching_optional:
            explanations.append(f"Has {len(matching_optional)} out of {len(optional_skill_set)} optional skills")
        if len(matching_required) < len(required_skill_set):
            missing = required_skill_set - candidate_skill_set
            explanations.append(f"Missing required skills: {', '.join(list(missing)[:3])}")
        
        return skills_score, explanations
    
    def _calculate_experience_score(self, candidate_exp: int, required_exp: int) -> Tuple[float, List[str]]:
        """Calculate experience alignment score."""
        explanations = []
        
        if candidate_exp >= required_exp:
            # Exact match or more experience gets full points
            exp_score = 100.0
            explanations.append(f"Meets experience requirement ({candidate_exp} years >= {required_exp} years)")
        else:
            # Partial credit for close experience
            ratio = candidate_exp / required_exp if required_exp > 0 else 0
            exp_score = max(0, ratio * 100)
            explanations.append(f"Below experience requirement ({candidate_exp} years < {required_exp} years)")
        
        return exp_score, explanations
    
    def _calculate_domain_score(self, candidate_domain: str, job_domain: str) -> Tuple[float, List[str]]:
        """Calculate domain match score."""
        explanations = []
        
        candidate_domain_lower = candidate_domain.lower()
        job_domain_lower = job_domain.lower()
        
        if candidate_domain_lower == job_domain_lower:
            domain_score = 100.0
            explanations.append(f"Exact domain match: {candidate_domain}")
        elif self._are_domains_related(candidate_domain_lower, job_domain_lower):
            domain_score = 75.0
            explanations.append(f"Related domain: {candidate_domain} vs {job_domain}")
        else:
            domain_score = 25.0
            explanations.append(f"Different domain: {candidate_domain} vs {job_domain}")
        
        return domain_score, explanations
    
    def _are_domains_related(self, domain1: str, domain2: str) -> bool:
        """Check if two domains are related."""
        related_domains = {
            "tech": ["software", "it", "information technology", "web", "mobile"],
            "finance": ["banking", "investment", "insurance", "fintech"],
            "healthcare": ["medical", "hospital", "clinical", "pharma"],
            "data science": ["analytics", "data", "ml", "ai", "machine learning", "artificial intelligence"]
        }
        
        # Check if domains are in the same category
        for category, domains in related_domains.items():
            if domain1 == category or domain1 in domains:
                if domain2 == category or domain2 in domains:
                    return True
        
        return False
    
    def _calculate_seniority_score(self, candidate: Candidate, job_description: JobDescription) -> Tuple[float, List[str]]:
        """Calculate seniority level match score."""
        explanations = []
        
        candidate_exp = candidate.years_of_experience
        job_seniority = job_description.seniority.lower()
        
        # Map experience to expected seniority
        if candidate_exp < 2:
            candidate_seniority = "junior"
        elif candidate_exp < 5:
            candidate_seniority = "mid-level"
        elif candidate_exp < 8:
            candidate_seniority = "senior"
        else:
            candidate_seniority = "lead"
        
        if candidate_seniority == job_seniority:
            seniority_score = 100.0
            explanations.append(f"Seniority level match: {candidate_seniority.title()}")
        elif (
            (candidate_seniority == "mid-level" and job_seniority == "senior") or
            (candidate_seniority == "senior" and job_seniority == "mid-level") or
            (candidate_seniority == "lead" and job_seniority == "senior") or
            (candidate_seniority == "senior" and job_seniority == "lead")
        ):
            seniority_score = 75.0
            explanations.append(f"Close seniority match: {candidate_seniority.title()} vs {job_seniority.title()}")
        else:
            seniority_score = 50.0
            explanations.append(f"Some seniority mismatch: {candidate_seniority.title()} vs {job_seniority.title()}")
        
        return seniority_score, explanations
    
    def _calculate_bonus_score(self, activity_signals: dict) -> Tuple[float, List[str]]:
        """Calculate bonus signals score."""
        explanations = []
        bonus_points = 0
        
        # Check for positive signals
        if activity_signals.get("open_to_work", False):
            bonus_points += 30
            explanations.append("Candidate is open to work")
        
        if activity_signals.get("profile_updated", False):
            bonus_points += 20
            explanations.append("Recent profile activity")
        
        if activity_signals.get("recently_applied", False):
            bonus_points += 15
            explanations.append("Recently applied to jobs")
        
        # Cap at 100
        bonus_score = min(100.0, bonus_points)
        
        if bonus_points == 0:
            explanations.append("No additional activity signals")
        
        return bonus_score, explanations