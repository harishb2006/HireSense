# AI Resume Analysis - Phase 2

## Overview

AI-powered resume analysis that returns **structured JSON output** for intelligent resume-JD matching.

## Endpoint

```http
POST /api/analyze
Content-Type: application/json
```

## Request Body

```json
{
  "resume_text": "Your extracted resume text here...",
  "job_description": "Job description text here..."
}
```

## Response Schema

```json
{
  "match_score": 72,
  "missing_keywords": ["Docker", "System Design", "Kubernetes"],
  "section_feedback": {
    "Summary": "Too generic, lacks role alignment",
    "Experience": "Strong impact but missing metrics",
    "Skills": "Needs cloud technologies"
  }
}
```

## Response Fields

### `match_score` (integer, 0-100)
- Numerical score indicating how well the resume matches the job description
- Based on keyword matches, experience alignment, and skill coverage
- Higher score = better match

### `missing_keywords` (array of strings)
- Critical keywords and technologies from the JD that are missing in the resume
- Helps candidates identify gaps to address
- Typically 5-10 most important missing terms

### `section_feedback` (object)
- **Summary**: Actionable feedback on the summary/objective section
- **Experience**: Specific suggestions for the experience section
- **Skills**: Recommendations for the skills section
- Each field provides concrete, actionable improvement suggestions

## Example Usage

### Using cURL

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Software Engineer with 5 years experience in Python, FastAPI...",
    "job_description": "Looking for Senior Backend Engineer with Docker, Kubernetes..."
  }'
```

### Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/api/analyze",
    json={
        "resume_text": "Your resume text...",
        "job_description": "Job description..."
    }
)

analysis = response.json()
print(f"Match Score: {analysis['match_score']}")
print(f"Missing Keywords: {analysis['missing_keywords']}")
```

### Using JavaScript/Axios

```javascript
const response = await axios.post('http://localhost:8000/api/analyze', {
  resume_text: 'Your resume text...',
  job_description: 'Job description...'
});

console.log(`Match Score: ${response.data.match_score}`);
console.log('Missing Keywords:', response.data.missing_keywords);
console.log('Feedback:', response.data.section_feedback);
```

## AI Integration

### Current Implementation
- Mock response for development/testing
- Validates output structure before returning

### Production LLM Integration

To integrate a real LLM, update `services/ai_analyzer.py`:

#### OpenAI GPT-4

```python
import openai

def _call_llm(self, prompt: str) -> Dict[str, Any]:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)
```

Add to `requirements.txt`:
```
openai==1.3.0
```

Set environment variable:
```bash
export OPENAI_API_KEY="your-api-key"
```

#### Anthropic Claude

```python
import anthropic

def _call_llm(self, prompt: str) -> Dict[str, Any]:
    client = anthropic.Anthropic(api_key=self.api_key)
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(message.content[0].text)
```

#### Local LLM (Ollama)

```python
import requests

def _call_llm(self, prompt: str) -> Dict[str, Any]:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        }
    )
    return json.loads(response.json()["response"])
```

## Prompt Engineering

The prompt in `_build_analysis_prompt()` is carefully crafted to:

1. **Enforce JSON-only output** - No markdown, no explanations
2. **Provide clear schema** - Exact format specification
3. **Set scoring rules** - Clear criteria for match_score
4. **Demand actionability** - Feedback must be specific and actionable

### Key Prompt Elements

```
- Return ONLY valid JSON (no markdown, no additional text)
- match_score: 0-100 based on keyword matches and alignment
- missing_keywords: 5-10 critical missing terms
- section_feedback: Actionable, specific suggestions
```

## Error Handling

### 400 Bad Request
- Empty resume_text
- Empty job_description

### 500 Internal Server Error
- AI analysis fails
- Invalid output structure from LLM
- API key/authentication issues

## Testing

### Test with sample data:

```bash
# Test endpoint
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Python developer with FastAPI experience",
    "job_description": "Senior Python Engineer needed with Docker and AWS"
  }'
```

Expected response:
```json
{
  "match_score": 72,
  "missing_keywords": ["Docker", "AWS", "System Design"],
  "section_feedback": {
    "Summary": "Add years of experience and seniority level",
    "Experience": "Include specific project achievements",
    "Skills": "Add Docker and AWS cloud technologies"
  }
}
```

## Architecture

```
Client Request
     ↓
POST /api/analyze
     ↓
AnalyzeRequest (Pydantic validation)
     ↓
AIAnalyzer.analyze_resume()
     ↓
Build prompt with resume + JD
     ↓
Call LLM API
     ↓
Parse JSON response
     ↓
Validate output structure
     ↓
Return structured JSON
```

## Future Enhancements

1. **Multiple LLM support** - Allow users to choose LLM provider
2. **Caching** - Cache analysis results for identical resume-JD pairs
3. **Streaming responses** - Real-time feedback as analysis progresses
4. **Custom sections** - Support for additional resume sections
5. **Improvement suggestions** - AI-generated resume rewrite suggestions
6. **ATS simulation** - Mimic actual ATS scoring algorithms

## Notes

- Always validate LLM output structure before returning
- Use environment variables for API keys (never hardcode)
- Consider rate limiting for production
- Log all LLM interactions for debugging
- Monitor token usage and costs
