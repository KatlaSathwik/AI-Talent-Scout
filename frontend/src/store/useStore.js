import { create } from 'zustand';

const useStore = create((set, get) => ({
  // Job description state
  jobDescription: '',
  setJobDescription: (jobDescription) => set({ jobDescription }),
  
  // Candidates state
  candidates: [],
  setCandidates: (candidates) => set({ candidates }),
  
  // Loading state
  isLoading: false,
  setIsLoading: (isLoading) => set({ isLoading }),
  
  // Error state
  error: null,
  setError: (error) => set({ error }),
  
  // Filters
  sortBy: 'final_score',
  setSortBy: (sortBy) => set({ sortBy }),
  
  minMatchScore: 0,
  setMinMatchScore: (minMatchScore) => set({ minMatchScore }),
  
  minInterestScore: 0,
  setMinInterestScore: (minInterestScore) => set({ minInterestScore }),
  
  // Actions
  shortlistedCandidates: [],
  rejectedCandidates: [],
  
  toggleShortlist: (candidateId) => {
    const { shortlistedCandidates, rejectedCandidates } = get();
    if (shortlistedCandidates.includes(candidateId)) {
      set({
        shortlistedCandidates: shortlistedCandidates.filter(id => id !== candidateId)
      });
    } else {
      set({
        shortlistedCandidates: [...shortlistedCandidates, candidateId],
        rejectedCandidates: rejectedCandidates.filter(id => id !== candidateId)
      });
    }
  },
  
  toggleReject: (candidateId) => {
    const { rejectedCandidates, shortlistedCandidates } = get();
    if (rejectedCandidates.includes(candidateId)) {
      set({
        rejectedCandidates: rejectedCandidates.filter(id => id !== candidateId)
      });
    } else {
      set({
        rejectedCandidates: [...rejectedCandidates, candidateId],
        shortlistedCandidates: shortlistedCandidates.filter(id => id !== candidateId)
      });
    }
  },
  
  // Reset state
  reset: () => set({
    candidates: [],
    error: null,
    shortlistedCandidates: [],
    rejectedCandidates: []
  })
}));

export default useStore;
