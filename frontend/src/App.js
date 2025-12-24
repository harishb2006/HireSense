import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [resumeResult, setResumeResult] = useState(null);
  const [jdResult, setJdResult] = useState(null);
  const [loading, setLoading] = useState({ resume: false, jd: false });

  const handleResumeUpload = async (e) => {
    e.preventDefault();
    if (!resumeFile) {
      alert('Please select a PDF file');
      return;
    }

    setLoading({ ...loading, resume: true });
    const formData = new FormData();
    formData.append('file', resumeFile);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/resume/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResumeResult(response.data);
    } catch (error) {
      setResumeResult({ error: error.response?.data?.detail || error.message });
    } finally {
      setLoading({ ...loading, resume: false });
    }
  };

  const handleJDSubmit = async (e) => {
    e.preventDefault();
    if (!jobDescription.trim()) {
      alert('Please enter a job description');
      return;
    }

    setLoading({ ...loading, jd: true });
    try {
      const response = await axios.post(`${API_BASE_URL}/api/jd/submit`, {
        job_description: jobDescription
      });
      setJdResult(response.data);
    } catch (error) {
      setJdResult({ error: error.response?.data?.detail || error.message });
    } finally {
      setLoading({ ...loading, jd: false });
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-slate-700 text-white py-8 px-10 text-center mb-10 border-b-4 border-slate-800">
        <h1 className="text-4xl font-semibold mb-2 tracking-tight">HireSense</h1>
        <p className="text-lg opacity-90">AI-Powered Resume & Job Description Analysis</p>
      </header>

      <div className="max-w-7xl mx-auto px-5 grid md:grid-cols-2 gap-8">
        <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-slate-700 mb-5 text-2xl font-semibold">📄 Upload Resume</h2>
          <form onSubmit={handleResumeUpload} className="flex flex-col gap-4">
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setResumeFile(e.target.files[0])}
              className="p-3 border-2 border-dashed border-gray-300 rounded bg-gray-50 cursor-pointer text-sm hover:border-slate-700 hover:bg-white transition-colors"
            />
            <button 
              type="submit" 
              disabled={loading.resume}
              className="bg-slate-700 text-white px-6 py-3 rounded font-medium hover:bg-slate-800 active:bg-slate-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading.resume ? 'Processing...' : 'Upload Resume'}
            </button>
          </form>
          {resumeResult && (
            <div className={`mt-5 p-5 rounded-lg ${resumeResult.error ? 'bg-red-50 border-2 border-red-200 text-red-800' : 'bg-green-50 border-2 border-green-200 text-green-800'}`}>
              {resumeResult.error ? (
                <p>❌ {resumeResult.error}</p>
              ) : (
                <>
                  <h3 className="mb-4 text-xl font-semibold">✅ Resume Processed!</h3>
                  <p><strong>Filename:</strong> {resumeResult.filename}</p>
                  <div className="mt-4">
                    <strong>Extracted Text:</strong>
                    <pre className="bg-black/5 p-4 rounded mt-2 whitespace-pre-wrap break-words text-sm max-h-72 overflow-y-auto">{resumeResult.resume_text?.substring(0, 500)}...</pre>
                  </div>
                </>
              )}
            </div>
          )}
        </div>

        <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-slate-700 mb-5 text-2xl font-semibold">💼 Submit Job Description</h2>
          <form onSubmit={handleJDSubmit} className="flex flex-col gap-4">
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste job description here..."
              rows="10"
              className="p-3 border border-gray-300 rounded text-sm resize-y focus:outline-none focus:border-slate-700 focus:ring-2 focus:ring-slate-700/10 transition-all"
            />
            <button 
              type="submit" 
              disabled={loading.jd}
              className="bg-slate-700 text-white px-6 py-3 rounded font-medium hover:bg-slate-800 active:bg-slate-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading.jd ? 'Processing...' : 'Submit JD'}
            </button>
          </form>
          {jdResult && (
            <div className={`mt-5 p-5 rounded-lg ${jdResult.error ? 'bg-red-50 border-2 border-red-200 text-red-800' : 'bg-green-50 border-2 border-green-200 text-green-800'}`}>
              {jdResult.error ? (
                <p>❌ {jdResult.error}</p>
              ) : (
                <>
                  <h3 className="mb-4 text-xl font-semibold">✅ Job Description Processed!</h3>
                  <div className="mt-4">
                    <strong>Cleaned Text:</strong>
                    <pre className="bg-black/5 p-4 rounded mt-2 whitespace-pre-wrap break-words text-sm max-h-72 overflow-y-auto">{jdResult.cleaned_job_description}</pre>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
