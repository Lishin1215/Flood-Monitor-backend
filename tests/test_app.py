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
                "notation" : "F1906-level-stage-i-15_min-m" ,
                "parameter" : "level" ,
                "parameterName" : "Water Level" ,
                "period" : 900 ,
                "qualifier" : "Stage" ,
                "station" : "http://environment.data.gov.uk/flood-monitoring/id/stations/F1906" ,
                "stationReference" : "F1906"
            },
            {
                "notation" : "F1906-flow-logged-i-15_min-m3_s" ,
                "parameter" : "flow" ,
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
    assert data["measurements"][0]["notation"] == "F1906-level-stage-i-15_min-m"
    assert data["measurements"][0]["hasData"] is True
    assert data["measurements"][1]["parameterName"] == "Flow"
    assert data["measurements"][1]["qualifier"] == "Logged"
    assert data["measurements"][1]["notation"] == "F1906-flow-logged-i-15_min-m3_s"
    assert data["measurements"][1]["hasData"] is False


@patch("services.flood_info_service.FloodInfoService.get_particular_M")
def test_get_particular_M_success(mock_get_particular_M, client):
    mock_get_particular_M.return_value = {
        "items": [
            {
                "@id" : "http://environment.data.gov.uk/flood-monitoring/data/readings/1029TH-level-stage-i-15_min-mASD/2025-03-06T22-30-00Z" ,
                "dateTime" : "2025-03-06T22:30:00Z" ,
                "measure" : "http://environment.data.gov.uk/flood-monitoring/id/measures/1029TH-level-stage-i-15_min-mASD" ,
                "value" : 0.284
            },
            {
                "@id" : "http://environment.data.gov.uk/flood-monitoring/data/readings/1029TH-level-stage-i-15_min-mASD/2025-03-06T22-15-00Z" ,
                "dateTime" : "2025-03-06T22:15:00Z" ,
                "measure" : "http://environment.data.gov.uk/flood-monitoring/id/measures/1029TH-level-stage-i-15_min-mASD" ,
                "value" : 0.285  
            }
        ]
    }

    response = client.get("/get-particular-M/1029TH-level-stage-i-15_min-mASD")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "readings" in data
    assert len(data["readings"])==2
    assert data["hasData"] is True
    assert data["readings"][0]["dateTime"] == "2025-03-06T22:30:00Z"
    assert data["readings"][0]["value"] == 0.284
    assert data["readings"][1]["dateTime"] == "2025-03-06T22:15:00Z"
    assert data["readings"][1]["value"] == 0.285


@patch("services.flood_info_service.FloodInfoService.get_particular_M")
def test_get_particular_M_no_data(mock_get_particular_M, client):
    mock_get_particular_M.return_value = {
        "items": []
    }

    response = client.get("/get-particular-M/F1906-flow-logged-i-15_min-m3_s")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "readings" in data
    assert data["hasData"] is False
    assert len(data["readings"]) == 0