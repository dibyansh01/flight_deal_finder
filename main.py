from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()
sheet_data_length = len(sheet_data)
# print(sheet_data)
ORIGIN_CITY_IATA = "DEL"

for i in range(sheet_data_length):
    try:
        if sheet_data[i]["iataCode"] == "":
            sheet_data[i]["iataCode"] = flight_search.get_destination_code(sheet_data[i]["city"])
    except KeyError:
        print("Error. Empty row in sheet, moving ro next.")
        continue



data_manager.destination_data = sheet_data
data_manager.update_dstination_code()

tomorrow = datetime.now() + timedelta(days=1)
six_month_fromtoday = datetime.now() + timedelta(days=(6*30))

for destination in sheet_data:
    try:
        flight = flight_search.check_flight(
            ORIGIN_CITY_IATA, destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_fromtoday
        )
    except KeyError:
        print("Error. City entry is empty")
        continue
    try:
        if flight.price < destination["lowestPrice"]:
            notification_manager.send_sms(
                message=f"Low price alert Only ₹{flight.price} to fly from {flight.origin_city} - {flight.origin_airport} "
                        f"to {flight.destination_city} - {flight.destination_airport}, from {flight.out_date}"
                        f" to {flight.return_date}"
            )
    except AttributeError:
        continue

