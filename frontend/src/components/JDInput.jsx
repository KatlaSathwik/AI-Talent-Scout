import React, { useState } from 'react';
import useStore from '../store/useStore';
import { analyzeJobDescription } from '../services/api';

const JDInput = () => {
  const { jobDescription, setJobDescription, setIsLoading, setError, setCandidates, reset } = useStore();
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!jobDescription.trim()) return;
    
    setIsAnalyzing(true);
    setIsLoading(true);
    setError(null);
    reset(); // Clear previous results
    
    try {
      const candidates = await analyzeJobDescription(jobDescription);
      setCandidates(candidates);
    } catch (err) {
      setError('Failed to analyze job description. Please try again.');
      console.error(err);
    } finally {
      setIsAnalyzing(false);
      setIsLoading(false);
    }
  };

  return (
    <div className="card mb-8">
      <div className="px-6 py-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Job Description</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste Job Description..."
              className="input-field h-48 resize-none"
              disabled={isAnalyzing}
            />
          </div>
          <div className="flex justify-between items-center">
            <button
              type="submit"
              className="btn-primary flex items-center"
              disabled={isAnalyzing || !jobDescription.trim()}
            >
              {isAnalyzing ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing...
                </>
              ) : 'Analyze Candidates'}
            </button>

            {jobDescription && (
              <button
                type="button"
                onClick={() => {
                  setJobDescription('');
                  reset();
                }}
                className="btn-outline"
              >
                Clear
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};

export default JDInput;
