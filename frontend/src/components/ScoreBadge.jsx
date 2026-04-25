import React from 'react';

const ScoreBadge = ({ score, type = 'match', size = 'normal' }) => {
  const getTypeClass = () => {
    switch (type) {
      case 'match':
        return 'score-badge-match';
      case 'interest':
        return 'score-badge-interest';
      case 'final':
        return 'score-badge-final';
      default:
        return 'score-badge-match';
    }
  };

  const getSizeClass = () => {
    switch (size) {
      case 'small':
        return 'text-xs px-2 py-0.5';
      case 'large':
        return 'text-base px-4 py-2';
      default:
        return 'text-sm px-3 py-1';
    }
  };

  const getLabel = () => {
    switch (type) {
      case 'match':
        return 'Match';
      case 'interest':
        return 'Interest';
      case 'final':
        return 'Final';
      default:
        return '';
    }
  };

  return (
    <span className={`score-badge ${getTypeClass()} ${getSizeClass()} flex items-center`}>
      <span className="font-medium">{score}</span>
      <span className="ml-1 opacity-75">{getLabel()}</span>
    </span>
  );
};

export default ScoreBadge;