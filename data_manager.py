import requests
from pprint import pprint
SHEETY_ENDPOINT = "YOUR_SHEETY_ENDPOINT"

#This class is responsible for talking to the Google Sheet.
class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data



    def update_dstination_code(self):
        for city in self.destination_data:
            try:
                new_data = {
                    "sheet1": {
                        "iataCode":city["iataCode"]
                    }
                }

                response = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json = new_data)
                print(response.json)
            except KeyError:
                continue
        # else:
        #     print("no entry is there")

# data_manager = DataManager()
# print(data_manager.get_destination_data())

