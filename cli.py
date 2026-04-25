"""
CLI interface for the AI-Powered Talent Scouting Agent.
Allows running the pipeline from the command line.
"""
import argparse
import sys
import json

from app.agents.jd_parser import JDParser
from app.agents.matcher import CandidateMatcher
from app.agents.scorer import CandidateScorer
from app.agents.outreach_agent import OutreachAgent
from app.services.candidate_service import CandidateService


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="AI-Powered Talent Scouting Agent")
    parser.add_argument("--job-description", "-j", type=str, 
                        help="Path to job description file")
    parser.add_argument("--output", "-o", type=str, default="results.json",
                        help="Output file for results (default: results.json)")
    parser.add_argument("--top", "-t", type=int, default=5,
                        help="Number of top candidates to return (default: 5)")
    
    args = parser.parse_args()
    
    # Read job description
    if args.job_description:
        try:
            with open(args.job_description, 'r') as f:
                job_description_text = f.read()
        except FileNotFoundError:
            print(f"Error: Job description file '{args.job_description}' not found.")
            sys.exit(1)
    else:
        print("Error: Please provide a job description file using --job-description")
        sys.exit(1)
    
    print("AI-Powered Talent Scouting Agent")
    print("=" * 40)
    print(f"Processing job description: {args.job_description}")
    print()
    
    # Parse job description
    print("1. Parsing job description...")
    jd_parser = JDParser()
    parsed_jd = jd_parser.parse(job_description_text)
    print(f"   Role: {parsed_jd.role}")
    print(f"   Experience required: {parsed_jd.experience_years} years")
    print(f"   Domain: {parsed_jd.domain}")
    print()
    
    # Find matching candidates
    print("2. Finding matching candidates...")
    matcher = CandidateMatcher()
    matched_candidates = matcher.find_matches(parsed_jd, k=args.top * 2)  # Get more candidates for scoring
    print(f"   Found {len(matched_candidates)} potential matches")
    print()
    
    # Score candidates
    print("3. Scoring candidates...")
    scorer = CandidateScorer()
    scored_candidates = scorer.score_candidates(matched_candidates, parsed_jd)
    print(f"   Scored {len(scored_candidates)} candidates")
    print()
    
    # Assess interest
    print("4. Assessing candidate interest...")
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
            "match_score": round(match_result.match_score, 1),
            "interest_score": round(interest_assessment.interest_score, 1),
            "final_score": round(final_score, 1),
            "match_explanation": match_result.match_explanation,
            "interest_explanation": interest_assessment.interest_explanation
        })
    
    # Sort by final score (descending)
    final_rankings.sort(key=lambda x: x["final_score"], reverse=True)
    
    # Display top candidates
    print(f"5. Top {args.top} Candidates:")
    print("-" * 30)
    for i, candidate in enumerate(final_rankings[:args.top], 1):
        print(f"   {i}. {candidate['name']}")
        print(f"      Final Score: {candidate['final_score']}")
        print(f"      Match Score: {candidate['match_score']}")
        print(f"      Interest Score: {candidate['interest_score']}")
        print()
    
    # Save results
    output_data = {
        "job_description": {
            "role": parsed_jd.role,
            "skills_required": parsed_jd.skills_required,
            "experience_years": parsed_jd.experience_years,
            "domain": parsed_jd.domain
        },
        "rankings": final_rankings[:args.top]
    }
    
    with open(args.output, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()