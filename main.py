from fastapi import FastAPI
from routes import resume, jd

app = FastAPI(title="HireSense API")

app.include_router(resume.router)
app.include_router(jd.router)
