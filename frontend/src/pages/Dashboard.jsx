import React from 'react';
import JDInput from '../components/JDInput';
import CandidateList from '../components/CandidateList';
import ScatterPlot from '../components/ScatterPlot';
import useStore from '../store/useStore';

const Dashboard = () => {
  const {
    sortBy,
    setSortBy,
    minMatchScore,
    setMinMatchScore,
    minInterestScore,
    setMinInterestScore,
    candidates,
  } = useStore();

  return (
    <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <JDInput />

      <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-3">
        <div className="card p-4">
          <label className="mb-2 block text-sm font-medium text-gray-700">Sort By</label>
          <select
            className="input-field"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
          >
            <option value="final_score">Final Score</option>
            <option value="match_score">Match Score</option>
            <option value="interest_score">Interest Score</option>
          </select>
        </div>

        <div className="card p-4">
          <div className="mb-2 flex items-center justify-between">
            <label className="text-sm font-medium text-gray-700">Min Match Score</label>
            <span className="text-sm text-blue-700">{minMatchScore}</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            step="1"
            value={minMatchScore}
            onChange={(e) => setMinMatchScore(Number(e.target.value))}
            className="w-full"
          />
        </div>

        <div className="card p-4">
          <div className="mb-2 flex items-center justify-between">
            <label className="text-sm font-medium text-gray-700">Min Interest Score</label>
            <span className="text-sm text-green-700">{minInterestScore}</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            step="1"
            value={minInterestScore}
            onChange={(e) => setMinInterestScore(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <div className="mb-6">
        <ScatterPlot />
      </div>

      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-900">Ranked Candidates</h2>
        <span className="text-sm text-gray-500">{candidates?.length || 0} total</span>
      </div>
      <CandidateList />
    </div>
  );
};

export default Dashboard;

