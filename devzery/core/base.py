import threading
import requests
import json
import time

class BaseDevzeryMiddleware:
    def __init__(self, api_endpoint=None, api_key=None, source_name=None):
        self.api_endpoint = api_endpoint or "https://server-v3-7qxc7hlaka-uc.a.run.app/api/add"
        self.api_key = api_key
        self.source_name = source_name

    def send_data_to_api_sync(self, data, response_content):
        try:
            if (self.api_key and self.source_name) and (response_content is not None):
                headers = {
                    'x-access-token': self.api_key,
                    'source-name': self.source_name
                }
                response = requests.post(self.api_endpoint, json=data, headers=headers)
                if response.status_code == 200:
                    print("Devzery: Success!", response.json()['message'])
                if response.status_code != 200:
                    print(f"Failed to send data to API endpoint. Status code: {response.status_code}")
            elif (self.api_key and self.source_name) is None:
                print("Devzery: No API Key or Source given!")
            else:
                print("Devzery: Response content is not JSON, not adding")
        except requests.RequestException as e:
            print(f"Error occurred while sending data to API endpoint: {e}")
