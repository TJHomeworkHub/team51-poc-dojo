#!/opt/pwn.college/python
"""
appointment_api.py - Appointment API Endpoints
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from flask import Flask, jsonify, request, abort
import threading
import time

from validators import validate_patient_name, validate_patient_email, validate_phone_number, validate_appointment_date, validate_appointment_time

app = Flask(__name__)

# --- In-memory data model ---------------------------------------------------
@dataclass
class Appointment:
    id: int
    patient_name: str
    patient_email: str
    phone_number: str
    appointment_date: str
    appointment_time: str
    reason: str
    notes: Optional[str] = None

_store: List[Appointment] = []
_next_id = 1


def _get_next_id() -> int:
    global _next_id
    _id = _next_id
    _next_id += 1
    return _id


def _find_appointment(aid: int) -> Optional[Appointment]:
    for a in _store:
        if a.id == aid:
            return a
    return None


# --- Routes ----------------------------------------------------------------
@app.get("/")
def index():
    return jsonify({"service": "appointment-api", "status": "ok"}), 200


@app.post("/api/appointments")
def create_appointment():
    """
    Expected JSON body:
    {
        "patient_name": "John Doe",
        "patient_email": "john@example.com",
        "phone_number": "555-123-4567",
        "appointment_date": "2025-12-20",
        "appointment_time": "14:30",
        "reason": "Annual checkup",
        "notes": "Optional notes"
    }
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Validate patient_name using the validators module
    name = data.get("patient_name")
    ok, msg = validate_patient_name(name)
    if not ok:
        return jsonify({"error": msg}), 400

    # Validate patient_email using the validators module
    email = data.get("patient_email")
    ok, msg = validate_patient_email(email)
    if not ok:
        return jsonify({"error": msg}), 400

    # Validate phone_number using the validators module
    pnum = data.get("phone_number")
    ok, msg = validate_phone_number(pnum)
    if not ok:
        return jsonify({"error": msg}), 400

    # Validate appointment_date using the validators module
    date = data.get("appointment_date")
    ok, msg = validate_appointment_date(date)
    if not ok:
        return jsonify({"error": msg}), 400

    # Validate appointment_time using the validators module
    tm = data.get("appointment_time")
    ok, msg = validate_appointment_time(tm)
    if not ok:
        return jsonify({"error": msg}), 400

    appt = Appointment(
        id=_get_next_id(),
        patient_name=name.strip(),
        patient_email=email.strip(),
        phone_number=pnum.strip(),
        appointment_date=date.strip(),
        appointment_time=tm.strip(),
        reason=str(data.get("reason", "")).strip(),
        notes=(str(data.get("notes")).strip() if data.get("notes") is not None else None),
    )
    _store.append(appt)
    return jsonify({"id": appt.id, "appointment": asdict(appt)}), 201


@app.get("/api/appointments/<int:appointment_id>")
def get_appointment(appointment_id: int):
    appt = _find_appointment(appointment_id)
    if appt is None:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify(asdict(appt)), 200


@app.get("/api/appointments/search")
def search_appointments():
    """
    Query parameter: ?name=<query>
    Performs a case-insensitive substring match on patient_name.
    This endpoint simulates the search functionality.
    """
    q = request.args.get("name", "")
    if not isinstance(q, str) or q.strip() == "":
        return jsonify({"error": "Provide a non-empty 'name' query parameter"}), 400

    q_lower = q.strip().lower()
    results = [asdict(a) for a in _store if q_lower in a.patient_name.lower()]
    return jsonify({"count": len(results), "results": results}), 200

@app.post("/api/appointments/<int:appointment_id>/notes")
def add_notes(appointment_id: int):
    """
    Adds/overwrites notes for an appointment. Notes are optional and not validated
    in this incremental challenge.
    """
    appt = _find_appointment(appointment_id)
    if appt is None:
        return jsonify({"error": "Appointment not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    body = request.get_json()
    notes = body.get("notes")

    appt.notes = None if notes is None else str(notes)
    return jsonify({"id": appt.id, "notes": appt.notes}), 200


def _seed_sample_data():
    sample = Appointment(
        id=_get_next_id(),
        patient_name="Alice Example",
        patient_email="alice@example.org",
        phone_number="555-000-1111",
        appointment_date="2099-01-01",
        appointment_time="09:00",
        reason="Initial sample appointment",
        notes=None,
    )
    _store.append(sample)


# --- Entrypoint -------------------------------------------------------------
def run_server():
    if not _store:
        _seed_sample_data()

    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    run_server()
