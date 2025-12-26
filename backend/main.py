from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import resume, jd, interview, rewriter

app = FastAPI(title="HireSense API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local Vite dev server
        "http://localhost:4173",  # Local Vite preview
        "https://hire-sense-63teo8xko-harishs-projects-605e156a.vercel.app",  # Vercel deployment
        "https://*.vercel.app",  # All Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router)
app.include_router(jd.router)
app.include_router(interview.router)
app.include_router(rewriter.router)

@app.get("/")
async def root():
    return {"message": "HireSense API is running"}
