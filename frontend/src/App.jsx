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
      // Upload PDF and extract text
      const uploadResponse = await axios.post('http://localhost:8000/api/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setResult({
        type: 'success',
        filename: uploadResponse.data.filename,
        resumeText: uploadResponse.data.resume_text,
        jobDescription: jobDescription
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
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

          {/* Success Result */}
          {result && result.type === 'success' && (
            <div className="mt-6 space-y-4">
              <div className="card bg-green-50 border-2 border-green-200">
                <p className="text-green-700 font-semibold text-lg">✅ Resume Processed Successfully!</p>
                <p className="text-sm text-gray-600 mt-2">
                  <strong>Filename:</strong> {result.filename}
                </p>
              </div>

              <div className="card space-y-3">
                <h4 className="font-bold text-gray-800">📄 Extracted Resume Text:</h4>
                <div className="p-4 bg-gray-50 rounded border border-gray-200 max-h-64 overflow-y-auto">
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                    {result.resumeText}
                  </pre>
                </div>
              </div>

              <div className="card space-y-3">
                <h4 className="font-bold text-gray-800">💼 Job Description:</h4>
                <div className="p-4 bg-gray-50 rounded border border-gray-200 max-h-64 overflow-y-auto">
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                    {result.jobDescription}
                  </pre>
                </div>
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
