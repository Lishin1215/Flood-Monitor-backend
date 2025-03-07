import pytest
import json
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("services.flood_info_service.FloodInfoService.get_stations")
def test_get_stations_success(mock_get_stations, client):
    mock_get_stations.return_value = {
        "items": [
            {
                "@id": "http://environment.data.gov.uk/flood-monitoring/id/stations/1029TH",
                "catchmentName": "Cotwolds"
            },
            {
                "@id": "http://environment.data.gov.uk/flood-monitoring/id/stations/E2043",
                "catchmentName": "Welland"
            }
        ]
    }

    response = client.get("/get-stations")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "stations" in data
    assert len(data["stations"])==2
    assert data["stations"][0]["station_id"] == "1029TH"
    assert data["stations"][1]["catchment_name"] == "Welland"


@patch("services.flood_info_service.FloodInfoService.get_measurement")
def test_get_measurement_success(mock_get_measurement, client):
    mock_get_measurement.return_value = {
        "items": [
            {
                "parameterName" : "Water Level" ,
                "period" : 900 ,
                "qualifier" : "Stage" ,
                "station" : "http://environment.data.gov.uk/flood-monitoring/id/stations/F1906" ,
                "stationReference" : "F1906" 
            },
            {
                "parameterName" : "Flow" ,
                "period" : 900 ,
                "qualifier" : "Logged" ,
                "station" : "http://environment.data.gov.uk/flood-monitoring/id/stations/F1906" , 
                "stationReference" : "F1906" 
            }
        ]
    }

    response = client.get("/get-measurement/F1906")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "measurements" in data
    assert len(data["measurements"])==2
    assert data["measurements"][0]["parameterName"] == "Water Level"
    assert data["measurements"][0]["qualifier"] == "Stage"
    assert data["measurements"][1]["parameterName"] == "Flow"
    assert data["measurements"][1]["qualifier"] == "Logged"

