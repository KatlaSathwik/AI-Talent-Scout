import React, { useMemo, useState } from 'react';
import ScoreBadge from './ScoreBadge';
import ExplanationList from './ExplanationList';
import useStore from '../store/useStore';

const CandidateCard = ({ candidate, rank }) => {
  const [expanded, setExpanded] = useState(false);
  const {
    shortlistedCandidates,
    rejectedCandidates,
    toggleShortlist,
    toggleReject,
  } = useStore();

  const candidateId = candidate.name;
  const isShortlisted = shortlistedCandidates.includes(candidateId);
  const isRejected = rejectedCandidates.includes(candidateId);

  const summary = useMemo(() => {
    const topMatch = candidate.match_explanation?.[0] || 'Strong profile alignment';
    const topInterest = candidate.interest_explanation?.[0] || 'Shows interest signals';
    return `${topMatch}. ${topInterest}.`;
  }, [candidate]);

  return (
    <div className="card border border-gray-100">
      <div className="p-5 sm:p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <div className="flex items-center gap-2">
              <span className="inline-flex h-7 w-7 items-center justify-center rounded-full bg-gray-100 text-xs font-semibold text-gray-700">
                #{rank}
              </span>
              <h3 className="text-lg font-semibold text-gray-900">{candidate.name}</h3>
            </div>
            <p className="mt-2 text-sm text-gray-600">{summary}</p>
          </div>

          <div className="flex flex-wrap gap-2">
            <ScoreBadge score={Math.round(candidate.match_score)} type="match" />
            <ScoreBadge score={Math.round(candidate.interest_score)} type="interest" />
            <ScoreBadge score={Math.round(candidate.final_score)} type="final" />
          </div>
        </div>

        <div className="mt-4 flex flex-wrap items-center gap-2">
          <button
            className={`btn-secondary ${isShortlisted ? 'ring-2 ring-secondary-300' : ''}`}
            onClick={() => toggleShortlist(candidateId)}
            type="button"
          >
            {isShortlisted ? 'Shortlisted' : 'Shortlist'}
          </button>

          <button
            className={`btn-outline ${isRejected ? 'border-red-300 text-red-700' : ''}`}
            onClick={() => toggleReject(candidateId)}
            type="button"
          >
            {isRejected ? 'Rejected' : 'Reject'}
          </button>

          <button
            className="btn-outline"
            onClick={() => setExpanded((v) => !v)}
            type="button"
          >
            {expanded ? 'Hide Details' : 'View Details'}
          </button>
        </div>

        <div
          className={`grid transition-all duration-300 ${expanded ? 'grid-rows-[1fr] opacity-100 mt-4' : 'grid-rows-[0fr] opacity-0 mt-0'}`}
        >
          <div className="overflow-hidden">
            <div className="rounded-xl bg-gray-50 p-4">
              <ExplanationList title="Match Explanation" explanations={candidate.match_explanation || []} isVisible />
              <ExplanationList title="Interest Explanation" explanations={candidate.interest_explanation || []} isVisible={false} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CandidateCard;

