"""
Job Description Parser Agent for the AI-Powered Talent Scouting Agent.
Parses raw job descriptions into structured data using LLM prompting.
"""
import json
import re
from typing import Dict, List

from pydantic import ValidationError

from app.models.schemas import JobDescription
from app.services.llm_service import LLMService
from app.services.prompt_templates import PromptTemplates


class JDParser:
    """Agent for parsing job descriptions into structured data."""
    
    def __init__(self):
        """Initialize the JD parser."""
        self.prompt_templates = PromptTemplates()
        try:
            self.llm_service = LLMService()
        except Exception:
            self.llm_service = None
    
    def parse(self, job_description: str) -> JobDescription:
        """
        Parse a raw job description into structured data.
        
        Args:
            job_description: Raw job description text
            
        Returns:
            Structured job description object
        """
        # Prefer LLM parsing; fallback to robust rule-based parsing.
        parsed_data = self._parse_with_llm(job_description)
        if parsed_data is None:
            parsed_data = self._simulate_llm_parsing(job_description)

        return JobDescription(**parsed_data)

    def _parse_with_llm(self, job_description: str) -> Dict | None:
        """Parse with Gemini and return normalized dict, or None on failure."""
        if not self.llm_service:
            return None

        prompt = self.prompt_templates.jd_parsing_json_prompt(job_description)
        try:
            payload = self.llm_service.generate_json(prompt, temperature=0.1)
        except Exception:
            return None

        # Minimal normalization
        normalized = {
            "role": str(payload.get("role", "Software Developer")),
            "skills_required": [str(s).lower() for s in payload.get("skills_required", []) if str(s).strip()],
            "skills_optional": [str(s).lower() for s in payload.get("skills_optional", []) if str(s).strip()],
            "experience_years": int(payload.get("experience_years", 3) or 3),
            "seniority": str(payload.get("seniority", "Mid-level")),
            "domain": str(payload.get("domain", "Tech")),
            "signals": [str(s) for s in payload.get("signals", []) if str(s).strip()],
        }

        try:
            JobDescription(**normalized)
            return normalized
        except ValidationError:
            return None
    
    def _simulate_llm_parsing(self, job_description: str) -> dict:
        """
        Simulate LLM parsing of job description.
        In practice, this would call an actual LLM API.
        """
        # Extract role (first noun phrase or sentence containing "developer", "engineer", etc.)
        role_patterns = [
            r"(?i)(senior|lead|principal)?\s*(software|backend|frontend|full[\s-]*stack)?\s*(developer|engineer|programmer)",
            r"(?i)(senior|lead|principal)?\s*(data|machine learning|ai)?\s*(scientist|analyst|engineer)",
            r"(?i)(senior|lead|principal)?\s*(devops|cloud|site reliability)?\s*(engineer|architect)"
        ]
        
        role = "Software Developer"  # Default role
        for pattern in role_patterns:
            match = re.search(pattern, job_description)
            if match:
                role = match.group(0).strip().title()
                break
        
        # Extract skills (look for common technical terms)
        tech_terms = [
            "python", "java", "javascript", "react", "node", "docker", "kubernetes",
            "aws", "azure", "gcp", "sql", "nosql", "mongodb", "postgresql", "mysql",
            "django", "flask", "spring", "angular", "vue", "typescript", "go", "rust",
            "machine learning", "data science", "ai", "tensorflow", "pytorch"
        ]
        
        skills_required = []
        skills_optional = []
        
        # Convert to lowercase for matching
        jd_lower = job_description.lower()
        
        # Look for required skills (with "required", "must have", etc.)
        required_indicators = ["required", "must have", "essential", "mandatory"]
        optional_indicators = ["nice to have", "preferred", "bonus", "optional"]
        
        for term in tech_terms:
            if term in jd_lower:
                # Check if it's explicitly marked as required or optional
                is_required = any(indicator in jd_lower for indicator in required_indicators)
                is_optional = any(indicator in jd_lower for indicator in optional_indicators)
                
                if is_required and not is_optional:
                    skills_required.append(term.title())
                elif is_optional:
                    skills_optional.append(term.title())
                else:
                    # Default to required if not specified
                    skills_required.append(term.title())
        
        # Remove duplicates and limit to reasonable number
        skills_required = list(set(skills_required))[:10]
        skills_optional = list(set(skills_optional))[:5]
        
        # Extract experience (look for number + years)
        experience_match = re.search(r"(\d+)\s*\+?\s*years?", jd_lower)
        experience_years = int(experience_match.group(1)) if experience_match else 3
        
        # Determine seniority based on experience
        if experience_years < 2:
            seniority = "Junior"
        elif experience_years < 5:
            seniority = "Mid-level"
        elif experience_years < 8:
            seniority = "Senior"
        else:
            seniority = "Lead"
        
        # Extract domain (tech, finance, healthcare, etc.)
        domains = ["tech", "technology", "finance", "financial", "healthcare", "health", 
                  "ecommerce", "retail", "consulting", "startup", "enterprise"]
        domain = "Tech"  # Default
        for d in domains:
            if d in jd_lower:
                domain = d.title()
                break
        
        # Extract signals (remote work, visa sponsorship, etc.)
        signals = []
        if "remote" in jd_lower:
            signals.append("Remote work available")
        if "visa" in jd_lower or "sponsorship" in jd_lower:
            signals.append("Visa sponsorship available")
        if "flexible hours" in jd_lower or "flexibility" in jd_lower:
            signals.append("Flexible working hours")
        
        return {
            "role": role,
            "skills_required": skills_required,
            "skills_optional": skills_optional,
            "experience_years": experience_years,
            "seniority": seniority,
            "domain": domain,
            "signals": signals
        }
