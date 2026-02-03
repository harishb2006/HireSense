from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import resume, jd, rewriter, mock_interview
from contextlib import asynccontextmanager
from database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Database is already initialized via Docker init.sql
    yield
    # Shutdown: Close database connections
    await close_db()


app = FastAPI(title="HireSense API", lifespan=lifespan)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local Vite dev server
        "http://localhost:4173",  # Local Vite preview
        "https://hire-sense-sigma.vercel.app",  # Vercel production
        "https://hire-sense-63teo8xko-harishs-projects-605e156a.vercel.app",  # Vercel preview
        "*",  # Allow all origins (for development - remove in production if needed)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router)
app.include_router(jd.router)
app.include_router(rewriter.router)
app.include_router(mock_interview.router)

@app.get("/")
async def root():
    return {"message": "HireSense Prep Pro API is running"}
