import requests
import logging
import redis
import json
from datetime import datetime, timedelta
import sentry_sdk


class FloodInfoService:
    API_URL = "https://environment.data.gov.uk/flood-monitoring"
    redis_client = None
    

    def __init__(self):
        try:
            self.redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
            self.redis_client.ping()
        except redis.ConnectionError as e:
            self.redis_client = None

    def get_stations(self):
        cache_key = "stations_data"
        if self.redis_client:
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
            
        try:
            response = requests.get(self.API_URL + "/id/stations")
            response.raise_for_status()
            data = response.json()

            if self.redis_client:
                self.redis_client.setex(cache_key, timedelta(hours=24), json.dumps(data))


            return data
        except requests.RequestException as e:
            # logging.error(f"API request failed: {str(e)}")
            sentry_sdk.capture_exception(e)
            raise Exception("API request failed")
        

    def get_measurement(self, station_id):
        cache_key = f"measurement_{station_id}"
        if self.redis_client:
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        
        try:
            response = requests.get(f"{self.API_URL}/id/stations/{station_id}/measures")
            response.raise_for_status
            data = response.json()
            
            if self.redis_client:
                self.redis_client.setex(cache_key, timedelta(hours=24), json.dumps(data))

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
  

    
    