from flask import Blueprint, request, jsonify
from .db import CloudSQLClient
from datetime import datetime
import os

bp = Blueprint("routes", __name__)

DB_CONFIG = {
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB"),
    "connection_name": os.getenv("MYSQL_CONNECTION_NAME"),
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
}

TABLE_NAME = os.getenv("MYSQL_FIRMS_TABLE", "firms")
db_client = CloudSQLClient(DB_CONFIG)

@bp.route("/uru_training_data", methods=["GET"])
def get_uru_training_data():

    results = db_client.fetch_table_to_geojson("training_uruguay_fire")

    return jsonify({"count": len(results), "data": results}), 200


@bp.route("/firms", methods=["GET"])
def get_firms():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    fire = request.args.get("fire", "true").lower() == "true"  # opcional, por defecto True

    if not start_date or not end_date:
        return jsonify({"error": "start_date y end_date son obligatorios"}), 400

    try:
        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    try:
        results = db_client.fetch_between_dates(
            table=TABLE_NAME,
            start_date=start_date,
            end_date=end_date,
            fire=fire
        )
        return jsonify({"count": len(results), "data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
