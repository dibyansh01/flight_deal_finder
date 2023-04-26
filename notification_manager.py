from twilio.rest import Client
TWILIO_SID = "TWILIO_SID"
TWILIO_AUTH_TOKEN = "TWILIO_TOKEN"
TWILIO_PHONE_NO = "TWILIO_PHONE_NO"
MY_PHONE_NO = "MY_PHONE_NO"

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NO,
            to=MY_PHONE_NO,
        )
        # Prints if successfully sent.
        print(message.sid)