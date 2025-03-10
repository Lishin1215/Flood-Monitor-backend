import logging
from flask import Flask, jsonify, request
from services.flood_info_service import FloodInfoService
from flask_cors import CORS
import sentry_sdk
from dotenv import load_dotenv
import os

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    send_default_pii=True,
)

app = Flask(__name__)
CORS(app)
service = FloodInfoService()

@app.route("/get-stations", methods=["GET"])
def get_stations():
    try:
        data = service.get_stations()

        if not data or "items" not in data:
            return jsonify({"error": "Invalid API response"}), 500

        station_catchments = [
            {
                "station_id": station.get("@id", "Unknown").split("/")[-1],
                "catchment_name": station.get("catchmentName", "Unknown")
            }
            for station in data["items"]
        ]

        return jsonify({"stations": station_catchments})
    except Exception as e:
        # logging.error(f"Error in get_stations: {str(e)}")
        sentry_sdk.capture_exception(e)
        return jsonify({"error": "Failed to fetch stations"}), 500


@app.route("/get-measurement/<station_id>", methods=["GET"])
def get_measurement(station_id):
    try:
        data = service.get_measurement(station_id)
        
        if "items" not in data:
            return jsonify({"error": "No measurement data found"}), 404
        
        measurements = []
        for measure in data["items"]:
            notation = measure.get("notation", "Unknown")

            #check if each measure has "readings"
            readings_data = service.get_particular_M(notation)

            has_data = bool(readings_data.get("items"))
        
            measurements.append({
                    "parameterName": measure.get("parameterName", "Unknown"),
                    "qualifier": measure.get("qualifier", "Unknown"),
                    "notation": notation,
                    "hasData": has_data
            })

        return jsonify({"measurements": measurements})
    except Exception as e:
        # logging.error(f"Error in get_measurement: {str(e)}")
        sentry_sdk.capture_exception(e)
        return jsonify({"error": "Failed to fetch measurement data"}), 500


@app.route("/get-particular-M/<notation>", methods=["GET"])
def get_particular_M(notation): 
    try:
        data = service.get_particular_M(notation)

        if "items" not in data or not data["items"]:
            return jsonify({"readings": [], "hasData": False})
        
        readings = [
            {
                "dateTime": reading.get("dateTime", "Unknown"),
                "value": reading.get("value", "Unknown")
            }
            for reading in data["items"]
        ]

        return jsonify({"readings": readings, "hasData": True})
    except Exception as e:
        # logging.error(f"Error in get_particular_M: {str(e)}")
        sentry_sdk.capture_exception(e)
        return jsonify({"error": "Failed to fetch measurement data"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


    
        