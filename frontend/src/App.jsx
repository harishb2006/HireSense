import React, { useState } from 'react';
import ResumeUpload from './components/ResumeUpload';
import AIAnalysis from './components/AIAnalysis';
import AIInterviewer from './components/AIInterviewer';
import StarRewriter from './components/StarRewriter';
import './App.css';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [activeTab, setActiveTab] = useState('upload');
  const [interviewSummary, setInterviewSummary] = useState(null);

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
  };

  const handleStartInterview = () => {
    setActiveTab('interview');
  };

  const handleInterviewComplete = (summary) => {
    setInterviewSummary(summary);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white/80 backdrop-blur-sm sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center">
                <span className="text-white text-xl font-bold">🎯</span>
              </div>
              <div>
                <h1 className="text-gray-900 font-bold text-xl">HireSense</h1>
                <p className="text-gray-500 text-xs">AI-Powered Career Mentor</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-gray-500 text-xs">Status</p>
                <p className="text-green-600 text-sm font-medium flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                  Active
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Navigation Tabs */}
        <div className="mb-8">
          <div className="flex gap-2 bg-white border border-gray-200 rounded-xl p-1 max-w-2xl mx-auto shadow-sm">
            <button
              onClick={() => setActiveTab('upload')}
              className={`flex-1 px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === 'upload'
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              📊 Analysis
            </button>
            <button
              onClick={() => setActiveTab('interview')}
              disabled={!analysisData}
              className={`flex-1 px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === 'interview'
                  ? 'bg-indigo-600 text-white shadow-md'
                  : analysisData
                  ? 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  : 'text-gray-400 cursor-not-allowed bg-gray-50'
              }`}
            >
              🎤 Mock Interview
            </button>
            <button
              onClick={() => setActiveTab('rewriter')}
              disabled={!analysisData}
              className={`flex-1 px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === 'rewriter'
                  ? 'bg-purple-600 text-white shadow-md'
                  : analysisData
                  ? 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  : 'text-gray-400 cursor-not-allowed bg-gray-50'
              }`}
            >
              ✨ STAR Rewriter
            </button>
          </div>
        </div>
        {/* Resume Analysis Tab */}
        {activeTab === 'upload' && (
          <>
            {/* Upload Section */}
            <div className="mb-12">
              <ResumeUpload onAnalysisComplete={handleAnalysisComplete} />
            </div>

            {/* Analysis Results */}
            {analysisData && (
              <div className="animate-fadeIn">
                <AIAnalysis 
                  data={analysisData} 
                  onStartInterview={handleStartInterview}
                />
              </div>
            )}

            {/* Features Section - Show when no analysis */}
            {!analysisData && (
              <div className="mt-16">
                <h3 className="text-2xl font-bold text-gray-900 text-center mb-8">🚀 Powerful Features</h3>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-blue-300 transition-all">
                    <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center mb-4">
                      <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                    <h4 className="text-gray-900 font-semibold text-lg mb-2">Match Score</h4>
                    <p className="text-gray-600 text-sm">Get percentage match between resume and job description</p>
                  </div>

                  <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-indigo-300 transition-all">
                    <div className="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center mb-4">
                      <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                      </svg>
                    </div>
                    <h4 className="text-gray-900 font-semibold text-lg mb-2">Mock Interview</h4>
                    <p className="text-gray-600 text-sm">Practice targeted questions based on your weaknesses</p>
                  </div>

                  <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-purple-300 transition-all">
                    <div className="w-12 h-12 rounded-xl bg-purple-50 flex items-center justify-center mb-4">
                      <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </div>
                    <h4 className="text-gray-900 font-semibold text-lg mb-2">STAR Rewriter</h4>
                    <p className="text-gray-600 text-sm">Transform weak bullets into impactful achievements</p>
                  </div>

                  <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-green-300 transition-all">
                    <div className="w-12 h-12 rounded-xl bg-green-50 flex items-center justify-center mb-4">
                      <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <h4 className="text-gray-900 font-semibold text-lg mb-2">PDF Scorecard</h4>
                    <p className="text-gray-600 text-sm">Download comprehensive analysis and interview feedback</p>
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {/* AI Interview Tab */}
        {activeTab === 'interview' && analysisData && (
          <div className="animate-fadeIn">
            <AIInterviewer 
              resumeData={analysisData?.analysis} 
              jobDescription={analysisData?.jobDescription}
              interviewQuestions={analysisData?.interview?.questions}
              onInterviewComplete={handleInterviewComplete}
            />
          </div>
        )}

        {/* STAR Rewriter Tab */}
        {activeTab === 'rewriter' && analysisData && (
          <div className="animate-fadeIn">
            <StarRewriter 
              jobDescription={analysisData?.jobDescription}
              resumeContext={analysisData?.resumeText}
            />
          </div>
        )}

        {/* Placeholder for locked tabs */}
        {(activeTab === 'interview' || activeTab === 'rewriter') && !analysisData && (
          <div className="bg-white border border-gray-200 rounded-2xl p-12 text-center shadow-lg">
            <div className="w-20 h-20 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-6">
              <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-3">Feature Locked</h3>
            <p className="text-gray-600 mb-6 max-w-md mx-auto">
              Upload your resume and job description first to unlock {activeTab === 'interview' ? 'mock interview' : 'STAR rewriter'} features.
            </p>
            <button
              onClick={() => setActiveTab('upload')}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-xl shadow-md hover:shadow-lg transition-all"
            >
              Go to Resume Analysis
            </button>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 mt-20 bg-white">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <p className="text-gray-500 text-sm text-center">
            © 2025 HireSense. Your AI-powered career mentor helping you land your dream job.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
