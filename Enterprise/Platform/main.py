"""
AAP Enterprise Data Plane API.

This module serves as the commercial feature materialisation store. It handles
incoming telemetry, serves dynamic accessibility patches to the client engine,
and provides datasets for downstream LLM fine-tuning pipelines.
"""

import json
import os
from typing import Dict, List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

# --- Configuration & State ---
app = FastAPI(title="AAP Enterprise Data Plane")
# FIX: Go up two levels to save the DB in the root 'app' folder
DB_PATH = "../../mock_feature_store.json"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class TraceIngest(BaseModel):
    """Schema for incoming client interaction telemetry."""
    url: str
    eventType: str
    targetSelector: str
    currentRole: str
    declaredIntent: Optional[str] = None

# --- Database Utilities ---
def init_db() -> None:
    """Initialises the local JSON database if it does not exist."""
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump({"materialized_features": {}, "telemetry_logs": []}, f)

def get_db() -> Dict:
    """Retrieves the current state of the JSON database."""
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data: Dict) -> None:
    """Persists the updated database dictionary to the filesystem."""
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

@app.on_event("startup")
def startup() -> None:
    """Lifecyle event to ensure database is ready on boot."""
    init_db()

# --- API Endpoints ---
@app.get("/static/v1.jsonld")
def serve_standard_schema() -> FileResponse:
    """Serves the canonical AAP vocabulary schema for global reference."""
    # FIX: Go up two levels and match the capital 'V' in V1.jsonld
    schema_path = os.path.abspath("../../Open_Standard/Vocabulary/V1.jsonld")
    return FileResponse(schema_path, media_type="application/ld+json")

@app.get("/demo/aap", response_class=HTMLResponse)
def serve_aap_page() -> str:
    """Serves the standard-compliant test harness page."""
    # FIX: Go up two levels and match the 'app.html' filename
    html_path = os.path.abspath("../../Open_Source_Engine/test-harness/app.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/v1/trace")
def process_trace(payload: TraceIngest) -> Dict:
    """Ingests interaction telemetry and determines if structural patches are required."""
    db = get_db()
    db["telemetry_logs"].append(payload.model_dump())
    
    feature_key = f"{payload.url}::{payload.targetSelector}"
    patches = []
    
    # Materialised feature lookup
    if feature_key in db["materialized_features"]:
        patches.append(db["materialized_features"][feature_key])
    # Heuristic patching based on declared intent vs. poor structural markup
    elif payload.declaredIntent == "submit_payment" and payload.currentRole == "div":
        patches.append({
            "selector": payload.targetSelector,
            "corrected_role": "button",
            "corrected_label": "Submit Payment Confirmation"
        })
        
    save_db(db)
    return {"status": "processed", "active_patches": patches}

@app.get("/api/v1/export/golden-pairs")
def export_alignment_data() -> List[Dict]:
    """Transforms raw telemetry into conversational pairs for LLM fine-tuning."""
    db = get_db()
    golden_pairs = []
    
    for log in db["telemetry_logs"]:
        if log.get("declaredIntent") == "submit_payment" and log.get("currentRole") == "div":
            golden_pairs.append({
                "user_prompt": f"Generate an item for user intent: {log['declaredIntent']}",
                "naive_output": f"<{log['currentRole']} id='{log['targetSelector']}'>Pay</{log['currentRole']}>",
                "accessible_output": "<button type='button' aria-label='Confirm payment transaction'>Pay</button>"
            })
            
    return golden_pairs