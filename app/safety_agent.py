"""
safety_agent.py
Milestone 2 deliverable: Safety Agent

Responsibilities (per project spec):
 - Monitor worker safety compliance
 - Detect PPE violations
 - Identify unsafe worker behavior
 - Analyze accident-prone zones
 - Generate safety recommendations

Same design philosophy as the Site Risk Agent (Milestone 1): rule-based,
deterministic, fast to demo. This keeps every agent's output structured and
comparable, which matters later when the Risk Intelligence Engine (Milestone 4)
needs to combine findings from all four agents.
"""

from datetime import datetime
from app.mock_data import generate_worker_activity_log

# Severity weights for missing PPE items (some are more critical than others)
PPE_SEVERITY = {
    "Safety Harness": 9,   # working-at-height protection - most critical
    "Hard Hat": 8,
    "Safety Boots": 6,
    "Safety Vest": 5,
    "Protective Gloves": 4,
}

UNSAFE_BEHAVIOR_SEVERITY = {
    "Working at height without harness": 10,
    "Standing under suspended load": 9,
    "Bypassing machine guard": 8,
    "Ignoring barricade/warning tape": 7,
    "Using phone while operating equipment": 7,
    "Smoking in restricted zone": 5,
}


def detect_ppe_violations(workers):
    """Flag every missing PPE item per worker as a structured violation."""
    violations = []
    for w in workers:
        for item in w["missing_ppe"]:
            violations.append({
                "worker_id": w["worker_id"],
                "worker_name": w["name"],
                "zone": w["zone"],
                "missing_item": item,
                "severity": PPE_SEVERITY.get(item, 5),
            })
    return violations


def detect_unsafe_behavior(workers):
    """Flag workers observed engaging in unsafe behavior."""
    flagged = []
    for w in workers:
        if w["unsafe_behavior"]:
            flagged.append({
                "worker_id": w["worker_id"],
                "worker_name": w["name"],
                "zone": w["zone"],
                "behavior": w["unsafe_behavior"],
                "severity": UNSAFE_BEHAVIOR_SEVERITY.get(w["unsafe_behavior"], 6),
            })
    return flagged


def analyze_accident_prone_zones(ppe_violations, unsafe_behaviors):
    """Aggregate PPE + behavior issues per zone to identify accident-prone areas."""
    zone_issue_count = {}
    for v in ppe_violations:
        zone_issue_count[v["zone"]] = zone_issue_count.get(v["zone"], 0) + 1
    for b in unsafe_behaviors:
        zone_issue_count[b["zone"]] = zone_issue_count.get(b["zone"], 0) + 1

    accident_prone = [z for z, c in zone_issue_count.items() if c >= 2]
    return zone_issue_count, accident_prone


def compute_safety_score(total_workers, ppe_violations, unsafe_behaviors):
    """
    Composite safety score, 0-100, HIGHER = SAFER (inverse of risk score).
    Starts at 100 and deducts points for violations, weighted by severity.
    """
    if total_workers == 0:
        return 100

    ppe_penalty = sum(v["severity"] for v in ppe_violations) * 0.35
    behavior_penalty = sum(b["severity"] for b in unsafe_behaviors) * 0.6

    score = 100 - (ppe_penalty + behavior_penalty)
    return max(0, min(100, round(score)))


def generate_safety_recommendations(ppe_violations, unsafe_behaviors, accident_prone_zones):
    """Simple templated recommendations based on what was detected."""
    recs = []
    if any(v["missing_item"] == "Safety Harness" for v in ppe_violations):
        recs.append("Immediate harness check required for all height-work crews.")
    if any(b["severity"] >= 9 for b in unsafe_behaviors):
        recs.append("Stop-work order recommended for critical unsafe behaviors detected today.")
    if accident_prone_zones:
        recs.append(f"Increase supervision in: {', '.join(accident_prone_zones)}.")
    if len(ppe_violations) > 3:
        recs.append("Conduct a site-wide PPE compliance briefing before next shift.")
    if not recs:
        recs.append("No critical safety actions required. Continue routine monitoring.")
    return recs


def run_safety_agent():
    """
    Main entry point for the Safety Agent.
    Pulls (mock) worker data, runs PPE + behavior detection, zone analysis,
    scoring, and recommendations. Returns a structured result for the dashboard/API.
    """
    workers = generate_worker_activity_log()

    ppe_violations = detect_ppe_violations(workers)
    unsafe_behaviors = detect_unsafe_behavior(workers)
    zone_issue_count, accident_prone_zones = analyze_accident_prone_zones(
        ppe_violations, unsafe_behaviors
    )
    safety_score = compute_safety_score(len(workers), ppe_violations, unsafe_behaviors)
    recommendations = generate_safety_recommendations(
        ppe_violations, unsafe_behaviors, accident_prone_zones
    )

    ppe_compliance_rate = round(
        100 * (1 - len(ppe_violations) / max(1, len(workers) * len(PPE_SEVERITY))), 1
    )

    return {
        "generated_at": datetime.now().isoformat(),
        "workers_monitored": len(workers),
        "safety_score": safety_score,
        "ppe_compliance_rate": ppe_compliance_rate,
        "ppe_violations": ppe_violations,
        "unsafe_behaviors": unsafe_behaviors,
        "accident_prone_zones": accident_prone_zones,
        "zone_issue_count": zone_issue_count,
        "recommendations": recommendations,
    }
