"""
mock_data.py
Simulates raw construction-site data that would normally come from
CCTV feeds, site inspection reports, equipment sensors, and weather APIs.

In production this module would be replaced by real integrations.
For Milestone 1, this stands in so the Site Risk Agent has something to work on.
"""

import random
from datetime import datetime, timedelta

random.seed(42)  # reproducible demo data

ZONES = ["Zone A - Foundation", "Zone B - Scaffolding", "Zone C - Electrical",
         "Zone D - Crane Area", "Zone E - Material Storage"]

HAZARD_TYPES = [
    "Fall Hazard", "Unsecured Scaffolding", "Exposed Wiring",
    "Heavy Equipment Proximity", "Blocked Emergency Exit",
    "Unstable Excavation Edge", "Missing Guardrail", "Poor Lighting"
]

EQUIPMENT = ["Crane", "Excavator", "Concrete Mixer", "Scaffolding Rig", "Generator"]


def generate_site_activity_log(num_events: int = 25):
    """Simulates a feed of raw site events (as if pulled from CCTV / IoT sensors)."""
    events = []
    now = datetime.now()
    for i in range(num_events):
        events.append({
            "event_id": f"EVT-{1000+i}",
            "zone": random.choice(ZONES),
            "timestamp": (now - timedelta(minutes=random.randint(0, 480))).isoformat(),
            "equipment_involved": random.choice(EQUIPMENT) if random.random() > 0.4 else None,
            "raw_hazard_flag": random.choice(HAZARD_TYPES) if random.random() > 0.55 else None,
            "environmental_note": random.choice(
                ["High wind", "Heavy rain", "Normal", "Normal", "Normal"]
            ),
        })
    return events


def generate_equipment_status():
    """Simulates equipment health/safety sensor readings."""
    status = []
    for eq in EQUIPMENT:
        status.append({
            "equipment": eq,
            "zone": random.choice(ZONES),
            "operational": random.random() > 0.15,
            "last_inspected_days_ago": random.randint(0, 45),
        })
    return status


# ---------------------------------------------------------------------------
# Milestone 2: Safety Agent mock data (worker monitoring / PPE compliance)
# ---------------------------------------------------------------------------

WORKER_NAMES = [
    "R. Kumar", "S. Patel", "A. Sharma", "M. Iyer", "V. Reddy",
    "K. Nair", "P. Singh", "D. Rao", "N. Gupta", "T. Menon",
    "J. Das", "L. Verma"
]

PPE_ITEMS = ["Hard Hat", "Safety Vest", "Safety Boots", "Protective Gloves", "Safety Harness"]

UNSAFE_BEHAVIORS = [
    "Working at height without harness",
    "Standing under suspended load",
    "Bypassing machine guard",
    "Smoking in restricted zone",
    "Using phone while operating equipment",
    "Ignoring barricade/warning tape",
]


def generate_worker_activity_log(num_workers: int = 12):
    """Simulates worker presence + PPE sensor / camera detections for the day."""
    workers = []
    for i in range(num_workers):
        name = WORKER_NAMES[i % len(WORKER_NAMES)]
        zone = random.choice(ZONES)
        # Randomly decide which PPE items this worker is missing (most workers fully compliant)
        missing_ppe = [item for item in PPE_ITEMS if random.random() < 0.12]
        unsafe_behavior = random.choice(UNSAFE_BEHAVIORS) if random.random() < 0.15 else None

        workers.append({
            "worker_id": f"W-{200 + i}",
            "name": name,
            "zone": zone,
            "missing_ppe": missing_ppe,
            "unsafe_behavior": unsafe_behavior,
            "hours_on_site_today": round(random.uniform(1, 9), 1),
        })
    return workers
