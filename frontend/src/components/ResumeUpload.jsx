import React, { useState } from 'react';
import { API_BASE_URL } from '../config';

const ResumeUpload = ({ onAnalysisComplete }) => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setResumeFile(file);
      setError('');
    } else {
      setError('Please upload a PDF file');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!resumeFile) {
      setError('Please upload a resume');
      return;
    }

    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', resumeFile);
    formData.append('job_description', jobDescription);

    try {
      // Use the start-interview endpoint which does everything
      const response = await fetch(`${API_BASE_URL}/api/interview/start-interview`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      onAnalysisComplete({
        ...data,
        jobDescription: jobDescription
      });
    } catch (err) {
      setError('Failed to analyze resume. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Resume Upload Card */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-blue-300 transition-all">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center">
            <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="text-gray-900 font-semibold text-lg">Resume PDF</h3>
        </div>

        <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-400 hover:bg-blue-50/50 transition-all">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="hidden"
            id="resume-upload"
          />
          <label htmlFor="resume-upload" className="cursor-pointer flex flex-col items-center">
            {resumeFile ? (
              <div className="text-green-600">
                <svg className="w-16 h-16 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-gray-900 font-medium text-lg mb-1">{resumeFile.name}</p>
                <p className="text-gray-600 text-sm">Click to change file</p>
              </div>
            ) : (
              <>
                <svg className="w-16 h-16 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <p className="text-gray-900 font-medium mb-1">Drop your resume here</p>
                <p className="text-gray-600 text-sm">or click to browse • PDF only</p>
              </>
            )}
          </label>
        </div>

        {resumeFile && (
          <div className="mt-4 flex items-center gap-2 text-sm">
            <span className="text-gray-600">Selected:</span>
            <span className="text-blue-600 font-medium">{resumeFile.name}</span>
          </div>
        )}
      </div>

      {/* Job Description Card */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-indigo-300 transition-all">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-indigo-50 flex items-center justify-center">
            <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="text-gray-900 font-semibold text-lg">Job Description</h3>
        </div>

        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the job description here...&#x0a;&#x0a;Include:&#x0a;• Required skills and qualifications&#x0a;• Job responsibilities&#x0a;• Company information"
          className="w-full h-[280px] px-4 py-3 bg-gray-50 border border-gray-300 rounded-xl text-gray-900 placeholder-gray-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 resize-none transition-all"
        />
      </div>

      {/* Error Message */}
      {error && (
        <div className="lg:col-span-2 bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-xl flex items-center gap-2">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {error}
        </div>
      )}

      {/* Submit Button */}
      <div className="lg:col-span-2">
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-4 px-6 rounded-xl shadow-md hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 text-lg"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-6 w-6" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Analyzing Resume...</span>
            </>
          ) : (
            <>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <span>Analyze Resume with AI</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default ResumeUpload;
