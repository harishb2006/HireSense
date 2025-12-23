import { useState } from 'react';
import AIAnalysis from './components/AIAnalysis';
import ResumeUpload from './components/ResumeUpload';

function App() {
  const [activeTab, setActiveTab] = useState('analyze');

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="bg-white/10 backdrop-blur-lg border-b border-white/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center shadow-lg">
                <span className="text-2xl">🎯</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">HireSense</h1>
                <p className="text-sm text-white/80">AI-Powered Resume Analysis</p>
              </div>
            </div>
            
            <div className="flex gap-2">
              <button
                onClick={() => setActiveTab('analyze')}
                className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                  activeTab === 'analyze'
                    ? 'bg-white text-primary-600 shadow-lg'
                    : 'text-white hover:bg-white/10'
                }`}
              >
                🤖 AI Analysis
              </button>
              <button
                onClick={() => setActiveTab('upload')}
                className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                  activeTab === 'upload'
                    ? 'bg-white text-primary-600 shadow-lg'
                    : 'text-white hover:bg-white/10'
                }`}
              >
                📄 Upload Resume
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="py-8">
        {activeTab === 'analyze' ? (
          <AIAnalysis />
        ) : (
          <div className="max-w-4xl mx-auto px-6">
            <div className="text-center space-y-4 py-12">
              <h2 className="text-4xl font-bold text-white drop-shadow-lg">
                📤 Upload Your Resume
              </h2>
              <p className="text-lg text-white/90">
                Extract text from your PDF resume for analysis
              </p>
            </div>
            <ResumeUpload />
          </div>
        )}
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
