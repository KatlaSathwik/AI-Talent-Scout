"""
Prompt templates for LLM interactions in the AI-Powered Talent Scouting Agent.
"""
from typing import Dict, Any


class PromptTemplates:
    """Collection of prompt templates for different agent functionalities."""
    
    @staticmethod
    def jd_parsing_prompt(job_description: str) -> str:
        """Generate prompt for parsing job descriptions."""
        return f"""
You are an expert recruiter specializing in parsing job descriptions. 
Extract the following information from the job description below:

Role: [Main job title]
Skills Required: [List of required skills]
Skills Optional: [List of preferred/nice-to-have skills]
Experience: [Minimum years of experience required]
Seniority: [Seniority level: Junior/Mid-level/Senior/Lead/Executive]
Domain: [Industry domain: Tech/Finance/Healthcare/etc.]
Signals: [Other important signals like remote work, visa sponsorship, etc.]

Job Description:
{job_description}

Provide your response in the exact format specified above.
""".strip()

    @staticmethod
    def jd_parsing_json_prompt(job_description: str) -> str:
        """Generate deterministic JSON-only prompt for JD parsing."""
        return f"""
You are an expert recruiter. Extract structured information from the job description.

Return ONLY valid JSON with this exact schema:
{{
  "role": "string",
  "skills_required": ["string"],
  "skills_optional": ["string"],
  "experience_years": 0,
  "seniority": "Junior|Mid-level|Senior|Lead|Executive",
  "domain": "string",
  "signals": ["string"]
}}

Rules:
- Keep skills lowercase normalized names where possible (e.g., "python", "fastapi").
- If experience is absent, infer a reasonable integer.
- Do not include markdown or commentary.

Job Description:
{job_description}
""".strip()

    @staticmethod
    def outreach_simulation_prompt(candidate_name: str, role: str, company: str = "Acme Corp") -> str:
        """Generate prompt for simulating outreach conversations."""
        return f"""
You are conducting an initial outreach conversation with {candidate_name}, a potential job candidate.
Your goal is to assess their interest in the opportunity without being pushy.

Job Role: {role}
Company: {company}
Location: Remote

Conversation History:
Recruiter: Hi {candidate_name}, I'm reaching out because I think you might be a great fit for a Senior Developer position at {company}. Are you open to exploring new opportunities?

Based on their profile and the job details, generate a realistic response that indicates their level of interest.
Consider factors like:
- Alignment with their background
- Career progression opportunities
- Compensation and benefits (if mentioned)
- Location preferences
- Current employment status

Respond in a natural, conversational tone as if you were the candidate.
""".strip()

    @staticmethod
    def interest_classification_prompt(conversation_transcript: str) -> str:
        """Generate prompt for classifying candidate interest."""
        return f"""
Analyze the candidate's response in the conversation below and classify their interest level.

Conversation:
{conversation_transcript}

Classify their interest as one of:
- HIGH: Clearly interested and engaged
- MEDIUM: Somewhat interested but with reservations
- LOW: Not interested or lukewarm response
- DECLINE: Explicitly not interested

Also extract key signals about:
- Availability
- Salary expectations
- Relocation willingness
- Other constraints

Provide your response in JSON format:
{{
  "interest_level": "HIGH|MEDIUM|LOW|DECLINE",
  "key_signals": ["signal1", "signal2", ...],
  "summary": "Brief summary of their position"
}}
""".strip()

    @staticmethod
    def interest_classification_json_prompt(conversation_transcript: str) -> str:
        """Generate deterministic JSON-only prompt for interest classification."""
        return f"""
Analyze the conversation and classify candidate interest.

Return ONLY valid JSON with this exact schema:
{{
  "interest_level": "HIGH|MEDIUM|LOW|DECLINE",
  "key_signals": ["string"],
  "summary": "string"
}}

Conversation:
{conversation_transcript}
""".strip()
