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

    assert "stations" in data
    assert len(data["stations"])==2
    assert data["stations"][0]["station_id"] == "1029TH"
    assert data["stations"][1]["catchment_name"] == "Welland"