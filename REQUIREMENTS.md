# Requirements Specification for AI-Powered Talent Scouting & Engagement Agent

## Overview
This document specifies the functional and technical requirements for building an AI-Powered Talent Scouting & Engagement Agent that can parse job descriptions, find matching candidates, score them, simulate outreach conversations, and return a ranked shortlist.

## Functional Requirements

### 1. Job Description Parser
**Description**: Parse raw job description text into structured data using LLM prompting.

**Inputs**:
- Raw job description text (string)

**Outputs**:
- Structured job data containing:
  - Role title (string)
  - Required skills (array of strings)
  - Optional skills (array of strings)
  - Experience years (integer)
  - Seniority level (string)
  - Domain/industry (string)
  - Additional signals (array of strings)

**Processing Steps**:
1. Receive raw job description text
2. Use LLM with prompt engineering to extract structured information
3. Validate and clean extracted data
4. Return structured job object

### 2. Candidate Dataset
**Description**: Maintain a mock dataset of candidates for matching.

**Structure**:
Each candidate should contain:
- Name (string)
- Skills (array of strings)
- Years of experience (integer)
- Domain/industry (string)
- Past roles (array of strings)
- Activity signals (object with boolean flags)

### 3. Candidate Discovery & Matching
**Description**: Find candidates that match job requirements using embeddings and filtering.

**Process**:
1. Convert job description and candidate profiles to embeddings
2. Use FAISS for similarity search
3. Apply filters:
   - Minimum experience requirement
   - Required skills matching
   - Domain alignment

### 4. Match Scoring
**Description**: Calculate a match score (0-100) for each candidate based on job requirements.

**Scoring Components**:
- Skills match (40% weight)
- Experience alignment (20% weight)
- Domain match (15% weight)
- Seniority level match (15% weight)
- Bonus signals (10% weight)

**Output**:
- Numerical score (0-100)
- Explanation of scoring rationale

### 5. Outreach Simulation
**Description**: Simulate conversational outreach to estimate candidate interest.

**Conversation Flow**:
1. Initial interest inquiry
2. Role alignment questions
3. Availability assessment

**Output Signals**:
- Interested/Not Interested
- Passive/Active candidate
- Engagement level assessment

### 6. Interest Scoring
**Description**: Calculate an interest score (0-100) based on outreach simulation and activity signals.

**Scoring Components**:
- Explicit interest (40% weight)
- Engagement level (20% weight)
- Activity signals (20% weight)
- Responsiveness (20% weight)

### 7. Final Ranking
**Description**: Combine match and interest scores to produce final ranking.

**Algorithm**:
`final_score = 0.6 * match_score + 0.4 * interest_score`

**Output**:
Ranked list of candidates with:
- Name
- Match score
- Interest score
- Final score
- Match explanations
- Interest explanations

## Technical Requirements

### Backend Framework
- Python + FastAPI for API implementation

### LLM Integration
- OpenAI API integration with abstraction layer
- Deterministic responses (low temperature)
- Reusable prompt templates

### Embeddings & Vector Storage
- OpenAI embeddings or sentence-transformers
- FAISS for local vector storage and similarity search

### Data Storage
- SQLite database for MVP

### API Endpoints
- POST /analyze
  - Input: { job_description: string }
  - Output: Ranked list of candidates with scores and explanations

## Non-functional Requirements

### Performance
- Response time under 30 seconds for complete pipeline
- Efficient embedding caching

### Code Quality
- Modular, readable code structure
- Type hints for all functions
- Comprehensive docstrings
- Separation of business logic from API layer

### Testing
- Sample job description for testing
- Verification of full pipeline functionality
- Top 5 candidates output for validation

## Implementation Constraints

### Technology Stack
- Python 3.8+
- FastAPI
- OpenAI API
- FAISS
- SQLite

### Project Structure
Must follow the specified directory structure:
```
/app
  /agents
  /services
  /models
  /data
  main.py
  config.py
```

## Future Enhancements (Out of Scope for MVP)
- Web frontend
- Advanced analytics dashboard
- Real-time candidate engagement
- Multi-language support
- Integration with job boards and professional networks