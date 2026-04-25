"""
Test runner for the AI-Powered Talent Scouting Agent.
Runs all tests to verify the system works correctly.
"""
import sys
import os

def run_unit_tests():
    """Run unit tests for individual components."""
    print("Running unit tests...")
    print("-" * 30)
    
    # Test 1: Config loading
    try:
        from app.config import settings
        print("✓ Config loading")
    except Exception as e:
        print(f"✗ Config loading - {e}")
        return False
    
    # Test 2: Schema validation
    try:
        from app.models.schemas import JobDescription, Candidate
        # Create a test job description
        job_desc = JobDescription(
            role="Software Engineer",
            skills_required=["Python", "Django"],
            skills_optional=["React", "AWS"],
            experience_years=3,
            seniority="Mid-level",
            domain="Tech",
            signals=["Remote work available"]
        )
        print("✓ Schema validation")
    except Exception as e:
        print(f"✗ Schema validation - {e}")
        return False
    
    # Test 3: Candidate service
    try:
        from app.services.candidate_service import CandidateService
        service = CandidateService()
        candidates = service.get_all_candidates()
        assert len(candidates) > 0, "No candidates found"
        print("✓ Candidate service")
    except Exception as e:
        print(f"✗ Candidate service - {e}")
        return False
    
    # Test 4: JD Parser
    try:
        from app.agents.jd_parser import JDParser
        parser = JDParser()
        test_jd = "Looking for a Python developer with 3+ years experience in Django and PostgreSQL"
        parsed = parser.parse(test_jd)
        assert parsed.role, "No role parsed"
        print("✓ JD Parser")
    except Exception as e:
        print(f"✗ JD Parser - {e}")
        return False
    
    print("All unit tests passed!")
    return True

def run_integration_test():
    """Run integration test with the full pipeline."""
    print("\nRunning integration test...")
    print("-" * 30)
    
    try:
        # Import required components
        from app.agents.jd_parser import JDParser
        from app.agents.matcher import CandidateMatcher
        from app.agents.scorer import CandidateScorer
        from app.services.candidate_service import CandidateService
        
        # Sample job description
        job_description = """
        Senior Python Developer needed with 5+ years experience.
        Must have skills in Django, PostgreSQL, and AWS.
        Experience with Docker and Kubernetes is a plus.
        """
        
        # Parse job description
        parser = JDParser()
        parsed_jd = parser.parse(job_description)
        
        # Find matches
        matcher = CandidateMatcher()
        matches = matcher.find_matches(parsed_jd, k=3)
        
        # Score candidates
        scorer = CandidateScorer()
        scored = scorer.score_candidates(matches, parsed_jd)
        
        assert len(scored) > 0, "No candidates scored"
        print("✓ Full pipeline integration")
        
    except Exception as e:
        print(f"✗ Full pipeline integration - {e}")
        return False
    
    print("Integration test passed!")
    return True

def main():
    """Run all tests."""
    print("AI-Powered Talent Scouting Agent - Test Suite")
    print("=" * 50)
    
    if not run_unit_tests():
        sys.exit(1)
    
    if not run_integration_test():
        sys.exit(1)
    
    print("\n🎉 All tests passed! The system is working correctly.")

if __name__ == "__main__":
    main()