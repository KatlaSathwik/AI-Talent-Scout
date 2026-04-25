# AI-Powered Talent Scouting & Engagement Agent - Architecture Plan

## Project Overview

This document outlines the architecture and implementation plan for an AI-Powered Talent Scouting & Engagement Agent. The system will parse job descriptions, match candidates from a dataset, score them based on various criteria, simulate outreach conversations, and return a ranked shortlist.

## Project Structure

```
/app
  /agents
    jd_parser.py          # Parses job descriptions into structured data
    matcher.py            # Matches candidates based on job requirements
    outreach_agent.py     # Simulates conversational outreach to candidates
    scorer.py             # Calculates match and interest scores
  /services
    embedding_service.py  # Handles text embeddings using OpenAI or sentence-transformers
    vector_store.py       # Manages FAISS vector database for similarity search
    candidate_service.py  # Manages candidate data operations
  /models
    schemas.py            # Pydantic models for data validation
  /data
    candidates.json       # Mock candidate dataset
  main.py                 # FastAPI application entry point
  config.py               # Configuration management
```

## Component Architecture

### 1. JD Parser Agent
Responsible for parsing raw job description text into structured data using LLM prompting.

**Input**: Raw job description text
**Output**: Structured data containing:
- Role title
- Required skills (array)
- Optional skills (array)
- Experience requirements (years)
- Seniority level
- Domain/industry
- Additional signals

### 2. Candidate Dataset
A JSON file containing 20-30 mock candidates with fields:
- Name
- Skills (array)
- Years of experience
- Domain/industry
- Past roles (array)
- Activity signals

### 3. Embedding Service
Converts text (job descriptions and candidate profiles) into vector embeddings for similarity comparison.

Options:
- OpenAI embeddings API
- Sentence transformers (local option)

### 4. Vector Store (FAISS)
Performs similarity search between job description embeddings and candidate embeddings to find the best matches.

### 5. Matcher
Applies filtering and matching logic:
- Minimum experience requirements
- Required skills matching
- Domain alignment

### 6. Scorer
Calculates two types of scores:

#### Match Score (0-100)
Weighted components:
- Skills match (40%)
- Experience alignment (20%)
- Domain match (15%)
- Seniority level match (15%)
- Bonus signals (10%)

#### Interest Score (0-100)
Based on:
- Explicit interest signals (40%)
- Engagement level (20%)
- Activity signals (20%)
- Responsiveness (20%)

### 7. Outreach Agent
Simulates 2-3 turn conversations with candidates to gauge interest:
- Initial interest inquiry
- Role alignment questions
- Availability assessment

### 8. Final Ranking Algorithm
Combines match and interest scores:
`final_score = 0.6 * match_score + 0.4 * interest_score`

## API Design

### Endpoint
`POST /analyze`

### Request Body
```json
{
  "job_description": "string"
}
```

### Response
```json
[
  {
    "name": "string",
    "match_score": "number",
    "interest_score": "number",
    "final_score": "number",
    "match_explanation": ["string"],
    "interest_explanation": ["string"]
  }
]
```

## LLM Prompt Design

Reusable prompt templates for:
1. JD parsing - Extract structured information from job descriptions
2. Outreach conversation - Generate natural conversation flows
3. Interest classification - Interpret candidate responses

All prompts will use low temperature for deterministic responses.

## Implementation Roadmap

1. **Project Setup**
   - Create directory structure
   - Set up configuration management
   - Define data models/schemas

2. **Data Layer**
   - Create mock candidate dataset
   - Implement embedding service
   - Set up FAISS vector store

3. **Core Logic**
   - Implement JD parser agent
   - Build matching algorithm
   - Create scoring mechanisms
   - Develop outreach simulation

4. **API Layer**
   - Build FastAPI endpoints
   - Implement request/response handling

5. **Testing & Documentation**
   - Add sample job description
   - Test full pipeline
   - Create requirements.txt
   - Write README documentation

## Optional Enhancements

- Logging system for tracking operations
- Caching mechanism for embeddings
- Simple CLI interface for local testing
- Performance monitoring