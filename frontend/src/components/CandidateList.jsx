import React, { useMemo } from 'react';
import CandidateCard from './CandidateCard';
import useStore from '../store/useStore';

const CandidateList = () => {
  const {
    candidates,
    sortBy,
    minMatchScore,
    minInterestScore,
    isLoading,
    error,
  } = useStore();

  const visibleCandidates = useMemo(() => {
    const filtered = (candidates || []).filter(
      (c) => c.match_score >= minMatchScore && c.interest_score >= minInterestScore,
    );

    const sorted = [...filtered].sort((a, b) => {
      if (sortBy === 'match_score') return b.match_score - a.match_score;
      if (sortBy === 'interest_score') return b.interest_score - a.interest_score;
      return b.final_score - a.final_score;
    });

    return sorted;
  }, [candidates, sortBy, minMatchScore, minInterestScore]);

  if (isLoading) {
    return (
      <div className="card p-8 text-center">
        <div className="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-gray-200 border-t-primary-600" />
        <p className="mt-3 text-sm text-gray-600">Analyzing candidates...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card p-6">
        <p className="text-sm text-red-600">{error}</p>
      </div>
    );
  }

  if (!candidates || candidates.length === 0) {
    return (
      <div className="card p-10 text-center">
        <h3 className="text-lg font-semibold text-gray-900">No candidates yet</h3>
        <p className="mt-2 text-sm text-gray-600">
          Paste a job description and click analyze to see ranked candidates.
        </p>
      </div>
    );
  }

  if (visibleCandidates.length === 0) {
    return (
      <div className="card p-8 text-center">
        <h3 className="text-lg font-semibold text-gray-900">No candidates match your filters</h3>
        <p className="mt-2 text-sm text-gray-600">Lower the score thresholds to view more profiles.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {visibleCandidates.map((candidate, index) => (
        <CandidateCard
          key={`${candidate.name}-${index}`}
          candidate={candidate}
          rank={index + 1}
        />
      ))}
    </div>
  );
};

export default CandidateList;

