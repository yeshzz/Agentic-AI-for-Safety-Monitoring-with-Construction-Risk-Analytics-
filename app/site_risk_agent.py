"""
site_risk_agent.py
Milestone 1 deliverable: Site Risk Agent

Responsibilities (per project spec):
 - Monitor construction site activities
 - Detect unsafe site conditions
 - Assess environmental risks
 - Identify equipment-related hazards
 - Generate site risk scores

NOTE ON DESIGN CHOICE:
This is implemented as a deterministic rule engine rather than an LLM call.
This is intentional for Milestone 1 — it's fast, free, reproducible, and
demo-safe. The Construction Risk Intelligence Engine (Milestone 4) is where
LLM reasoning gets layered on top to generate natural-language
recommendations from these structured findings. Mention this design
rationale in your demo if asked "where's the AI/LLM part?".
"""

from datetime import datetime
from app.mock_data import generate_site_activity_log, generate_equipment_status

# Severity weights used for scoring
HAZARD_SEVERITY = {
    "Fall Hazard": 9,
    "Unstable Excavation Edge": 9,
    "Exposed Wiring": 8,
    "Missing Guardrail": 7,
    "Blocked Emergency Exit": 8,
    "Unsecured Scaffolding": 7,
    "Heavy Equipment Proximity": 6,
    "Poor Lighting": 4,
}

ENV_RISK_WEIGHT = {
    "High wind": 5,
    "Heavy rain": 6,
    "Normal": 0,
}


def detect_hazards(events):
    """Scan raw site events and flag structured hazard detections."""
    detected = []
    for e in events:
        if e["raw_hazard_flag"]:
            detected.append({
                "event_id": e["event_id"],
                "zone": e["zone"],
                "hazard_type": e["raw_hazard_flag"],
                "severity": HAZARD_SEVERITY.get(e["raw_hazard_flag"], 5),
                "timestamp": e["timestamp"],
            })
    return detected


def assess_environmental_risk(events):
    """Look at environmental notes attached to site events."""
    risky = [e for e in events if e["environmental_note"] != "Normal"]
    total_weight = sum(ENV_RISK_WEIGHT.get(e["environmental_note"], 0) for e in risky)
    return {
        "flagged_events": len(risky),
        "risk_weight": total_weight,
        "conditions": list({e["environmental_note"] for e in risky}),
    }


def identify_equipment_hazards(equipment_status):
    """Flag equipment that's non-operational or overdue for inspection."""
    flagged = []
    for eq in equipment_status:
        issues = []
        if not eq["operational"]:
            issues.append("Non-operational / malfunctioning")
        if eq["last_inspected_days_ago"] > 30:
            issues.append(f"Overdue inspection ({eq['last_inspected_days_ago']}d)")
        if issues:
            flagged.append({
                "equipment": eq["equipment"],
                "zone": eq["zone"],
                "issues": issues,
            })
    return flagged


def compute_site_risk_score(hazards, env_risk, equipment_hazards):
    """
    Weighted composite risk score, normalized 0-100.
    Higher = riskier. Mirrors the 'Site Risk Score' shown in the spec's dashboard.
    """
    hazard_score = sum(h["severity"] for h in hazards)
    equipment_score = len(equipment_hazards) * 6
    env_score = env_risk["risk_weight"]

    raw = hazard_score + equipment_score + env_score
    score = min(100, max(0, round(raw / 2.2)))  # normalized so demo scores land ~40-85
    return score


def classify_zones_by_risk(hazards):
    """Aggregate hazard count per zone -> used for the risk heatmap panel."""
    zone_counts = {}
    for h in hazards:
        zone_counts[h["zone"]] = zone_counts.get(h["zone"], 0) + 1
    high_risk_zones = [z for z, c in zone_counts.items() if c >= 2]
    return zone_counts, high_risk_zones


def run_site_risk_agent():
    """
    Main entry point for the Site Risk Agent.
    Pulls (mock) data, runs detection + scoring, returns a structured result
    that the dashboard/API layer can serve directly.
    """
    events = generate_site_activity_log()
    equipment_status = generate_equipment_status()

    hazards = detect_hazards(events)
    env_risk = assess_environmental_risk(events)
    equipment_hazards = identify_equipment_hazards(equipment_status)
    zone_counts, high_risk_zones = classify_zones_by_risk(hazards)
    risk_score = compute_site_risk_score(hazards, env_risk, equipment_hazards)

    return {
        "generated_at": datetime.now().isoformat(),
        "site_risk_score": risk_score,
        "active_hazards": len(hazards),
        "high_risk_zones": high_risk_zones,
        "hazards_detected": hazards,
        "environmental_risk": env_risk,
        "equipment_hazards": equipment_hazards,
        "zone_hazard_counts": zone_counts,
    }
