from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/get-stations", methods=["GET"])
def get_stations():
    pass


@app.route("/get-measurement/<station_id>", methods=["GET"])
def get_measurement(station_id):
    pass


@app.route("/get-particular-M", methods=["GET"])
def get_particular_M(): 
    station_id = request.args.get("station-id")
    measurement = request.args.get("measurement")
    qualifier = request.args.get("qualifier")
    pass
        