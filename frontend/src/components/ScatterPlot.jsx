import React, { useMemo } from 'react';
import {
  CartesianGrid,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from 'recharts';
import useStore from '../store/useStore';

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload || !payload.length) return null;
  const c = payload[0].payload;
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-3 shadow-lg">
      <p className="text-sm font-semibold text-gray-900">{c.name}</p>
      <p className="text-xs text-blue-700">Match: {Math.round(c.match_score)}</p>
      <p className="text-xs text-green-700">Interest: {Math.round(c.interest_score)}</p>
      <p className="text-xs text-purple-700">Final: {Math.round(c.final_score)}</p>
    </div>
  );
};

const ScatterPlot = () => {
  const { candidates, minMatchScore, minInterestScore } = useStore();

  const data = useMemo(
    () =>
      (candidates || [])
        .filter((c) => c.match_score >= minMatchScore && c.interest_score >= minInterestScore)
        .map((c) => ({
          ...c,
          x: c.match_score,
          y: c.interest_score,
          z: Math.max(40, c.final_score),
        })),
    [candidates, minMatchScore, minInterestScore],
  );

  return (
    <div className="card p-5 sm:p-6">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">Candidate Score Map</h3>
        <p className="text-xs text-gray-500">X: Match Score · Y: Interest Score</p>
      </div>

      {data.length === 0 ? (
        <div className="flex h-72 items-center justify-center rounded-xl bg-gray-50 text-sm text-gray-500">
          No candidate points to display yet.
        </div>
      ) : (
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 10, right: 10, bottom: 10, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" dataKey="x" name="Match Score" domain={[0, 100]} />
              <YAxis type="number" dataKey="y" name="Interest Score" domain={[0, 100]} />
              <ZAxis type="number" dataKey="z" range={[60, 220]} />
              <Tooltip content={<CustomTooltip />} />
              <Scatter data={data} fill="#7c3aed" />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default ScatterPlot;

