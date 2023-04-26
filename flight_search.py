import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = "YOUR_TEQUILA_API_KEY"
from data_manager import DataManager
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        header = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, params= query, headers= header)
        results = response.json()
        code = results["locations"][0]["code"]
        return code

    def check_flight(self, origin_city_code, destination_city_code, from_time,to_time):
        header = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "RSD"
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=header, params=query)
        try:
            data = response.json()["data"][0]

        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price= data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: ₹{flight_data.price}")
        return flight_data

flight_search = FlightSearch()







# data_manager = DataManager()
# sheet_data = data_manager.get_destination_data()
# flight_search = FlightSearch()
# flight_search.get_destination_code(sheet_data[0]["city"])
