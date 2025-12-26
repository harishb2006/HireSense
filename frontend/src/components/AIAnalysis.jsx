import React, { useState } from 'react';
import { API_BASE_URL } from '../config';

const AIAnalysis = ({ data, onStartInterview }) => {
  const [downloadingPDF, setDownloadingPDF] = useState(false);

  if (!data || !data.analysis) return null;

  const { analysis } = data;
  const matchScore = analysis.match_score || 0;
  const overallAssessment = analysis.overall_assessment || '';
  const whyNotPassing = analysis.why_not_passing || {};
  const missingKeywords = analysis.missing_keywords || [];
  const gapAnalysis = analysis.gap_analysis || {};
  const sectionFeedback = analysis.section_detailed_feedback || {};
  const actionableSteps = analysis.actionable_next_steps || [];

  const getScoreColor = (score) => {
    if (score >= 70) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 50) return 'text-orange-600 bg-orange-50 border-orange-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const getScoreLabel = (score) => {
    if (score >= 70) return 'Good Match';
    if (score >= 50) return 'Moderate Match';
    return 'Needs Improvement';
  };

  const downloadPDFScorecard = async () => {
    setDownloadingPDF(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/rewriter/generate-scorecard`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          analysis: analysis,
          candidate_name: 'Candidate',
          interview_summary: null // Will be populated after interview
        }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `HireSense_Scorecard_${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        alert('Failed to generate PDF. Please try again.');
      }
    } catch (error) {
      console.error('PDF download error:', error);
      alert('Failed to download PDF. Please try again.');
    } finally {
      setDownloadingPDF(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-lg">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Resume Analysis Results</h2>
            <p className="text-gray-600">Here's your detailed AI-powered analysis</p>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={downloadPDFScorecard}
              disabled={downloadingPDF}
              className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-semibold py-3 px-6 rounded-xl shadow-md hover:shadow-lg transition-all inline-flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {downloadingPDF ? (
                <>
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Generating...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Download PDF Scorecard
                </>
              )}
            </button>
            <div className={`text-center px-6 py-4 rounded-xl border-2 ${getScoreColor(matchScore)}`}>
              <div className="text-4xl font-bold">{matchScore}%</div>
              <div className="text-sm font-medium mt-1">{getScoreLabel(matchScore)}</div>
            </div>
          </div>
        </div>

        {/* Overall Assessment */}
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
          <h3 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
            <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Overall Assessment
          </h3>
          <p className="text-gray-700 leading-relaxed">{overallAssessment}</p>
        </div>
      </div>

      {/* Why Not Passing Section */}
      {whyNotPassing.main_reasons && whyNotPassing.main_reasons.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Why Your Resume May Not Pass ATS
          </h3>
          
          <div className="space-y-3 mb-4">
            {whyNotPassing.main_reasons.map((reason, idx) => (
              <div key={idx} className="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-xl">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-red-600 text-white flex items-center justify-center text-sm font-bold">{idx + 1}</span>
                <p className="text-gray-800">{reason}</p>
              </div>
            ))}
          </div>

          {whyNotPassing.ats_perspective && (
            <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
              <h4 className="font-semibold text-gray-900 mb-2">🤖 ATS Perspective</h4>
              <p className="text-gray-700 text-sm">{whyNotPassing.ats_perspective}</p>
            </div>
          )}
        </div>
      )}

      {/* Missing Keywords */}
      {missingKeywords.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            Missing Critical Keywords
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {missingKeywords.map((item, idx) => (
              <div key={idx} className="border border-gray-200 rounded-xl p-4 hover:shadow-md transition-all">
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-3 py-1 bg-orange-100 text-orange-700 text-sm font-semibold rounded-full">
                    {item.keyword}
                  </span>
                  <span className={`text-xs font-medium px-2 py-1 rounded ${
                    item.importance === 'critical' ? 'bg-red-100 text-red-700' :
                    item.importance === 'high' ? 'bg-orange-100 text-orange-700' :
                    'bg-yellow-100 text-yellow-700'
                  }`}>
                    {item.importance}
                  </span>
                </div>
                <p className="text-gray-700 text-sm">{item.why_matters}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Gap Analysis */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-lg">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          Gap Analysis
        </h3>

        <div className="space-y-4">
          {gapAnalysis.experience_gaps && (
            <div className="border border-gray-200 rounded-xl p-4">
              <h4 className="font-semibold text-gray-900 mb-2">📊 Experience Gaps</h4>
              <p className="text-gray-700">{gapAnalysis.experience_gaps}</p>
            </div>
          )}

          {gapAnalysis.skills_gaps && (
            <div className="border border-gray-200 rounded-xl p-4">
              <h4 className="font-semibold text-gray-900 mb-2">🛠️ Skills Gaps</h4>
              <p className="text-gray-700">{gapAnalysis.skills_gaps}</p>
            </div>
          )}

          {gapAnalysis.qualification_gaps && (
            <div className="border border-gray-200 rounded-xl p-4">
              <h4 className="font-semibold text-gray-900 mb-2">🎓 Qualification Gaps</h4>
              <p className="text-gray-700">{gapAnalysis.qualification_gaps}</p>
            </div>
          )}
        </div>
      </div>

      {/* Section Detailed Feedback */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-lg">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Section-by-Section Feedback
        </h3>

        <div className="space-y-4">
          {Object.entries(sectionFeedback).map(([section, feedback]) => (
            <div key={section} className="border border-gray-200 rounded-xl p-4">
              <h4 className="font-semibold text-gray-900 mb-3 capitalize">{section}</h4>
              <div className="space-y-2 text-sm">
                <div>
                  <span className="font-medium text-gray-700">Current State:</span>
                  <p className="text-gray-600 mt-1">{feedback.current_state}</p>
                </div>
                <div>
                  <span className="font-medium text-red-700">Problem:</span>
                  <p className="text-gray-600 mt-1">{feedback.problem}</p>
                </div>
                <div>
                  <span className="font-medium text-orange-700">Impact:</span>
                  <p className="text-gray-600 mt-1">{feedback.impact}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Actionable Next Steps */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 border border-blue-700 rounded-2xl p-6 shadow-lg text-white">
        <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          Your Action Plan
        </h3>

        <div className="space-y-3">
          {actionableSteps.map((step, idx) => (
            <div key={idx} className="flex items-start gap-3 bg-white/10 rounded-xl p-4 backdrop-blur-sm">
              <span className="flex-shrink-0 w-8 h-8 rounded-full bg-white/20 text-white flex items-center justify-center font-bold">{idx + 1}</span>
              <p className="text-white">{step}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Call to Action - Practice Interview */}
      <div className="bg-white border-2 border-blue-300 rounded-2xl p-8 shadow-lg text-center">
        <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <h3 className="text-2xl font-bold text-gray-900 mb-3">Ready to Practice?</h3>
        <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
          Now that you know your weak areas, let's practice interview questions specifically targeting these gaps. This will help you prepare answers that address your shortcomings.
        </p>
        <button
          onClick={onStartInterview}
          className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-4 px-8 rounded-xl shadow-md hover:shadow-lg transition-all inline-flex items-center gap-3"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Start Mock Interview
        </button>
      </div>
    </div>
  );
};

export default AIAnalysis;
