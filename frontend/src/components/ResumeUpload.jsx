import { useState } from 'react';
import axios from 'axios';

export default function ResumeUpload({ onResumeExtracted }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a PDF file');
      return;
    }

    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/api/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(response.data);
      if (onResumeExtracted) {
        onResumeExtracted(response.data.resume_text);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card space-y-4">
      <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
        <span>📄</span> Upload Resume (PDF)
      </h2>
      
      <form onSubmit={handleUpload} className="space-y-4">
        <div className="relative">
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
        </div>
        
        <button
          type="submit"
          disabled={loading || !file}
          className="btn-primary w-full"
        >
          {loading ? 'Processing...' : 'Upload & Extract Text'}
        </button>
      </form>

      {error && (
        <div className="p-4 bg-red-50 border-2 border-red-200 rounded-lg">
          <p className="text-red-700 font-medium">❌ {error}</p>
        </div>
      )}

      {result && (
        <div className="p-4 bg-green-50 border-2 border-green-200 rounded-lg space-y-2">
          <p className="text-green-700 font-semibold">✅ Resume Processed Successfully!</p>
          <p className="text-sm text-gray-600"><strong>Filename:</strong> {result.filename}</p>
          <div className="mt-3 p-3 bg-white rounded border border-gray-200 max-h-48 overflow-y-auto">
            <p className="text-xs text-gray-500 mb-2">Preview (first 500 characters):</p>
            <pre className="text-sm text-gray-700 whitespace-pre-wrap">
              {result.resume_text?.substring(0, 500)}...
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
