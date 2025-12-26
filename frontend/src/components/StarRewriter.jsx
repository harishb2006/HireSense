import React, { useState } from 'react';
import { API_BASE_URL } from '../config';

const StarRewriter = ({ jobDescription, resumeContext }) => {
  const [originalBullet, setOriginalBullet] = useState('');
  const [rewriteResult, setRewriteResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRewrite = async () => {
    if (!originalBullet.trim()) {
      setError('Please enter a resume bullet point');
      return;
    }

    if (!jobDescription || !jobDescription.trim()) {
      setError('Job description is required. Please go back and enter it.');
      return;
    }

    setLoading(true);
    setError('');
    setRewriteResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/rewriter/star-rewrite`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          original_bullet: originalBullet,
          job_description: jobDescription,
          resume_context: resumeContext || ''
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setRewriteResult(data);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to rewrite bullet point');
      }
    } catch (err) {
      setError('Failed to connect to server. Please try again.');
      console.error('Rewrite error:', err);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    // Could add a toast notification here
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-2xl p-8 shadow-xl">
        <h2 className="text-3xl font-bold mb-3">✨ STAR Rewriter</h2>
        <p className="text-blue-100 text-lg">
          Transform weak bullet points into impactful achievements using the STAR framework
        </p>
      </div>

      {/* What is STAR Framework */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-md">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">📚 What is the STAR Framework?</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="text-blue-600 font-bold text-sm mb-1">S - Situation</div>
            <div className="text-gray-600 text-xs">Set the context</div>
          </div>
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="text-green-600 font-bold text-sm mb-1">T - Task</div>
            <div className="text-gray-600 text-xs">What needed doing</div>
          </div>
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
            <div className="text-orange-600 font-bold text-sm mb-1">A - Action</div>
            <div className="text-gray-600 text-xs">What YOU did</div>
          </div>
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <div className="text-purple-600 font-bold text-sm mb-1">R - Result</div>
            <div className="text-gray-600 text-xs">Measurable impact</div>
          </div>
        </div>
      </div>

      {/* Input Section */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-md">
        <label className="block text-gray-900 font-semibold mb-3">
          Enter your resume bullet point:
        </label>
        <textarea
          value={originalBullet}
          onChange={(e) => setOriginalBullet(e.target.value)}
          placeholder="Example: Worked on team project to develop new features for the application"
          className="w-full border border-gray-300 rounded-xl p-4 text-gray-800 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all min-h-[120px] resize-none"
        />
        
        {error && (
          <div className="mt-3 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        <button
          onClick={handleRewrite}
          disabled={loading || !originalBullet.trim()}
          className="mt-4 w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold py-3 px-6 rounded-xl hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Rewriting with AI...
            </span>
          ) : (
            '✨ Rewrite with STAR Framework'
          )}
        </button>
      </div>

      {/* Results Section */}
      {rewriteResult && (
        <div className="space-y-6 animate-fadeIn">
          {/* Before & After Comparison */}
          <div className="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-lg">
            <div className="grid md:grid-cols-2 divide-x divide-gray-200">
              {/* Before */}
              <div className="p-6 bg-red-50">
                <div className="flex items-center gap-2 mb-3">
                  <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  <h3 className="font-bold text-gray-900">Before</h3>
                </div>
                <p className="text-gray-700 text-sm leading-relaxed">
                  {rewriteResult.original}
                </p>
                {rewriteResult.improvements?.before_issues && (
                  <div className="mt-4 space-y-2">
                    {rewriteResult.improvements.before_issues.map((issue, idx) => (
                      <div key={idx} className="flex items-start gap-2">
                        <span className="text-red-600 text-xs">❌</span>
                        <span className="text-red-700 text-xs">{issue}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* After */}
              <div className="p-6 bg-green-50">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <h3 className="font-bold text-gray-900">After (STAR Format)</h3>
                  </div>
                  <button
                    onClick={() => copyToClipboard(rewriteResult.rewritten)}
                    className="text-green-600 hover:text-green-700 p-2 hover:bg-green-100 rounded-lg transition-all"
                    title="Copy to clipboard"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                  </button>
                </div>
                <p className="text-gray-800 text-sm leading-relaxed font-medium">
                  {rewriteResult.rewritten}
                </p>
                {rewriteResult.improvements?.after_strengths && (
                  <div className="mt-4 space-y-2">
                    {rewriteResult.improvements.after_strengths.map((strength, idx) => (
                      <div key={idx} className="flex items-start gap-2">
                        <span className="text-green-600 text-xs">✓</span>
                        <span className="text-green-700 text-xs">{strength}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* STAR Breakdown */}
          {rewriteResult.star_breakdown && (
            <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-md">
              <h3 className="font-bold text-gray-900 mb-4 text-lg">🎯 STAR Framework Breakdown</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="border border-blue-200 rounded-lg p-4 bg-blue-50">
                  <div className="font-semibold text-blue-900 mb-2">Situation</div>
                  <div className="text-gray-700 text-sm">{rewriteResult.star_breakdown.situation}</div>
                </div>
                <div className="border border-green-200 rounded-lg p-4 bg-green-50">
                  <div className="font-semibold text-green-900 mb-2">Task</div>
                  <div className="text-gray-700 text-sm">{rewriteResult.star_breakdown.task}</div>
                </div>
                <div className="border border-orange-200 rounded-lg p-4 bg-orange-50">
                  <div className="font-semibold text-orange-900 mb-2">Action</div>
                  <div className="text-gray-700 text-sm">{rewriteResult.star_breakdown.action}</div>
                </div>
                <div className="border border-purple-200 rounded-lg p-4 bg-purple-50">
                  <div className="font-semibold text-purple-900 mb-2">Result</div>
                  <div className="text-gray-700 text-sm">{rewriteResult.star_breakdown.result}</div>
                </div>
              </div>
            </div>
          )}

          {/* Impact Score & Keywords */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* Impact Improvement */}
            {rewriteResult.impact_score_improvement && (
              <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-md">
                <h3 className="font-bold text-gray-900 mb-3">📈 Impact Score Improvement</h3>
                <div className="flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-5xl font-bold text-green-600">
                      +{rewriteResult.impact_score_improvement}%
                    </div>
                    <div className="text-gray-600 text-sm mt-2">Stronger impact & clarity</div>
                  </div>
                </div>
              </div>
            )}

            {/* Keywords Added */}
            {rewriteResult.keywords_added && rewriteResult.keywords_added.length > 0 && (
              <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-md">
                <h3 className="font-bold text-gray-900 mb-3">🔑 Keywords Added</h3>
                <div className="flex flex-wrap gap-2">
                  {rewriteResult.keywords_added.map((keyword, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-indigo-100 text-indigo-700 text-sm font-medium rounded-full"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Action Button */}
          <div className="bg-gradient-to-r from-gray-50 to-gray-100 border border-gray-200 rounded-2xl p-6 text-center">
            <p className="text-gray-700 mb-4">
              Ready to transform another bullet point?
            </p>
            <button
              onClick={() => {
                setOriginalBullet('');
                setRewriteResult(null);
                setError('');
              }}
              className="bg-white text-gray-900 font-semibold py-2 px-6 rounded-xl border-2 border-gray-300 hover:border-gray-400 hover:shadow-md transition-all"
            >
              Rewrite Another Bullet Point
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default StarRewriter;
