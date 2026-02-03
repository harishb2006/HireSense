import React, { useState, useEffect, useRef } from 'react';
import { API_BASE_URL } from '../config';

/**
 * Prep Pro - Dynamic State-Aware AI Interviewer
 * Features:
 * - Multi-turn conversation with memory
 * - Real-time evaluation & live scoring
 * - Adaptive follow-up questions
 * - Knowledge map tracking
 * - Optional voice mode
 */
const AIInterviewer = () => {
  // Session State
  const [sessionId, setSessionId] = useState(null);
  const [sessionStarted, setSessionStarted] = useState(false);
  const [sessionCompleted, setSessionCompleted] = useState(false);
  
  // User Setup
  const [userName, setUserName] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [selectedRole, setSelectedRole] = useState('Node.js Developer');
  const [selectedLevel, setSelectedLevel] = useState('Senior');
  
  // Conversation
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentTopic, setCurrentTopic] = useState('');
  
  // Live Scoring
  const [liveScores, setLiveScores] = useState({
    technical_depth: 0,
    clarity: 0,
    confidence: 0,
    overall: 0
  });
  
  // Voice Mode (optional)
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [isListening, setIsListening] = useState(false);
  
  // Refs
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);
  
  // Available roles and levels
  const roles = ['Node.js Developer', 'React Developer', 'Python Developer', 'Full Stack Developer'];
  const levels = ['Junior', 'Mid', 'Senior'];
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  useEffect(() => {
    // Initialize Web Speech API if available
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      
      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setUserInput(transcript);
        setIsListening(false);
      };
      
      recognitionRef.current.onerror = () => {
        setIsListening(false);
      };
    }
  }, []);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  const startInterview = async () => {
    if (!userName.trim() || !userEmail.trim()) {
      alert('Please enter your name and email');
      return;
    }
    
    setLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/mock-interview/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_name: userName,
          user_email: userEmail,
          role: selectedRole,
          seniority_level: selectedLevel
        })
      });
      
      if (!response.ok) throw new Error('Failed to start interview');
      
      const data = await response.json();
      setSessionId(data.session_id);
      setSessionStarted(true);
      
      // Add AI's first question
      setMessages([{
        role: 'assistant',
        content: data.first_question,
        timestamp: new Date().toISOString(),
        messageNumber: 1
      }]);
      
      // Speak the question if voice is enabled
      if (voiceEnabled) {
        speakText(data.first_question);
      }
      
    } catch (error) {
      console.error('Error starting interview:', error);
      alert('Failed to start interview. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const submitAnswer = async () => {
    if (!userInput.trim() || loading) return;
    
    // Add user message immediately
    const userMessage = {
      role: 'user',
      content: userInput,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMessage]);
    
    const answerText = userInput;
    setUserInput('');
    setLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/mock-interview/answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          answer: answerText
        })
      });
      
      if (!response.ok) throw new Error('Failed to submit answer');
      
      const data = await response.json();
      
      // Update live scores
      setLiveScores({
        technical_depth: data.depth_score || 0,
        clarity: data.clarity_score || 0,
        confidence: data.confidence_score || 0,
        overall: data.overall_score || 0
      });
      
      // Update current topic
      if (data.current_topic) {
        setCurrentTopic(data.current_topic);
      }
      
      // Check if interview completed
      if (data.session_status === 'completed') {
        setSessionCompleted(true);
      }
      
      // Add AI's next question/response
      const aiMessage = {
        role: 'assistant',
        content: data.next_question,
        timestamp: new Date().toISOString(),
        messageNumber: data.message_number,
        isFollowUp: data.is_follow_up,
        scores: {
          technical_depth: data.depth_score,
          clarity: data.clarity_score,
          confidence: data.confidence_score,
          overall: data.overall_score
        }
      };
      setMessages(prev => [...prev, aiMessage]);
      
      // Speak if voice enabled
      if (voiceEnabled && !sessionCompleted) {
        speakText(data.next_question);
      }
      
    } catch (error) {
      console.error('Error submitting answer:', error);
      alert('Failed to submit answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const toggleVoiceInput = () => {
    if (!recognitionRef.current) {
      alert('Voice input not supported in your browser');
      return;
    }
    
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };
  
  const speakText = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.pitch = 1;
      window.speechSynthesis.speak(utterance);
    }
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submitAnswer();
    }
  };
  
  const viewReport = () => {
    // Open report in new tab
    window.open(`${API_BASE_URL}/api/mock-interview/session/${sessionId}/report/html`, '_blank');
  };
  
  const viewKnowledgeMap = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/mock-interview/session/${sessionId}/knowledge-map`);
      const data = await response.json();
      console.log('Knowledge Map:', data);
      // Could show in a modal
      alert(JSON.stringify(data.knowledge_map, null, 2));
    } catch (error) {
      console.error('Error fetching knowledge map:', error);
    }
  };
  
  // Setup Screen
  if (!sessionStarted) {
    return (
      <div style={styles.container}>
        <div style={styles.setupCard}>
          <h1 style={styles.title}>🎯 Prep Pro - AI Interview Simulator</h1>
          <p style={styles.subtitle}>
            Dynamic, State-Aware Technical Interview Practice
          </p>
          
          <div style={styles.form}>
            <div style={styles.formGroup}>
              <label style={styles.label}>Your Name</label>
              <input
                type="text"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                style={styles.input}
                placeholder="John Doe"
              />
            </div>
            
            <div style={styles.formGroup}>
              <label style={styles.label}>Email</label>
              <input
                type="email"
                value={userEmail}
                onChange={(e) => setUserEmail(e.target.value)}
                style={styles.input}
                placeholder="john@example.com"
              />
            </div>
            
            <div style={styles.formGroup}>
              <label style={styles.label}>Role</label>
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                style={styles.select}
              >
                {roles.map(role => (
                  <option key={role} value={role}>{role}</option>
                ))}
              </select>
            </div>
            
            <div style={styles.formGroup}>
              <label style={styles.label}>Seniority Level</label>
              <select
                value={selectedLevel}
                onChange={(e) => setSelectedLevel(e.target.value)}
                style={styles.select}
              >
                {levels.map(level => (
                  <option key={level} value={level}>{level}</option>
                ))}
              </select>
            </div>
            
            <div style={styles.formGroup}>
              <label style={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  checked={voiceEnabled}
                  onChange={(e) => setVoiceEnabled(e.target.checked)}
                  style={styles.checkbox}
                />
                Enable Voice Mode (Experimental)
              </label>
            </div>
            
            <button
              onClick={startInterview}
              disabled={loading}
              style={styles.startButton}
            >
              {loading ? 'Starting...' : 'Start Interview'}
            </button>
          </div>
          
          <div style={styles.features}>
            <h3>What makes Prep Pro different?</h3>
            <ul>
              <li>🧠 <strong>AI Remembers:</strong> Multi-turn conversation with full context</li>
              <li>🎯 <strong>Adaptive Questions:</strong> Drills down based on your answers</li>
              <li>📊 <strong>Live Evaluation:</strong> Real-time depth, clarity, confidence tracking</li>
              <li>🗺️ <strong>Knowledge Map:</strong> Shows your strengths and weaknesses</li>
              <li>📝 <strong>Detailed Debrief:</strong> Compare your answers vs. model answers</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }
  
  // Interview Screen
  return (
    <div style={styles.interviewContainer}>
      {/* Header with Live Scores */}
      <div style={styles.header}>
        <div style={styles.headerInfo}>
          <h2 style={styles.headerTitle}>Interview in Progress</h2>
          <span style={styles.topic}>{currentTopic || 'Getting Started'}</span>
        </div>
        
        <div style={styles.scoresPanel}>
          <ScoreIndicator label="Depth" score={liveScores.technical_depth} />
          <ScoreIndicator label="Clarity" score={liveScores.clarity} />
          <ScoreIndicator label="Confidence" score={liveScores.confidence} />
          <ScoreIndicator label="Overall" score={liveScores.overall} highlight />
        </div>
      </div>
      
      {/* Chat Messages */}
      <div style={styles.messagesContainer}>
        {messages.map((msg, idx) => (
          <Message key={idx} message={msg} />
        ))}
        {loading && (
          <div style={styles.loadingMessage}>
            <div style={styles.typingIndicator}>
              <span></span><span></span><span></span>
            </div>
            AI is analyzing your response...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Area */}
      {!sessionCompleted ? (
        <div style={styles.inputContainer}>
          <textarea
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your answer here... (Press Enter to send)"
            style={styles.textarea}
            disabled={loading}
            rows={3}
          />
          <div style={styles.inputActions}>
            {voiceEnabled && recognitionRef.current && (
              <button
                onClick={toggleVoiceInput}
                style={{
                  ...styles.voiceButton,
                  ...(isListening ? styles.voiceButtonActive : {})
                }}
              >
                🎤 {isListening ? 'Listening...' : 'Voice'}
              </button>
            )}
            <button
              onClick={submitAnswer}
              disabled={loading || !userInput.trim()}
              style={styles.sendButton}
            >
              Send Answer
            </button>
          </div>
        </div>
      ) : (
        <div style={styles.completedPanel}>
          <h2 style={styles.completedTitle}>Interview Completed! 🎉</h2>
          <p style={styles.completedText}>
            Your final score: <strong>{liveScores.overall}/10</strong>
          </p>
          <div style={styles.completedActions}>
            <button onClick={viewReport} style={styles.reportButton}>
              View Detailed Report
            </button>
            <button onClick={viewKnowledgeMap} style={styles.mapButton}>
              View Knowledge Map
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

// Score Indicator Component
const ScoreIndicator = ({ label, score, highlight }) => (
  <div style={{
    ...styles.scoreCard,
    ...(highlight ? styles.scoreCardHighlight : {})
  }}>
    <div style={styles.scoreLabel}>{label}</div>
    <div style={styles.scoreValue}>{score.toFixed(1)}</div>
    <div style={styles.scoreBar}>
      <div style={{
        ...styles.scoreBarFill,
        width: `${(score / 10) * 100}%`,
        backgroundColor: score >= 7 ? '#27ae60' : score >= 5 ? '#f39c12' : '#e74c3c'
      }} />
    </div>
  </div>
);

// Message Component
const Message = ({ message }) => {
  const isAI = message.role === 'assistant';
  
  return (
    <div style={{
      ...styles.message,
      ...(isAI ? styles.messageAI : styles.messageUser)
    }}>
      <div style={styles.messageHeader}>
        <span style={styles.messageSender}>
          {isAI ? '🤖 AI Interviewer' : '👤 You'}
        </span>
        {message.isFollowUp && (
          <span style={styles.followUpBadge}>Follow-up</span>
        )}
      </div>
      <div style={styles.messageContent}>{message.content}</div>
      {message.scores && message.role === 'assistant' && (
        <div style={styles.messageScores}>
          Scores: Depth {message.scores.technical_depth} | 
          Clarity {message.scores.clarity} | 
          Confidence {message.scores.confidence}
        </div>
      )}
    </div>
  );
};

// Styles
const styles = {
  container: {
    padding: '20px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'flex-start'
  },
  setupCard: {
    background: 'white',
    borderRadius: '20px',
    padding: '40px',
    maxWidth: '600px',
    width: '100%',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    border: '1px solid #e5e7eb'
  },
  title: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: '10px',
    textAlign: 'center'
  },
  subtitle: {
    color: '#7f8c8d',
    textAlign: 'center',
    marginBottom: '30px'
  },
  form: {
    marginBottom: '30px'
  },
  formGroup: {
    marginBottom: '20px'
  },
  label: {
    display: 'block',
    marginBottom: '8px',
    fontWeight: '600',
    color: '#2c3e50'
  },
  input: {
    width: '100%',
    padding: '12px',
    fontSize: '16px',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    transition: 'border-color 0.3s',
    outline: 'none'
  },
  select: {
    width: '100%',
    padding: '12px',
    fontSize: '16px',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    backgroundColor: 'white',
    cursor: 'pointer'
  },
  checkboxLabel: {
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer',
    color: '#2c3e50'
  },
  checkbox: {
    marginRight: '10px',
    width: '18px',
    height: '18px',
    cursor: 'pointer'
  },
  startButton: {
    width: '100%',
    padding: '15px',
    fontSize: '18px',
    fontWeight: 'bold',
    color: 'white',
    background: '#3b82f6',
    border: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  features: {
    marginTop: '30px',
    padding: '20px',
    background: '#f8f9fa',
    borderRadius: '10px'
  },
  interviewContainer: {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '600px',
    maxHeight: '80vh',
    background: 'white',
    borderRadius: '12px',
    overflow: 'hidden',
    border: '1px solid #e5e7eb',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
  },
  header: {
    background: 'white',
    padding: '20px',
    borderBottom: '2px solid #e0e0e0',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  headerInfo: {
    flex: 1
  },
  headerTitle: {
    margin: 0,
    fontSize: '24px',
    color: '#2c3e50'
  },
  topic: {
    color: '#7f8c8d',
    fontSize: '14px'
  },
  scoresPanel: {
    display: 'flex',
    gap: '15px'
  },
  scoreCard: {
    background: '#f8f9fa',
    padding: '12px',
    borderRadius: '8px',
    minWidth: '80px',
    textAlign: 'center'
  },
  scoreCardHighlight: {
    background: '#3b82f6',
    color: 'white'
  },
  scoreLabel: {
    fontSize: '12px',
    marginBottom: '5px',
    opacity: 0.8
  },
  scoreValue: {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '5px'
  },
  scoreBar: {
    height: '4px',
    background: 'rgba(0,0,0,0.1)',
    borderRadius: '2px',
    overflow: 'hidden'
  },
  scoreBarFill: {
    height: '100%',
    transition: 'width 0.5s ease'
  },
  messagesContainer: {
    flex: 1,
    overflowY: 'auto',
    padding: '20px',
    background: '#f5f5f5'
  },
  message: {
    marginBottom: '20px',
    padding: '15px',
    borderRadius: '12px',
    maxWidth: '80%',
    animation: 'fadeIn 0.3s'
  },
  messageAI: {
    background: 'white',
    marginRight: 'auto',
    borderBottomLeftRadius: '4px'
  },
  messageUser: {
    background: '#3b82f6',
    color: 'white',
    marginLeft: 'auto',
    borderBottomRightRadius: '4px'
  },
  messageHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '8px'
  },
  messageSender: {
    fontSize: '14px',
    fontWeight: 'bold',
    opacity: 0.8
  },
  followUpBadge: {
    background: '#f39c12',
    color: 'white',
    padding: '2px 8px',
    borderRadius: '4px',
    fontSize: '12px'
  },
  messageContent: {
    fontSize: '16px',
    lineHeight: '1.6'
  },
  messageScores: {
    marginTop: '10px',
    fontSize: '12px',
    opacity: 0.7
  },
  loadingMessage: {
    textAlign: 'center',
    padding: '20px',
    color: '#7f8c8d'
  },
  typingIndicator: {
    display: 'inline-flex',
    gap: '5px',
    marginBottom: '10px'
  },
  inputContainer: {
    background: 'white',
    padding: '20px',
    borderTop: '2px solid #e0e0e0'
  },
  textarea: {
    width: '100%',
    padding: '15px',
    fontSize: '16px',
    border: '2px solid #e0e0e0',
    borderRadius: '10px',
    resize: 'none',
    outline: 'none',
    fontFamily: 'inherit'
  },
  inputActions: {
    display: 'flex',
    gap: '10px',
    marginTop: '10px',
    justifyContent: 'flex-end'
  },
  voiceButton: {
    padding: '10px 20px',
    background: '#95a5a6',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px'
  },
  voiceButtonActive: {
    background: '#e74c3c',
    animation: 'pulse 1s infinite'
  },
  sendButton: {
    padding: '10px 30px',
    background: '#3b82f6',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: 'bold',
    transition: 'background 0.2s'
  },
  completedPanel: {
    background: 'white',
    padding: '40px',
    textAlign: 'center',
    borderTop: '2px solid #e0e0e0'
  },
  completedTitle: {
    color: '#27ae60',
    marginBottom: '20px'
  },
  completedText: {
    fontSize: '18px',
    marginBottom: '30px'
  },
  completedActions: {
    display: 'flex',
    gap: '15px',
    justifyContent: 'center'
  },
  reportButton: {
    padding: '15px 30px',
    background: '#3498db',
    color: 'white',
    border: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: 'bold'
  },
  mapButton: {
    padding: '15px 30px',
    background: '#9b59b6',
    color: 'white',
    border: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: 'bold'
  }
};

export default AIInterviewer;
