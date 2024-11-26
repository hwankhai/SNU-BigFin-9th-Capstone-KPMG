import React, { useState } from 'react';
import { ExclamationTriangleIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';

interface EvaluationResult {
  has_hallucination: boolean;
  explanation: string;
  details: {
    phase1_result: string;
    judgment_result: string | null;
  };
}

export const HallucinationEvaluator: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [knowledge, setKnowledge] = useState('');
  const [answer, setAnswer] = useState('');
  const [result, setResult] = useState<EvaluationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const response = await fetch('http://localhost:8000/evaluate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        mode: 'cors',
        credentials: 'omit',
        body: JSON.stringify({
          question,
          knowledge,
          answer,
        }),
      });
      
      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`Server error: ${errorData}`);
      }
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
      setError(error instanceof Error ? error.message : 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-6 md:p-10">
      <div className="max-w-4xl mx-auto glass-panel p-8 space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-semibold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            KnowHalu Evaluator
          </h1>
          <p className="text-gray-500">Evaluate AI responses for hallucinations</p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              Question
            </label>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="apple-input"
              rows={2}
              placeholder="Enter your question here..."
              required
            />
          </div>
          
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              Knowledge Base
            </label>
            <textarea
              value={knowledge}
              onChange={(e) => setKnowledge(e.target.value)}
              className="apple-input"
              rows={4}
              placeholder="Enter the reference knowledge here..."
              required
            />
          </div>
          
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              Answer
            </label>
            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              className="apple-input"
              rows={3}
              placeholder="Enter the answer to evaluate..."
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="apple-button"
          >
            {loading ? 'Evaluating...' : 'Evaluate Response'}
          </button>
        </form>

        {error && (
          <div className="result-card bg-red-50 space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-full bg-red-100">
                <XCircleIcon className="w-6 h-6 text-red-500" />
              </div>
              <h2 className="text-xl font-semibold text-red-500">Error</h2>
            </div>
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {result && (
          <div className="result-card space-y-6">
            <div className="flex items-center gap-3">
              {result.has_hallucination ? (
                <>
                  <div className="p-2 rounded-full bg-red-100">
                    <ExclamationTriangleIcon className="w-6 h-6 text-red-500" />
                  </div>
                  <h2 className="text-xl font-semibold text-red-500">Hallucination Detected</h2>
                </>
              ) : (
                <>
                  <div className="p-2 rounded-full bg-green-100">
                    <CheckCircleIcon className="w-6 h-6 text-green-500" />
                  </div>
                  <h2 className="text-xl font-semibold text-green-500">No Hallucination Detected</h2>
                </>
              )}
            </div>
            
            <div className="space-y-2">
              <h3 className="text-lg font-medium text-gray-900">Analysis</h3>
              <p className="text-gray-600 leading-relaxed">{result.explanation}</p>
            </div>
            
            {result.has_hallucination && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <h3 className="text-lg font-medium text-gray-900">Phase 1 Result</h3>
                  <p className="text-gray-600 leading-relaxed">{result.details.phase1_result}</p>
                </div>
                
                {result.details.judgment_result && (
                  <div className="space-y-2">
                    <h3 className="text-lg font-medium text-gray-900">Judgment Result</h3>
                    <p className="text-gray-600 leading-relaxed">{result.details.judgment_result}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
