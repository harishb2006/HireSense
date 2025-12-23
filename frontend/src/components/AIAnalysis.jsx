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
    <div className="max-w-7xl mx-auto p-6 space-y-8 animate-fade-in">
      {/* Header */}
      <div className="text-center space-y-4 py-12">
        <h1 className="text-5xl font-bold text-white drop-shadow-lg">
          🤖 AI Resume Analysis
        </h1>
        <p className="text-xl text-white/90">
          Get intelligent insights and match scores powered by AI
        </p>
      </div>

      {/* Input Section */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="card space-y-4">
          <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <span>📄</span> Resume Text
          </h2>
          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste your resume text here..."
            className="textarea-field"
            rows="15"
          />
        </div>

        <div className="card space-y-4">
          <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <span>💼</span> Job Description
          </h2>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here..."
            className="textarea-field"
            rows="15"
          />
        </div>
      </div>

      {/* Analyze Button */}
      <div className="flex justify-center">
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="btn-primary text-lg px-12 py-4"
        >
          {loading ? (
            <span className="flex items-center gap-3">
              <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Analyzing...
            </span>
          ) : (
            '🔍 Analyze Resume'
          )}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="card bg-red-50 border-2 border-red-200 animate-slide-up">
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
        <div className="space-y-6 animate-slide-up">
          {/* Match Score */}
          <div className="card bg-gradient-to-br from-primary-50 to-secondary-50">
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
                    stroke="url(#gradient)"
                    strokeWidth="16"
                    fill="none"
                    strokeDasharray={`${2 * Math.PI * 88}`}
                    strokeDashoffset={`${2 * Math.PI * 88 * (1 - analysis.match_score / 100)}`}
                    className="transition-all duration-1000 ease-out"
                  />
                  <defs>
                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#667eea" />
                      <stop offset="100%" stopColor="#764ba2" />
                    </linearGradient>
                  </defs>
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-secondary-600">
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
          <div className="card">
            <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span>🔑</span> Missing Keywords
            </h3>
            <div className="flex flex-wrap gap-3">
              {analysis.missing_keywords.map((keyword, index) => (
                <span
                  key={index}
                  className="px-4 py-2 bg-red-100 text-red-700 rounded-full font-semibold border-2 border-red-200 animate-fade-in"
                  style={{ animationDelay: `${index * 0.1}s` }}
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
  );
}

function FeedbackCard({ title, icon, feedback, color }) {
  const colorClasses = {
    blue: 'from-blue-50 to-blue-100 border-blue-200',
    purple: 'from-purple-50 to-purple-100 border-purple-200',
    pink: 'from-pink-50 to-pink-100 border-pink-200',
  };

  return (
    <div className={`card bg-gradient-to-br ${colorClasses[color]} border-2`}>
      <h4 className="text-xl font-bold text-gray-800 mb-3 flex items-center gap-2">
        <span className="text-2xl">{icon}</span>
        {title}
      </h4>
      <p className="text-gray-700 leading-relaxed">{feedback}</p>
    </div>
  );
}
