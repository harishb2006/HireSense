import { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a PDF file');
      return;
    }

    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Step 1: Upload PDF and extract text
      const uploadResponse = await axios.post('http://localhost:8000/api/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      const resumeText = uploadResponse.data.resume_text;
      
      // Step 2: Analyze resume against job description
      const analysisResponse = await axios.post('http://localhost:8000/api/analyze', {
        resume_text: resumeText,
        job_description: jobDescription
      });
      
      setResult({
        type: 'analysis',
        filename: uploadResponse.data.filename,
        resumeText: resumeText,
        jobDescription: jobDescription,
        analysis: analysisResponse.data
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Processing failed. Please try again.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="bg-white/10 backdrop-blur-lg border-b border-white/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center shadow-lg">
              <span className="text-2xl">🎯</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">HireSense</h1>
              <p className="text-sm text-white/80">AI-Powered Resume Analysis</p>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="py-8">
        <div className="max-w-4xl mx-auto px-6">
          <div className="text-center space-y-4 py-8">
            <h2 className="text-4xl font-bold text-white drop-shadow-lg">
              📤 Resume Analyzer
            </h2>
            <p className="text-lg text-white/90">
              Upload your resume PDF and enter the job description
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* PDF Upload */}
            <div className="card space-y-4">
              <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                <span>📄</span> Resume PDF
              </h3>
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => {
                  setFile(e.target.files[0]);
                  setError(null);
                  setResult(null);
                }}
                className="block w-full text-sm text-gray-600
                  file:mr-4 file:py-3 file:px-6
                  file:rounded-lg file:border-0
                  file:text-sm file:font-semibold
                  file:bg-gradient-to-r file:from-primary-500 file:to-secondary-500
                  file:text-white hover:file:opacity-90
                  file:cursor-pointer cursor-pointer
                  border-2 border-dashed border-primary-300 rounded-lg p-4
                  hover:border-primary-500 transition-colors"
              />
              {file && (
                <p className="text-sm text-gray-600">
                  Selected: <span className="font-semibold">{file.name}</span>
                </p>
              )}
            </div>

            {/* Job Description */}
            <div className="card space-y-4">
              <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                <span>💼</span> Job Description
              </h3>
              <textarea
                value={jobDescription}
                onChange={(e) => {
                  setJobDescription(e.target.value);
                  setError(null);
                  setResult(null);
                }}
                placeholder="Paste the job description here..."
                className="textarea-field"
                rows="12"
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || !file || !jobDescription.trim()}
              className="btn-primary w-full text-lg py-4"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-3">
                  <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Processing...
                </span>
              ) : (
                '🔍 Process Resume'
              )}
            </button>
          </form>

          {/* Error Message */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 border-2 border-red-200 rounded-lg">
              <p className="text-red-700 font-medium">❌ {error}</p>
            </div>
          )}

          {/* AI Analysis Result */}
          {result && result.type === 'analysis' && result.analysis && (
            <div className="mt-8 space-y-6 animate-fade-in">
              {/* Match Score - Hero Section */}
              <div className="card bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-indigo-200">
                <div className="text-center space-y-4">
                  <h3 className="text-3xl font-bold text-gray-800">ATS Match Score</h3>
                  <div className="flex items-center justify-center">
                    <div className="relative w-32 h-32">
                      <svg className="transform -rotate-90 w-32 h-32">
                        <circle cx="64" cy="64" r="56" stroke="#e5e7eb" strokeWidth="8" fill="none" />
                        <circle 
                          cx="64" 
                          cy="64" 
                          r="56" 
                          stroke={result.analysis.match_score >= 70 ? "#10b981" : result.analysis.match_score >= 50 ? "#f59e0b" : "#ef4444"}
                          strokeWidth="8" 
                          fill="none"
                          strokeDasharray={`${2 * Math.PI * 56}`}
                          strokeDashoffset={`${2 * Math.PI * 56 * (1 - result.analysis.match_score / 100)}`}
                          strokeLinecap="round"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-4xl font-bold text-gray-800">{result.analysis.match_score}%</span>
                      </div>
                    </div>
                  </div>
                  <p className="text-lg text-gray-700 max-w-3xl mx-auto">
                    {result.analysis.overall_assessment}
                  </p>
                </div>
              </div>

              {/* Why Not Passing Section */}
              <div className="card bg-red-50 border-2 border-red-300">
                <h3 className="text-2xl font-bold text-red-800 mb-4 flex items-center gap-2">
                  <span>🚫</span> Why This Resume Isn't Passing
                </h3>
                
                <div className="space-y-4">
                  <div>
                    <h4 className="font-bold text-gray-800 mb-2">Main Reasons:</h4>
                    <ul className="space-y-2">
                      {result.analysis.why_not_passing?.main_reasons?.map((reason, idx) => (
                        <li key={idx} className="flex gap-3">
                          <span className="text-red-600 font-bold">•</span>
                          <span className="text-gray-700">{reason}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  <div className="mt-4 p-4 bg-white rounded-lg border border-red-200">
                    <h4 className="font-bold text-gray-800 mb-2">🤖 ATS Perspective:</h4>
                    <p className="text-gray-700 leading-relaxed">
                      {result.analysis.why_not_passing?.ats_perspective}
                    </p>
                  </div>
                </div>
              </div>

              {/* Missing Keywords */}
              <div className="card bg-orange-50 border-2 border-orange-300">
                <h3 className="text-2xl font-bold text-orange-800 mb-4 flex items-center gap-2">
                  <span>🔑</span> Critical Missing Keywords
                </h3>
                
                <div className="space-y-4">
                  {result.analysis.missing_keywords?.map((item, idx) => (
                    <div key={idx} className="p-4 bg-white rounded-lg border border-orange-200">
                      <div className="flex items-start justify-between gap-4 mb-2">
                        <h4 className="font-bold text-lg text-gray-800">{item.keyword}</h4>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          item.importance === 'critical' ? 'bg-red-200 text-red-800' :
                          item.importance === 'high' ? 'bg-orange-200 text-orange-800' :
                          'bg-yellow-200 text-yellow-800'
                        }`}>
                          {item.importance?.toUpperCase()}
                        </span>
                      </div>
                      <p className="text-gray-700 leading-relaxed">
                        <span className="font-semibold">Why it matters:</span> {item.why_matters}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Gap Analysis */}
              <div className="card bg-yellow-50 border-2 border-yellow-300">
                <h3 className="text-2xl font-bold text-yellow-800 mb-4 flex items-center gap-2">
                  <span>📊</span> Detailed Gap Analysis
                </h3>
                
                <div className="space-y-4">
                  <div className="p-4 bg-white rounded-lg border border-yellow-200">
                    <h4 className="font-bold text-gray-800 mb-2">💼 Experience Gaps:</h4>
                    <p className="text-gray-700 leading-relaxed">
                      {result.analysis.gap_analysis?.experience_gaps}
                    </p>
                  </div>
                  
                  <div className="p-4 bg-white rounded-lg border border-yellow-200">
                    <h4 className="font-bold text-gray-800 mb-2">🛠️ Skills Gaps:</h4>
                    <p className="text-gray-700 leading-relaxed">
                      {result.analysis.gap_analysis?.skills_gaps}
                    </p>
                  </div>
                  
                  <div className="p-4 bg-white rounded-lg border border-yellow-200">
                    <h4 className="font-bold text-gray-800 mb-2">🎓 Qualification Gaps:</h4>
                    <p className="text-gray-700 leading-relaxed">
                      {result.analysis.gap_analysis?.qualification_gaps}
                    </p>
                  </div>
                </div>
              </div>

              {/* Section Detailed Feedback */}
              <div className="card bg-purple-50 border-2 border-purple-300">
                <h3 className="text-2xl font-bold text-purple-800 mb-4 flex items-center gap-2">
                  <span>📝</span> Section-by-Section Breakdown
                </h3>
                
                <div className="space-y-4">
                  {['summary', 'experience', 'skills'].map((section) => {
                    const feedback = result.analysis.section_detailed_feedback?.[section];
                    if (!feedback) return null;
                    
                    return (
                      <div key={section} className="p-4 bg-white rounded-lg border border-purple-200">
                        <h4 className="font-bold text-lg text-gray-800 mb-3 capitalize">
                          {section === 'summary' ? '📋' : section === 'experience' ? '💼' : '🛠️'} {section}
                        </h4>
                        
                        <div className="space-y-3">
                          <div>
                            <span className="font-semibold text-gray-700">Current State:</span>
                            <p className="text-gray-600 ml-4">{feedback.current_state}</p>
                          </div>
                          
                          <div>
                            <span className="font-semibold text-red-700">Problem:</span>
                            <p className="text-gray-600 ml-4">{feedback.problem}</p>
                          </div>
                          
                          <div>
                            <span className="font-semibold text-orange-700">Impact:</span>
                            <p className="text-gray-600 ml-4">{feedback.impact}</p>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Actionable Next Steps */}
              <div className="card bg-green-50 border-2 border-green-300">
                <h3 className="text-2xl font-bold text-green-800 mb-4 flex items-center gap-2">
                  <span>✅</span> Your Action Plan
                </h3>
                
                <div className="space-y-3">
                  {result.analysis.actionable_next_steps?.map((step, idx) => (
                    <div key={idx} className="flex gap-4 p-4 bg-white rounded-lg border border-green-200">
                      <div className="flex-shrink-0 w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center font-bold">
                        {idx + 1}
                      </div>
                      <p className="text-gray-700 leading-relaxed flex-1">{step}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Download/Save Section */}
              <div className="card bg-gray-50 border-2 border-gray-300 text-center">
                <p className="text-gray-700 mb-4">
                  💡 <strong>Pro Tip:</strong> Save this analysis and work through each action step systematically. Focus on the "critical" and "high" importance items first.
                </p>
                <button 
                  onClick={() => {
                    const dataStr = JSON.stringify(result.analysis, null, 2);
                    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
                    const exportFileDefaultName = 'resume_analysis.json';
                    const linkElement = document.createElement('a');
                    linkElement.setAttribute('href', dataUri);
                    linkElement.setAttribute('download', exportFileDefaultName);
                    linkElement.click();
                  }}
                  className="btn-primary"
                >
                  📥 Download Full Analysis (JSON)
                </button>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-20 py-8 text-center text-white/70">
        <p>© 2025 HireSense - AI-Powered Resume Analysis</p>
        <p className="text-sm mt-2">Built with React, FastAPI & Tailwind CSS</p>
      </footer>
    </div>
  );
}

export default App;
