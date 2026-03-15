from flask import Blueprint, jsonify, request
from src.api.database import fetch_patients, fetch_vitals, fetch_anomalies

api_bp = Blueprint("api", __name__)

@api_bp.route("/patients", methods=["GET"])
def get_patients():
    """Endpoint to list unique patient IDs."""
    try:
        patients = fetch_patients()
        return jsonify({"status": "success", "data": patients})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route("/vitals/<patient_id>", methods=["GET"])
def get_patient_vitals(patient_id):
    """Endpoint to get recent vitals for a specific patient."""
    try:
        limit = request.args.get("limit", 100, type=int)
        vitals = fetch_vitals(patient_id, limit)
        return jsonify({"status": "success", "patient_id": patient_id, "data": vitals})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route("/anomalies", methods=["GET"])
def get_recent_anomalies():
    """Endpoint to get recent anomaly events."""
    try:
        limit = request.args.get("limit", 50, type=int)
        anomalies = fetch_anomalies(limit)
        return jsonify({"status": "success", "data": anomalies})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route("/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "healthy", "service": "healthcare-anomaly-detection-api"})
