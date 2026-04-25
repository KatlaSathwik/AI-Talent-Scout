"""
Demo script for the AI-Powered Talent Scouting Agent.
Shows a complete example of how the system works.
"""
import json

from app.agents.jd_parser import JDParser
from app.agents.matcher import CandidateMatcher
from app.agents.scorer import CandidateScorer
from app.agents.outreach_agent import OutreachAgent
from app.services.candidate_service import CandidateService
from app.services.embedding_service import EmbeddingService
from app.services.cache_service import CacheService


def demo_pipeline():
    """Run a demonstration of the talent scouting pipeline."""
    print("AI-Powered Talent Scouting Agent - Demo")
    print("=" * 50)
    
    # Sample job description
    job_description = """
    Senior Backend Engineer - Python/Django
    
    We're looking for an experienced Backend Engineer to join our team. 
    You'll be responsible for designing and implementing scalable backend services.
    
    Requirements:
    - 5+ years of experience with Python and Django
    - Strong experience with PostgreSQL
    - Experience with AWS services
    - Knowledge of Docker and containerization
    - Familiarity with RESTful APIs
    
    Nice to have:
    - Experience with FastAPI
    - Knowledge of Redis
    - Familiarity with CI/CD pipelines
    
    This is a remote position with excellent benefits and growth opportunities.
    """
    
    # Step 1: Parse job description
    print("Step 1: Parsing job description...")
    parser = JDParser()
    parsed_jd = parser.parse(job_description)
    
    print(f"  Role: {parsed_jd.role}")
    print(f"  Required skills: {', '.join(parsed_jd.skills_required)}")
    print(f"  Experience required: {parsed_jd.experience_years} years")
    print(f"  Domain: {parsed_jd.domain}")
    print()
    
    # Step 2: Find matching candidates
    print("Step 2: Finding matching candidates...")
    matcher = CandidateMatcher()
    matched_candidates = matcher.find_matches(parsed_jd, k=5)
    print(f"  Found {len(matched_candidates)} matching candidates")
    print()
    
    # Step 3: Score candidates
    print("Step 3: Scoring candidates...")
    scorer = CandidateScorer()
    scored_candidates = scorer.score_candidates(matched_candidates, parsed_jd)
    print(f"  Scored {len(scored_candidates)} candidates")
    print()
    
    # Step 4: Assess interest
    print("Step 4: Assessing candidate interest...")
    outreach_agent = OutreachAgent()
    candidate_service = CandidateService()
    
    rankings = []
    for match_result in scored_candidates:
        candidate = candidate_service.get_candidate_by_id(match_result.candidate_id)
        interest_assessment = outreach_agent.assess_interest(candidate, parsed_jd)
        
        # Calculate final score
        final_score = 0.6 * match_result.match_score + 0.4 * interest_assessment.interest_score
        
        rankings.append({
            "name": candidate.name,
            "match_score": round(match_result.match_score, 1),
            "interest_score": round(interest_assessment.interest_score, 1),
            "final_score": round(final_score, 1),
            "skills": candidate.skills,
            "experience": candidate.years_of_experience
        })
    
    # Sort by final score
    rankings.sort(key=lambda x: x["final_score"], reverse=True)
    
    # Display results
    print("Final Rankings:")
    print("-" * 30)
    for i, candidate in enumerate(rankings, 1):
        print(f"  {i}. {candidate['name']}")
        print(f"     Final Score: {candidate['final_score']}")
        print(f"     Match Score: {candidate['match_score']}")
        print(f"     Interest Score: {candidate['interest_score']}")
        print(f"     Experience: {candidate['experience']} years")
        print(f"     Skills: {', '.join(candidate['skills'][:5])}")
        print()
    
    # Show cache stats
    print("Cache Statistics:")
    cache_service = CacheService()
    stats = cache_service.get_stats()
    print(f"  Cache entries: {stats['cache_entries']}")
    print(f"  Total size: {stats['total_size_bytes']} bytes")
    
    return rankings


if __name__ == "__main__":
    demo_pipeline()