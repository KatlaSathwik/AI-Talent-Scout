"""
Outreach Agent for the AI-Powered Talent Scouting Agent.
Simulates conversational outreach to estimate candidate interest.
"""
import random
from typing import Dict, List

from app.models.schemas import Candidate, JobDescription, InterestAssessment
from app.services.llm_service import LLMService
from app.services.prompt_templates import PromptTemplates


class OutreachAgent:
    """Agent for simulating outreach conversations with candidates."""
    
    def __init__(self):
        """Initialize the outreach agent."""
        self.prompt_templates = PromptTemplates()
        try:
            self.llm_service = LLMService()
        except Exception:
            self.llm_service = None
    
    def assess_interest(self, candidate: Candidate, job_description: JobDescription) -> InterestAssessment:
        """
        Simulate outreach conversation and assess candidate interest.
        
        Args:
            candidate: Candidate to assess
            job_description: Job description for the position
            
        Returns:
            InterestAssessment with interest score and explanations
        """
        # Try LLM-driven classification first; fallback to rule-based simulation.
        llm_assessment = self._assess_interest_with_llm(candidate, job_description)
        if llm_assessment:
            interest_level = llm_assessment["interest_level"]
            explanations = llm_assessment["explanations"]
        else:
            interest_level, explanations = self._simulate_interest_assessment(candidate, job_description)
        
        # Convert interest level to score
        interest_score_map = {
            "HIGH": 90,
            "MEDIUM": 60,
            "LOW": 30,
            "DECLINE": 10
        }
        
        interest_score = interest_score_map.get(interest_level, 50)
        
        # Determine engagement level based on activity signals
        engagement_level = self._determine_engagement_level(candidate)
        
        return InterestAssessment(
            candidate_id=candidate.id,
            interest_score=interest_score,
            interest_explanation=explanations,
            status=interest_level.lower(),
            engagement_level=engagement_level
        )

    def _assess_interest_with_llm(self, candidate: Candidate, job_description: JobDescription) -> Dict | None:
        """Use Gemini to classify interest from simulated conversation transcript."""
        if not self.llm_service:
            return None

        transcript = "\n".join(self.simulate_conversation(candidate, job_description))
        prompt = self.prompt_templates.interest_classification_json_prompt(transcript)

        try:
            payload = self.llm_service.generate_json(prompt, temperature=0.1)
        except Exception:
            return None

        interest_level = str(payload.get("interest_level", "MEDIUM")).upper()
        if interest_level not in {"HIGH", "MEDIUM", "LOW", "DECLINE"}:
            interest_level = "MEDIUM"

        key_signals = payload.get("key_signals", [])
        summary = payload.get("summary", "")

        explanations: List[str] = []
        if isinstance(key_signals, list):
            explanations.extend([str(s) for s in key_signals if str(s).strip()])
        if summary:
            explanations.append(str(summary))
        if not explanations:
            explanations.append("Interest assessed by Gemini conversation classification")

        return {
            "interest_level": interest_level,
            "explanations": explanations,
        }
    
    def _simulate_interest_assessment(self, candidate: Candidate, 
                                    job_description: JobDescription) -> tuple:
        """
        Simulate interest assessment based on candidate profile and job description.
        
        Returns:
            Tuple of (interest_level, explanations)
        """
        explanations = []
        
        # Check domain match
        if candidate.domain.lower() == job_description.domain.lower():
            explanations.append(f"Candidate's domain ({candidate.domain}) matches job domain ({job_description.domain})")
        else:
            explanations.append(f"Candidate's domain ({candidate.domain}) differs from job domain ({job_description.domain})")
        
        # Check skills match
        candidate_skills = set(skill.lower() for skill in candidate.skills)
        required_skills = set(skill.lower() for skill in job_description.skills_required)
        
        matching_skills = candidate_skills.intersection(required_skills)
        if matching_skills:
            explanations.append(f"Candidate has {len(matching_skills)} out of {len(required_skills)} required skills")
        else:
            explanations.append("Candidate lacks required skills")
        
        # Check experience match
        if candidate.years_of_experience >= job_description.experience_years:
            explanations.append(f"Candidate meets experience requirement ({candidate.years_of_experience} years)")
        else:
            explanations.append(f"Candidate below experience requirement ({candidate.years_of_experience} vs {job_description.experience_years} years)")
        
        # Determine interest level based on matches
        skill_match_ratio = len(matching_skills) / len(required_skills) if required_skills else 0
        
        # If candidate has most required skills and meets experience, likely HIGH interest
        if skill_match_ratio >= 0.8 and candidate.years_of_experience >= job_description.experience_years:
            interest_level = "HIGH"
        elif skill_match_ratio >= 0.5 and candidate.years_of_experience >= job_description.experience_years * 0.7:
            interest_level = "MEDIUM"
        elif skill_match_ratio >= 0.3 or candidate.years_of_experience >= job_description.experience_years * 0.5:
            interest_level = "LOW"
        else:
            interest_level = "DECLINE"
        
        # Adjust based on activity signals
        if candidate.activity_signals.get("open_to_work", False):
            # Increase interest level
            if interest_level == "DECLINE":
                interest_level = "LOW"
            elif interest_level == "LOW":
                interest_level = "MEDIUM"
            elif interest_level == "MEDIUM":
                interest_level = "HIGH"
            explanations.append("Candidate is open to work")
        
        if candidate.activity_signals.get("recently_applied", False):
            # Increase interest level
            if interest_level == "DECLINE":
                interest_level = "LOW"
            elif interest_level == "LOW":
                interest_level = "MEDIUM"
            explanations.append("Candidate recently applied to jobs")
        
        return interest_level, explanations
    
    def _determine_engagement_level(self, candidate: Candidate) -> str:
        """Determine engagement level based on activity signals."""
        open_to_work = candidate.activity_signals.get("open_to_work", False)
        profile_updated = candidate.activity_signals.get("profile_updated", False)
        recently_applied = candidate.activity_signals.get("recently_applied", False)
        
        # Count positive signals
        positive_signals = sum([open_to_work, profile_updated, recently_applied])
        
        if positive_signals >= 2:
            return "high"
        elif positive_signals == 1:
            return "medium"
        else:
            return "low"
    
    def simulate_conversation(self, candidate: Candidate, job_description: JobDescription) -> List[str]:
        """
        Simulate a conversation with the candidate.
        
        Args:
            candidate: Candidate to converse with
            job_description: Job description for the position
            
        Returns:
            List of conversation turns
        """
        # This would be implemented with actual LLM calls in a real system
        # For now, we'll simulate a basic conversation
        
        conversation = []
        
        # Initial outreach
        conversation.append(f"Recruiter: Hi {candidate.name}, I'm reaching out because I think you might be a great fit for a {job_description.role} position. Are you open to exploring new opportunities?")
        
        # Candidate response (simulated)
        if candidate.activity_signals.get("open_to_work", False):
            response = f"{candidate.name}: Yes, I'm definitely open to new opportunities, especially in {candidate.domain}. What can you tell me about the role?"
        else:
            response = f"{candidate.name}: I'm currently employed, but I'm always interested in hearing about new opportunities. What does this position entail?"
        
        conversation.append(response)
        
        # Follow-up questions
        conversation.append("Recruiter: It's a senior position requiring skills in " + ", ".join(job_description.skills_required[:3]) + ". The role involves working with modern technologies and offers opportunities for growth. What's your current availability like?")
        
        # Candidate availability response
        if candidate.activity_signals.get("open_to_work", False):
            response = f"{candidate.name}: I'm available immediately and very interested in discussing this further."
        else:
            response = f"{candidate.name}: I'm currently employed full-time, but I'd be open to discussing the role during my free time. What's the timeline for this position?"
        
        conversation.append(response)
        
        return conversation
