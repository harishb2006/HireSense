import React, { useState, useEffect, useRef } from 'react';

const AIInterviewer = ({ resumeData, jobDescription }) => {
  const [messages, setMessages] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [userAnswer, setUserAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [interviewStarted, setInterviewStarted] = useState(false);
  const [interviewComplete, setInterviewComplete] = useState(false);
  const [questionCount, setQuestionCount] = useState(0);
  const [feedback, setFeedback] = useState(null);
  const messagesEndRef = useRef(null);

  const maxQuestions = 5;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const startInterview = async () => {
    setInterviewStarted(true);
    setLoading(true);
    
    const welcomeMessage = {
      type: 'ai',
      content: `Hello! I'm your AI interviewer. I'll be conducting a mock interview based on the job description you provided. This interview will consist of ${maxQuestions} questions covering technical skills, experience, and behavioral aspects. Let's begin!`,
      timestamp: new Date().toISOString()
    };
    
    setMessages([welcomeMessage]);
    
    // Generate first question
    setTimeout(() => {
      generateQuestion();
    }, 1500);
  };

  const generateQuestion = async () => {
    setLoading(true);
    
    try {
      // Simulate AI question generation
      const questions = [
        "Can you walk me through your most relevant work experience for this position?",
        "What technical skills from your resume align best with this role?",
        "Describe a challenging project you've worked on and how you overcame obstacles.",
        "How do you stay updated with the latest technologies and industry trends?",
        "Why do you think you're a good fit for this position based on the job requirements?"
      ];
      
      const question = questions[questionCount] || "Tell me about a time when you demonstrated leadership.";
      
      setCurrentQuestion(question);
      
      const aiMessage = {
        type: 'ai',
        content: question,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, aiMessage]);
      setLoading(false);
    } catch (error) {
      console.error('Error generating question:', error);
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!userAnswer.trim()) return;

    const userMessage = {
      type: 'user',
      content: userAnswer,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setUserAnswer('');
    setLoading(true);

    // Simulate AI feedback
    setTimeout(() => {
      const feedbackMessage = {
        type: 'ai',
        content: "Thank you for your answer. That's a good response showing your experience and skills.",
        timestamp: new Date().toISOString(),
        isFeedback: true
      };
      
      setMessages(prev => [...prev, feedbackMessage]);
      
      const newCount = questionCount + 1;
      setQuestionCount(newCount);
      
      if (newCount >= maxQuestions) {
        setTimeout(() => {
          completeInterview();
        }, 1500);
      } else {
        setTimeout(() => {
          generateQuestion();
        }, 1500);
      }
    }, 2000);
  };

  const completeInterview = () => {
    setInterviewComplete(true);
    setLoading(false);
    
    const completionMessage = {
      type: 'ai',
      content: `Great job! You've completed the interview. I've assessed your responses and will now provide comprehensive feedback.`,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, completionMessage]);
    
    // Generate overall feedback
    const overallFeedback = {
      overallScore: 78,
      strengths: [
        'Clear communication and articulation',
        'Good technical knowledge demonstration',
        'Relevant experience highlighted effectively'
      ],
      improvements: [
        'Provide more specific examples with metrics',
        'Elaborate on problem-solving approaches',
        'Connect answers more directly to job requirements'
      ],
      recommendations: [
        'Practice the STAR method for behavioral questions',
        'Research the company and role more deeply',
        'Prepare specific metrics and achievements'
      ]
    };
    
    setFeedback(overallFeedback);
  };

  const restartInterview = () => {
    setMessages([]);
    setCurrentQuestion('');
    setUserAnswer('');
    setInterviewStarted(false);
    setInterviewComplete(false);
    setQuestionCount(0);
    setFeedback(null);
  };

  if (!interviewStarted) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-lg">
          <div className="text-center mb-8">
            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center mx-auto mb-6">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">AI Mock Interview</h2>
            <p className="text-gray-600 text-lg mb-6">
              Prepare for your real interview with our AI-powered mock interview session
            </p>
          </div>

          <div className="space-y-4 mb-8">
            <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-xl border border-blue-200">
              <svg className="w-6 h-6 text-blue-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">What to Expect</h3>
                <ul className="text-gray-700 text-sm space-y-1">
                  <li>• {maxQuestions} interview questions tailored to your profile</li>
                  <li>• Mix of technical, behavioral, and experience-based questions</li>
                  <li>• Real-time feedback on your responses</li>
                  <li>• Comprehensive evaluation at the end</li>
                </ul>
              </div>
            </div>

            <div className="flex items-start gap-3 p-4 bg-indigo-50 rounded-xl border border-indigo-200">
              <svg className="w-6 h-6 text-indigo-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Tips for Success</h3>
                <ul className="text-gray-700 text-sm space-y-1">
                  <li>• Take your time to think before answering</li>
                  <li>• Use specific examples from your experience</li>
                  <li>• Structure your answers clearly (STAR method)</li>
                  <li>• Be honest and authentic in your responses</li>
                </ul>
              </div>
            </div>
          </div>

          <button
            onClick={startInterview}
            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-4 px-6 rounded-xl shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-3"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Start Interview
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="bg-white border border-gray-200 rounded-2xl shadow-lg overflow-hidden">
        {/* Interview Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-white/20 flex items-center justify-center">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <div>
                <h2 className="text-xl font-bold">AI Mock Interview</h2>
                <p className="text-blue-100 text-sm">Question {Math.min(questionCount + 1, maxQuestions)} of {maxQuestions}</p>
              </div>
            </div>
            {!interviewComplete && (
              <div className="text-right">
                <div className="text-2xl font-bold">{Math.round((questionCount / maxQuestions) * 100)}%</div>
                <div className="text-blue-100 text-sm">Complete</div>
              </div>
            )}
          </div>
        </div>

        {/* Messages Container */}
        <div className="h-[500px] overflow-y-auto p-6 space-y-4 bg-gray-50">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl p-4 ${
                  message.type === 'user'
                    ? 'bg-blue-600 text-white'
                    : message.isFeedback
                    ? 'bg-green-50 border border-green-200 text-gray-800'
                    : 'bg-white border border-gray-200 text-gray-800'
                }`}
              >
                <div className="flex items-start gap-3">
                  {message.type === 'ai' && (
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.isFeedback ? 'bg-green-100' : 'bg-blue-100'
                    }`}>
                      {message.isFeedback ? (
                        <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      ) : (
                        <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                      )}
                    </div>
                  )}
                  <p className="text-sm leading-relaxed">{message.content}</p>
                </div>
              </div>
            </div>
          ))}
          
          {loading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 rounded-2xl p-4">
                <div className="flex items-center gap-2">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                  <span className="text-gray-500 text-sm">AI is thinking...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Feedback Section */}
        {interviewComplete && feedback && (
          <div className="p-6 bg-white border-t border-gray-200">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Interview Feedback</h3>
            
            <div className="grid md:grid-cols-3 gap-4 mb-6">
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-4 text-center">
                <div className="text-4xl font-bold text-blue-600 mb-2">{feedback.overallScore}%</div>
                <div className="text-gray-700 font-medium">Overall Score</div>
              </div>
              
              <div className="bg-green-50 border border-green-200 rounded-xl p-4 text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">{feedback.strengths.length}</div>
                <div className="text-gray-700 font-medium">Strengths</div>
              </div>
              
              <div className="bg-orange-50 border border-orange-200 rounded-xl p-4 text-center">
                <div className="text-4xl font-bold text-orange-600 mb-2">{feedback.improvements.length}</div>
                <div className="text-gray-700 font-medium">Areas to Improve</div>
              </div>
            </div>

            <div className="space-y-6">
              <div>
                <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Strengths
                </h4>
                <ul className="space-y-2">
                  {feedback.strengths.map((strength, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-gray-700">
                      <span className="text-green-600 mt-1">•</span>
                      {strength}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <svg className="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  Areas for Improvement
                </h4>
                <ul className="space-y-2">
                  {feedback.improvements.map((improvement, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-gray-700">
                      <span className="text-orange-600 mt-1">•</span>
                      {improvement}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  Recommendations
                </h4>
                <ul className="space-y-2">
                  {feedback.recommendations.map((recommendation, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-gray-700">
                      <span className="text-blue-600 mt-1">•</span>
                      {recommendation}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <button
              onClick={restartInterview}
              className="w-full mt-6 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-xl shadow-md hover:shadow-lg transition-all"
            >
              Start New Interview
            </button>
          </div>
        )}

        {/* Input Area */}
        {!interviewComplete && interviewStarted && (
          <div className="p-6 bg-white border-t border-gray-200">
            <div className="flex gap-3">
              <textarea
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    submitAnswer();
                  }
                }}
                placeholder="Type your answer here... (Press Enter to submit, Shift+Enter for new line)"
                className="flex-1 px-4 py-3 bg-gray-50 border border-gray-300 rounded-xl text-gray-900 placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 resize-none"
                rows="3"
                disabled={loading}
              />
              <button
                onClick={submitAnswer}
                disabled={loading || !userAnswer.trim()}
                className="px-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
                Send
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AIInterviewer;
