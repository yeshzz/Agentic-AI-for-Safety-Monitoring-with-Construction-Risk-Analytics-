"""
main.py
FastAPI entrypoint for BuildSure AI - Milestone 1
(Site Risk Monitoring & Hazard Detection)

Run with:
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/  -> dashboard
API docs at http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from app.site_risk_agent import run_site_risk_agent
from app.safety_agent import run_safety_agent

app = FastAPI(title="BuildSure AI - Site Risk Monitoring (Milestone 1)")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def serve_dashboard():
    return FileResponse(os.path.join(STATIC_DIR, "dashboard.html"))


@app.get("/api/site-risk")
def get_site_risk():
    """
    Core Milestone 1 endpoint.
    Runs the Site Risk Agent and returns hazard detections + risk score.
    """
    return run_site_risk_agent()


@app.get("/api/safety")
def get_safety_status():
    """
    Milestone 2 endpoint.
    Runs the Safety Agent and returns PPE compliance, unsafe behavior,
    accident-prone zones, and safety recommendations.
    """
    return run_safety_agent()


@app.get("/api/health")
def health_check():
    return {"status": "ok", "agents": ["Site Risk Agent", "Safety Agent"], "milestone": 2}
