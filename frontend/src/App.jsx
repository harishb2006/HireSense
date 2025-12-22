import { useState } from 'react';
import './App.css';
import axios from 'axios';

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
      const response = await axios.post('/api/resume/upload', formData, {
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
      const response = await axios.post('/api/jd/submit', {
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
    <div className="App">
      <header className="App-header">
        <h1>HireSense</h1>
        <p>AI-Powered Resume & Job Description Analysis</p>
      </header>

      <div className="container">
        <div className="section">
          <h2>📄 Upload Resume</h2>
          <form onSubmit={handleResumeUpload}>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setResumeFile(e.target.files[0])}
              className="file-input"
            />
            <button type="submit" disabled={loading.resume}>
              {loading.resume ? 'Processing...' : 'Upload Resume'}
            </button>
          </form>
          {resumeResult && (
            <div className={`result ${resumeResult.error ? 'error' : 'success'}`}>
              {resumeResult.error ? (
                <p>❌ {resumeResult.error}</p>
              ) : (
                <>
                  <h3>✅ Resume Processed!</h3>
                  <p><strong>Filename:</strong> {resumeResult.filename}</p>
                  <div className="text-preview">
                    <strong>Extracted Text:</strong>
                    <pre>{resumeResult.resume_text?.substring(0, 500)}...</pre>
                  </div>
                </>
              )}
            </div>
          )}
        </div>

        <div className="section">
          <h2>💼 Submit Job Description</h2>
          <form onSubmit={handleJDSubmit}>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste job description here..."
              rows="10"
            />
            <button type="submit" disabled={loading.jd}>
              {loading.jd ? 'Processing...' : 'Submit JD'}
            </button>
          </form>
          {jdResult && (
            <div className={`result ${jdResult.error ? 'error' : 'success'}`}>
              {jdResult.error ? (
                <p>❌ {jdResult.error}</p>
              ) : (
                <>
                  <h3>✅ Job Description Processed!</h3>
                  <div className="text-preview">
                    <strong>Cleaned Text:</strong>
                    <pre>{jdResult.cleaned_job_description}</pre>
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
