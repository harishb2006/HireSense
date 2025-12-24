import { useState } from 'react';
import axios from 'axios';

export default function AIAnalysis() {
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    
    if (!resumeText.trim() || !jobDescription.trim()) {
      setError('Please provide both resume text and job description');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('http://localhost:8000/api/analyze', {
        resume_text: resumeText,
        job_description: jobDescription
      });
      setAnalysis(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
      setAnalysis(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-slate-700 text-white py-8 px-10 text-center mb-10 border-b-4 border-slate-800">
        <h1 className="text-4xl font-semibold mb-2 tracking-tight">
          AI Resume Analysis
        </h1>
        <p className="text-lg opacity-90">
          Get intelligent insights and match scores powered by AI
        </p>
      </div>

      <div className="max-w-7xl mx-auto px-6 space-y-8">
        {/* Input Section */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-xl font-semibold flex items-center gap-2 text-slate-700 mb-4">
              <span>📄</span> Resume Text
            </h2>
            <textarea
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Paste your resume text here..."
              className="w-full p-3 border border-gray-300 rounded text-sm resize-y min-h-[250px] focus:outline-none focus:border-slate-700 focus:ring-2 focus:ring-slate-700/10 transition-all"
              rows="15"
            />
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-xl font-semibold flex items-center gap-2 text-slate-700 mb-4">
              <span>💼</span> Job Description
            </h2>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here..."
              className="w-full p-3 border border-gray-300 rounded text-sm resize-y min-h-[250px] focus:outline-none focus:border-slate-700 focus:ring-2 focus:ring-slate-700/10 transition-all"
              rows="15"
            />
          </div>
        </div>

        {/* Analyze Button */}
        <div className="flex justify-center">
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="bg-slate-700 text-white px-8 py-3 rounded font-medium hover:bg-slate-800 active:bg-slate-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-base"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Analyzing...
              </span>
            ) : (
              'Analyze Resume'
            )}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border-2 border-red-200 p-6 rounded-lg shadow-sm">
          <div className="flex items-start gap-3">
              <span className="text-2xl">❌</span>
              <div>
                <h3 className="text-xl font-bold text-red-700">Error</h3>
                <p className="text-red-600">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Analysis Results */}
        {analysis && (
          <div className="space-y-6">
            {/* Match Score */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="text-center space-y-4">
                <h3 className="text-2xl font-bold text-gray-800">Match Score</h3>
                <div className="relative inline-block">
                  <svg className="w-48 h-48 transform -rotate-90">
                    <circle
                      cx="96"
                      cy="96"
                      r="88"
                      stroke="#e5e7eb"
                      strokeWidth="16"
                      fill="none"
                    />
                    <circle
                      cx="96"
                      cy="96"
                      r="88"
                      stroke="#475569"
                      strokeWidth="16"
                      fill="none"
                      strokeDasharray={`${2 * Math.PI * 88}`}
                      strokeDashoffset={`${2 * Math.PI * 88 * (1 - analysis.match_score / 100)}`}
                      className="transition-all duration-1000 ease-out"
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-6xl font-bold text-slate-700">
                      {analysis.match_score}%
                    </span>
                  </div>
                </div>
                <p className="text-gray-600 text-lg">
                  {analysis.match_score >= 80 ? '🎉 Excellent Match!' :
                   analysis.match_score >= 60 ? '👍 Good Match' :
                   analysis.match_score >= 40 ? '⚠️ Fair Match' :
                   '🔴 Needs Improvement'}
                </p>
              </div>
            </div>

            {/* Missing Keywords */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <span>🔑</span> Missing Keywords
              </h3>
              <div className="flex flex-wrap gap-3">
                {analysis.missing_keywords.map((keyword, index) => (
                  <span
                    key={index}
                    className="px-4 py-2 bg-red-100 text-red-700 rounded-full font-semibold border-2 border-red-200"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>

            {/* Section Feedback */}
            <div className="grid md:grid-cols-3 gap-6">
              <FeedbackCard
                title="Summary"
                icon="📝"
                feedback={analysis.section_feedback.Summary}
                color="blue"
              />
              <FeedbackCard
                title="Experience"
                icon="💼"
                feedback={analysis.section_feedback.Experience}
                color="purple"
              />
              <FeedbackCard
                title="Skills"
                icon="⚡"
                feedback={analysis.section_feedback.Skills}
                color="pink"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function FeedbackCard({ title, icon, feedback, color }) {
  const colorClasses = {
    blue: 'bg-blue-50 border-blue-200',
    purple: 'bg-purple-50 border-purple-200',
    pink: 'bg-pink-50 border-pink-200',
  };

  return (
    <div className={`${colorClasses[color]} border-2 p-6 rounded-lg shadow-sm`}>
      <p className="text-gray-700 leading-relaxed">{feedback}</p>
    </div>
  );
}
