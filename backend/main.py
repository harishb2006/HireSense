from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import resume, jd

app = FastAPI(title="HireSense API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router)
app.include_router(jd.router)

@app.get("/")
async def root():
    return {"message": "HireSense API is running"}
