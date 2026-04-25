"""
Installation test script for the AI-Powered Talent Scouting Agent.
Verifies that all required packages are installed correctly.
"""
import sys
import importlib

def test_imports():
    """Test that all required packages can be imported."""
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'pydantic_settings',
        'google.genai',
        'sentence_transformers',
        'numpy',
        'faiss',
        'json',
        'os',
        'hashlib',
        'argparse'
    ]
    
    print("Testing package imports...")
    print("-" * 30)
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package}")
        except ImportError as e:
            print(f"✗ {package} - {e}")
            failed_imports.append(package)
    
    print()
    if failed_imports:
        print(f"Failed to import {len(failed_imports)} packages:")
        for pkg in failed_imports:
            print(f"  - {pkg}")
        print("\nPlease install the missing packages using:")
        print("pip install -r requirements.txt")
        return False
    else:
        print("All packages imported successfully!")
        return True

def test_services():
    """Test that our services can be instantiated."""
    print("\nTesting service instantiation...")
    print("-" * 30)
    
    try:
        from app.services.embedding_service import EmbeddingService
        embedding_service = EmbeddingService()
        print("✓ EmbeddingService")
    except Exception as e:
        print(f"✗ EmbeddingService - {e}")
        return False
    
    try:
        from app.services.candidate_service import CandidateService
        candidate_service = CandidateService()
        print("✓ CandidateService")
    except Exception as e:
        print(f"✗ CandidateService - {e}")
        return False
    
    try:
        from app.agents.jd_parser import JDParser
        parser = JDParser()
        print("✓ JDParser")
    except Exception as e:
        print(f"✗ JDParser - {e}")
        return False
    
    print("All services instantiated successfully!")
    return True

def main():
    """Run all installation tests."""
    print("AI-Powered Talent Scouting Agent - Installation Test")
    print("=" * 50)
    
    if not test_imports():
        sys.exit(1)
    
    if not test_services():
        sys.exit(1)
    
    print("\n🎉 Installation test passed! You're ready to use the Talent Scouting Agent.")

if __name__ == "__main__":
    main()
