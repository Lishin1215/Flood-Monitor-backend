import requests
import logging
from datetime import datetime, timedelta
import sentry_sdk


class FloodInfoService:
    API_URL = "https://environment.data.gov.uk/flood-monitoring"
    

    def get_stations(self):
        try:
            response = requests.get(self.API_URL + "/id/stations")
            response.raise_for_status()
            data = response.json()

            return data
        except requests.RequestException as e:
            # logging.error(f"API request failed: {str(e)}")
            sentry_sdk.capture_exception(e)
            raise Exception("API request failed")
        

    def get_measurement(self, station_id):
        try:
            response = requests.get(f"{self.API_URL}/id/stations/{station_id}/measures")
            response.raise_for_status
            data = response.json()

            return data
        except requests.RequestException as e:
            # logging.error(f"API request failed for station {station_id}: {str(e)}")
            sentry_sdk.capture_exception(e)
            return {"error":"API request failed"}
        
    
    def get_particular_M(self, notation):
        try:
            since_time = (datetime.utcnow() - timedelta(hours=24)).isoformat() + "Z" 
            response = requests.get(f"{self.API_URL}/id/measures/{notation}/readings", params={"since": since_time})
            response.raise_for_status
            data = response.json()

            return data
        except requests.RequestException as e:
            # logging.error(f"API request failed for station {notation}: {str(e)}")
            sentry_sdk.capture_exception(e)
            return {"error": "API request failed"}




f = FloodInfoService()
# print(f.get_stations())
# print(f.get_measurement(station_id="1029TH"))
print(f.get_particular_M(notation = "F1906-flow-logged-i-15_min-m3_s"))
  

    
    