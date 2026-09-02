# BuildSure AI — Milestone 1: Site Risk Monitoring & Hazard Detection

## How to run (VS Code / terminal)

```bash
cd buildsure-ai
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open **http://127.0.0.1:8000/** for the dashboard.
API docs (Swagger): **http://127.0.0.1:8000/docs**

The dashboard auto-refreshes every 15 seconds to simulate live monitoring.

## What's implemented (maps to Milestone 1 evaluation criteria)

| Requirement | Where it lives |
|---|---|
| Site risk monitoring operational | `app/mock_data.py` simulates a continuous feed of site activity + equipment sensor data |
| Hazard detection functioning | `app/site_risk_agent.py` → `detect_hazards()`, `assess_environmental_risk()`, `identify_equipment_hazards()` |
| Site risk dashboard available | `app/static/dashboard.html`, served at `/` — KPIs, hazard panel, zone risk bars, equipment flags |

## Architecture (mini version of the full spec)

```
Mock Site Data (CCTV/IoT stand-in)
        ↓
Site Risk Agent (rule engine: hazard detection, env risk, equipment checks)
        ↓
Risk Scoring (0-100 composite score)
        ↓
FastAPI /api/site-risk endpoint
        ↓
Dashboard (auto-refreshing HTML/JS)
```

## Design decisions to mention in your demo

1. **Why rule-based, not an LLM call, for this milestone?**
   The Site Risk Agent uses deterministic scoring logic instead of calling an LLM.
   This keeps it fast, reproducible, and free to demo repeatedly. The natural-language
   reasoning layer (LLM-based recommendations) is planned for the Construction Risk
   Intelligence Engine in Milestone 4, once outputs from all agents (Safety, Compliance,
   Insurance) need to be synthesized together.

2. **Why mock data?**
   Real CCTV/IoT integration is out of scope for Week 1-2. `mock_data.py` is built as
   an isolated module so it's a drop-in replacement point later — swap it for a real
   data source without touching the agent logic.

3. **Risk scoring formula** is transparent and tunable (severity-weighted hazards +
   equipment flags + environmental conditions, normalized to 0-100) — easy to explain
   if asked how the score is derived.

## Next milestones (per project plan)
- Milestone 2 (Wk 3-4): Safety Agent — PPE violation detection
- Milestone 3 (Wk 5-6): Compliance Agent + Insurance Agent
- Milestone 4 (Wk 7-8): Reporting Agent + Risk Intelligence Engine + full orchestration
