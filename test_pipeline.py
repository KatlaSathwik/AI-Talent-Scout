"""
Test script for the AI-Powered Talent Scouting Agent.
Demonstrates the full pipeline functionality.
"""
import json
from app.agents.jd_parser import JDParser
from app.agents.matcher import CandidateMatcher
from app.agents.scorer import CandidateScorer
from app.agents.outreach_agent import OutreachAgent
from app.services.candidate_service import CandidateService


def main():
    """Run the full talent scouting pipeline."""
    print("AI-Powered Talent Scouting Agent - Test Pipeline")
    print("=" * 50)
    
    # Sample job description
    job_description_text = """
    We are looking for a Senior Python Developer with 5+ years of experience to join our team.
    The ideal candidate will have strong skills in Django, FastAPI, PostgreSQL, and AWS.
    Experience with Docker and Kubernetes is a plus.
    This is a remote position with competitive salary and benefits.
    
    Responsibilities:
    - Design and implement scalable backend systems
    - Collaborate with frontend developers and product managers
    - Write clean, maintainable, and well-tested code
    - Participate in code reviews and technical discussions
    
    Requirements:
    - 5+ years of experience with Python
    - Strong experience with Django and/or FastAPI
    - Proficiency with PostgreSQL or similar relational databases
    - Experience with AWS cloud services
    - Familiarity with Docker and containerization
    - BS/MS in Computer Science or related field
    
    Nice to have:
    - Experience with Kubernetes
    - Knowledge of machine learning frameworks
    - Experience with CI/CD pipelines
    """
    
    print("1. Parsing Job Description...")
    jd_parser = JDParser()
    parsed_jd = jd_parser.parse(job_description_text)
    print(f"   Role: {parsed_jd.role}")
    print(f"   Required Skills: {', '.join(parsed_jd.skills_required)}")
    print(f"   Experience Required: {parsed_jd.experience_years} years")
    print(f"   Domain: {parsed_jd.domain}")
    print()
    
    print("2. Finding Matching Candidates...")
    matcher = CandidateMatcher()
    matched_candidates = matcher.find_matches(parsed_jd, k=10)
    print(f"   Found {len(matched_candidates)} matching candidates")
    print()
    
    print("3. Scoring Candidates...")
    scorer = CandidateScorer()
    scored_candidates = scorer.score_candidates(matched_candidates, parsed_jd)
    print(f"   Scored {len(scored_candidates)} candidates")
    print()
    
    print("4. Assessing Candidate Interest...")
    outreach_agent = OutreachAgent()
    candidate_service = CandidateService()
    
    final_rankings = []
    for match_result in scored_candidates:
        candidate = candidate_service.get_candidate_by_id(match_result.candidate_id)
        interest_assessment = outreach_agent.assess_interest(candidate, parsed_jd)
        
        # Calculate final score
        final_score = 0.6 * match_result.match_score + 0.4 * interest_assessment.interest_score
        
        final_rankings.append({
            "name": candidate.name,
            "match_score": match_result.match_score,
            "interest_score": interest_assessment.interest_score,
            "final_score": final_score,
            "match_explanation": match_result.match_explanation,
            "interest_explanation": interest_assessment.interest_explanation
        })
    
    # Sort by final score (descending)
    final_rankings.sort(key=lambda x: x["final_score"], reverse=True)
    
    print("5. Final Rankings:")
    print("-" * 30)
    for i, candidate in enumerate(final_rankings[:5], 1):
        print(f"   {i}. {candidate['name']}")
        print(f"      Final Score: {candidate['final_score']:.1f}")
        print(f"      Match Score: {candidate['match_score']:.1f}")
        print(f"      Interest Score: {candidate['interest_score']:.1f}")
        print(f"      Match Explanation: {', '.join(candidate['match_explanation'][:2])}")
        print(f"      Interest Explanation: {', '.join(candidate['interest_explanation'][:2])}")
        print()
    
    # Save results to file
    output_data = {
        "job_description": {
            "role": parsed_jd.role,
            "skills_required": parsed_jd.skills_required,
            "experience_years": parsed_jd.experience_years,
            "domain": parsed_jd.domain
        },
        "rankings": final_rankings[:5]
    }
    
    with open("test_results.json", "w") as f:
        json.dump(output_data, f, indent=2)
    
    print("Results saved to test_results.json")


if __name__ == "__main__":
    main()