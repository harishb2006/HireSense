import React, { useState } from 'react';
import ResumeUpload from './components/ResumeUpload';
import AIAnalysis from './components/AIAnalysis';
import AIInterviewer from './components/AIInterviewer';
import './App.css';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [activeTab, setActiveTab] = useState('upload');

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
  };

  const handleStartInterview = () => {
    setActiveTab('interview');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white/80 backdrop-blur-sm sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gray-800 flex items-center justify-center">
                <span className="text-white text-xl font-bold">🎯</span>
              </div>
              <div>
                <h1 className="text-gray-900 font-bold text-xl">HireSense</h1>
                <p className="text-gray-500 text-xs">AI-Powered Resume Analyzer</p>
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
          <div className="flex gap-2 bg-white border border-gray-200 rounded-xl p-1 max-w-md mx-auto shadow-sm">
            <button
              onClick={() => setActiveTab('upload')}
              className={`flex-1 px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === 'upload'
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
            Resume Analysis Tab */}
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
                <h3 className="text-2xl font-bold text-gray-900 text-center mb-8">Powerful Features</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-blue-300 transition-all">
                    <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center mb-4">
                      <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                    <h4 className="text-gray-900 font-semibold text-lg mb-2">Match Score</h4>
                    <p className="text-gray-600 text-sm">Get a percentage match between your resume and job description</p>
                  </div>

                  <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-indigo-300 transition-all">
                    <div className="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center mb-4">
                      <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </div>
                    <h4 className="text-gray-900 font-semibold text-lg mb-2">AI Insights</h4>
                    <p className="text-gray-600 text-sm">Powered by advanced AI to provide accurate analysis and suggestions</p>
                  </div>

                  <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-green-300 transition-all">
                    <div className="w-12 h-12 rounded-xl bg-green-50 flex items-center justify-center mb-4">
                      <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <h4 className="text-gray-900 font-semibold text-lg mb-2">Recommendations</h4>
                    <p className="text-gray-600 text-sm">Get actionable suggestions to improve your resume content</p>
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
            />
          </div>
        )}

        {/* Interview Features - Show when no interview started */}
        {activeTab === 'interview' && !analysisData && (
              <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-blue-300 transition-all">
                <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <h4 className="text-gray-900 font-semibold text-lg mb-2">Interactive Conversations</h4>
                <p className="text-gray-600 text-sm">Engage in realistic interview dialogues with AI-powered questions tailored to your profile</p>
              </div>

              <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-indigo-300 transition-all">
                <div className="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h4 className="text-gray-900 font-semibold text-lg mb-2">Real-time Feedback</h4>
                <p className="text-gray-600 text-sm">Receive instant feedback on your answers and learn how to improve your responses</p>
              </div>

              <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-green-300 transition-all">
                <div className="w-12 h-12 rounded-xl bg-green-50 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h4 className="text-gray-900 font-semibold text-lg mb-2">Performance Analytics</h4>
                <p className="text-gray-600 text-sm">Get detailed insights on your interview performance with scores and recommendations</p>
              </div>

              <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-purple-300 transition-all">
                <div className="w-12 h-12 rounded-xl bg-purple-50 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <h4 className="text-gray-900 font-semibold text-lg mb-2">Unlimited Practice</h4>
                <p className="text-gray-600 text-sm">Practice as many times as you want to build confidence and master your interview skills
              Prepare for your real interview with personalized mock interviews and instant feedback
            </p>
          </div>
        )}

        {/* Upload Section */}
        <div className="mb-12">
          <ResumeUpload onAnalysisComplete={handleAnalysisComplete} />
        </div>

        {/* Analysis Results */}
        {analysisData && (
          <div className="animate-fadeIn">
            <AIAnalysis data={analysisData} />
          </div>
        )}

        {/* Features Section - Show when no analysis */}
        {!analysisData && (
          <div className="mt-16">
            <h3 className="text-2xl font-bold text-gray-900 text-center mb-8">Powerful Features</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-blue-300 transition-all">
                <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h4 className="text-gray-900 font-semibold text-lg mb-2">Match Score</h4>
                <p className="text-gray-600 text-sm">Get a percentage match between your resume and job description</p>
              </div>

              <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-indigo-300 transition-all">
                <div className="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h4 className="text-gray-900 font-semibold text-lg mb-2">AI Insights</h4>
                <p className="text-gray-600 text-sm">Powered by advanced AI to provide accurate analysis and suggestions</p>
              </div>

              <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg hover:border-green-300 transition-all">
                <div className="w-12 h-12 rounded-xl bg-green-50 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h4 className="text-gray-900 font-semibold text-lg mb-2">Recommendations</h4>
                <p className="text-gray-600 text-sm">Get actionable suggestions to improve your resume content</p>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 mt-20 bg-white">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <p className="text-gray-500 text-sm text-center">
            © 2025 HireSense. Powered by AI to help you land your dream job.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
