import React, { useState } from 'react';

const ExplanationList = ({ title, explanations, isVisible = true }) => {
  const [expanded, setExpanded] = useState(isVisible);

  if (!explanations || explanations.length === 0) {
    return null;
  }

  return (
    <div className="mt-4">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center text-sm font-medium text-gray-700 hover:text-gray-900 focus:outline-none"
      >
        <span>{title}</span>
        <svg 
          className={`ml-2 h-4 w-4 transform transition-transform ${expanded ? 'rotate-180' : ''}`} 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      
      {expanded && (
        <ul className="mt-2 space-y-1">
          {explanations.map((explanation, index) => (
            <li key={index} className="flex items-start">
              <svg className="h-5 w-5 text-green-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              <span className="text-sm text-gray-600">{explanation}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ExplanationList;