import axios from 'axios';

// Create axios instance with base URL
const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Mock data for fallback
const mockCandidates = [
  {
    name: "Alex Johnson",
    match_score: 92,
    interest_score: 85,
    final_score: 89,
    match_explanation: [
      "5+ years experience in Python and Django",
      "Worked with PostgreSQL in previous roles",
      "Experience with AWS cloud services",
      "Strong portfolio in web development"
    ],
    interest_explanation: [
      "Recently updated LinkedIn profile",
      "Applied to 3 similar positions this month",
      "Open to remote work opportunities"
    ]
  },
  {
    name: "Maria Garcia",
    match_score: 88,
    interest_score: 75,
    final_score: 83,
    match_explanation: [
      "4+ years experience in Python",
      "Familiar with Django REST Framework",
      "Experience with Docker containers",
      "Contributor to open-source projects"
    ],
    interest_explanation: [
      "Profile indicates job searching",
      "Updated resume 2 weeks ago",
      "Attended virtual tech meetup recently"
    ]
  },
  {
    name: "David Chen",
    match_score: 95,
    interest_score: 60,
    final_score: 81,
    match_explanation: [
      "Senior Python Developer with 7 years experience",
      "Expert in Django and PostgreSQL",
      "AWS Certified Solutions Architect",
      "Led team of 5 developers at previous company"
    ],
    interest_explanation: [
      "Not actively applying but open to opportunities",
      "Prefers onsite positions",
      "Looking for leadership roles"
    ]
  },
  {
    name: "Sarah Williams",
    match_score: 82,
    interest_score: 90,
    final_score: 85,
    match_explanation: [
      "3+ years experience in Python and Django",
      "Experience with PostgreSQL and Redis",
      "Familiar with CI/CD pipelines",
      "Quick learner of new technologies"
    ],
    interest_explanation: [
      "Actively seeking new opportunities",
      "Available for immediate start",
      "Open to contract positions"
    ]
  }
];

// Analyze job description
export const analyzeJobDescription = async (jobDescription) => {
  try {
    const response = await apiClient.post('/analyze', {
      job_description: jobDescription
    });
    
    return response.data.candidates;
  } catch (error) {
    console.error('API Error:', error);
    // Return mock data if API fails
    return mockCandidates;
  }
};

// Health check
export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    return { status: 'unhealthy' };
  }
};

export default {
  analyzeJobDescription,
  healthCheck
};