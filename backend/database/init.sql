-- HireSense Mock Interview Database Schema

-- User Profiles Table
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    total_interviews INTEGER DEFAULT 0,
    avg_score DECIMAL(5,2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interview Sessions Table
CREATE TABLE IF NOT EXISTS interview_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    role VARCHAR(100) NOT NULL,  -- e.g., "Node.js Developer", "React Developer"
    seniority_level VARCHAR(50) NOT NULL,  -- e.g., "Junior", "Mid", "Senior"
    status VARCHAR(50) DEFAULT 'active',  -- active, completed, abandoned
    total_score DECIMAL(5,2) DEFAULT 0.0,
    technical_depth_score DECIMAL(5,2) DEFAULT 0.0,
    clarity_score DECIMAL(5,2) DEFAULT 0.0,
    confidence_score DECIMAL(5,2) DEFAULT 0.0,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP NULL,
    duration_minutes INTEGER DEFAULT 0,
    
    -- Conversation state for AI memory
    ai_context JSONB DEFAULT '{}',  -- Stores AI's understanding of user's strengths/weaknesses
    follow_up_queue JSONB DEFAULT '[]',  -- Queue of follow-up questions to drill down
    knowledge_map JSONB DEFAULT '{}',  -- Tracks user's knowledge across topics
    current_topic VARCHAR(100) NULL,  -- Current topic being discussed
    topics_covered TEXT[] DEFAULT '{}'  -- Topics already covered
);

-- Conversation Messages Table
CREATE TABLE IF NOT EXISTS conversation_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id UUID REFERENCES interview_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,  -- 'user' or 'assistant'
    message TEXT NOT NULL,
    depth_score DECIMAL(5,2) DEFAULT NULL,  -- Only for user messages
    clarity_score DECIMAL(5,2) DEFAULT NULL,
    confidence_score DECIMAL(5,2) DEFAULT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message_number INTEGER NOT NULL,  -- Sequential order in conversation
    
    -- AI Analysis metadata
    is_follow_up VARCHAR(10) DEFAULT 'false',  -- 'true' if this was a drill-down question
    topic VARCHAR(100) NULL,  -- Topic this message relates to
    keywords_detected TEXT[] DEFAULT '{}',  -- Key technical terms mentioned
    model_answer TEXT NULL  -- Ideal answer for comparison (for AI questions)
);

-- Question Bank Table
CREATE TABLE IF NOT EXISTS question_bank (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100) NOT NULL,  -- e.g., "Backend", "Frontend", "Database"
    role VARCHAR(100) NOT NULL,
    seniority_level VARCHAR(50) NOT NULL,
    question_text TEXT NOT NULL,
    ideal_answer TEXT NOT NULL,
    follow_up_hints JSONB DEFAULT '[]',  -- Array of follow-up question templates
    tags TEXT[] DEFAULT '{}',  -- e.g., {"Node.js", "Event Loop", "Async"}
    difficulty INTEGER DEFAULT 5,  -- 1-10 scale
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_sessions_user_id ON interview_sessions(user_id);
CREATE INDEX idx_sessions_status ON interview_sessions(status);
CREATE INDEX idx_messages_session_id ON conversation_messages(session_id);
CREATE INDEX idx_messages_timestamp ON conversation_messages(timestamp);
CREATE INDEX idx_questions_role_level ON question_bank(role, seniority_level);
CREATE INDEX idx_questions_category ON question_bank(category);

-- Insert sample questions for testing
INSERT INTO question_bank (category, role, seniority_level, question_text, ideal_answer, follow_up_hints, tags, difficulty) VALUES
(
    'Backend',
    'Node.js Developer',
    'Senior',
    'Can you explain how the Event Loop handles Asynchronous I/O in Node.js?',
    'The Event Loop is the core of Node.js''s non-blocking I/O model. It operates in phases: timers, pending callbacks, idle/prepare, poll, check, and close callbacks. The poll phase is where I/O operations are handled. When async operations complete, their callbacks are queued. The event loop continuously checks these queues and executes callbacks, allowing Node.js to handle thousands of concurrent connections efficiently.',
    '["What happens if a setImmediate is scheduled during the poll phase?", "How does the microtask queue (process.nextTick) interact with the event loop phases?", "Can you explain the difference between setImmediate and setTimeout(fn, 0)?"]',
    ARRAY['Node.js', 'Event Loop', 'Async I/O', 'Performance'],
    8
),
(
    'Backend',
    'Node.js Developer',
    'Mid',
    'What is middleware in Express.js and how does it work?',
    'Middleware functions are functions that have access to the request object (req), response object (res), and the next middleware function in the application''s request-response cycle. They can execute code, modify req/res objects, end the request-response cycle, or call the next middleware using next(). Middleware is executed sequentially and can be application-level, router-level, error-handling, or built-in.',
    '["How do you handle errors in middleware?", "What is the difference between app.use() and app.get()?", "Can you explain the order of middleware execution?"]',
    ARRAY['Express.js', 'Middleware', 'Backend', 'API'],
    5
),
(
    'Frontend',
    'React Developer',
    'Senior',
    'Explain the concept of reconciliation in React and how the Virtual DOM works.',
    'Reconciliation is the algorithm React uses to diff the Virtual DOM with the actual DOM. When state changes, React creates a new Virtual DOM tree and compares it with the previous one using a diffing algorithm. It identifies the minimal set of changes needed and updates only those specific DOM nodes. React uses keys to track elements, and the algorithm has O(n) complexity by making assumptions like elements of different types produce different trees.',
    '["What role do keys play in the reconciliation process?", "How does React Fiber improve reconciliation?", "What is the difference between controlled and uncontrolled reconciliation?"]',
    ARRAY['React', 'Virtual DOM', 'Reconciliation', 'Performance'],
    9
),
(
    'Frontend',
    'React Developer',
    'Junior',
    'What is JSX and why do we use it in React?',
    'JSX is a syntax extension for JavaScript that allows you to write HTML-like code within JavaScript. It makes it easier to create React elements and components. JSX gets compiled to React.createElement() calls by tools like Babel. We use it because it makes the code more readable and allows us to leverage the full power of JavaScript within our markup.',
    '["Can you write React without JSX?", "What are the differences between JSX and HTML?", "How does Babel transform JSX?"]',
    ARRAY['React', 'JSX', 'Basics', 'Frontend'],
    3
),
(
    'Frontend',
    'React Developer',
    'Junior',
    'What is the difference between state and props in React?',
    'Props are read-only data passed from parent to child components, while state is mutable data managed within a component. Props are used for component communication and configuration, whereas state is used for data that changes over time and affects the component''s rendering. State changes trigger re-renders, and you update state using setState() in class components or the useState hook in functional components.',
    '["Can you modify props directly?", "When would you lift state up?", "What happens when state changes?"]',
    ARRAY['React', 'State', 'Props', 'Basics'],
    3
),
(
    'Frontend',
    'React Developer',
    'Junior',
    'Explain the useState hook and how it works.',
    'useState is a React Hook that lets you add state to functional components. It returns an array with two elements: the current state value and a function to update it. When you call the setter function, React re-renders the component with the new state value. You can initialize state with a value or a function. Each useState call creates an independent state variable.',
    '["What happens if you call the setter function with the same value?", "Can you have multiple useState hooks in one component?", "What is lazy initialization in useState?"]',
    ARRAY['React', 'Hooks', 'useState', 'State Management'],
    4
),
(
    'Frontend',
    'React Developer',
    'Mid',
    'What is the useEffect hook and when would you use it?',
    'useEffect is a Hook that lets you perform side effects in functional components. It runs after every render by default, but you can control when it runs using the dependency array. Common use cases include data fetching, subscriptions, manually changing the DOM, and setting up timers. You can return a cleanup function from useEffect to handle cleanup operations like unsubscribing or canceling requests.',
    '["What is the purpose of the dependency array?", "How do you prevent an infinite loop with useEffect?", "What is the cleanup function used for?"]',
    ARRAY['React', 'Hooks', 'useEffect', 'Side Effects'],
    6
),
(
    'Backend',
    'Node.js Developer',
    'Junior',
    'What is Node.js and what makes it different from traditional server-side languages?',
    'Node.js is a JavaScript runtime built on Chrome''s V8 engine that allows you to run JavaScript on the server. Unlike traditional server-side languages that use multi-threading, Node.js uses a single-threaded, non-blocking, event-driven architecture. This makes it efficient for I/O-heavy operations and allows it to handle many concurrent connections with minimal overhead.',
    '["What is the event loop?", "What types of applications is Node.js best suited for?", "What is npm?"]',
    ARRAY['Node.js', 'Basics', 'Backend', 'JavaScript'],
    3
);

-- Function to update user statistics after interview completion
CREATE OR REPLACE FUNCTION update_user_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        UPDATE user_profiles
        SET 
            total_interviews = total_interviews + 1,
            avg_score = (
                SELECT AVG(total_score)
                FROM interview_sessions
                WHERE user_id = NEW.user_id AND status = 'completed'
            ),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = NEW.user_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_user_stats
AFTER UPDATE ON interview_sessions
FOR EACH ROW
EXECUTE FUNCTION update_user_stats();

COMMENT ON TABLE user_profiles IS 'Stores user information and interview statistics';
COMMENT ON TABLE interview_sessions IS 'Tracks individual interview sessions with metadata and scores';
COMMENT ON TABLE conversation_messages IS 'Stores complete conversation history with scoring';
COMMENT ON TABLE question_bank IS 'Pre-defined questions with ideal answers and follow-up templates';
