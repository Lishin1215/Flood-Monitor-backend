import logging
from flask import Flask, jsonify, request
from services.flood_info_service import FloodInfoService

app = Flask(__name__)

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
        logging.error(f"Error in get_stations: {str(e)}")
        return jsonify({"error": "Failed to fetch stations"}), 500


@app.route("/get-measurement/<station_id>", methods=["GET"])
def get_measurement(station_id):
    try:
        data = service.get_measurement(station_id)

        if "error" in data:
            return jsonify(data), 404
        
        if "items" not in data:
            return jsonify({"error": "No measurement data found"}), 404
        
        measurements = [
            {
                "parameterName": measure.get("parameterName", "Unknown"),
                "qualifier": measure.get("qualifier", "Unknown")
            }
            for measure in data["items"]
        ]

        return jsonify({"measurements": measurements})
    except Exception as e:
        logging.error(f"Error in get_measurement: {str(e)}")
        return jsonify({"error": "Failed to fetch measurement data"}), 500


@app.route("/get-particular-M", methods=["GET"])
def get_particular_M(): 
    station_id = request.args.get("station-id")
    measurement = request.args.get("measurement")
    qualifier = request.args.get("qualifier")
    pass
        