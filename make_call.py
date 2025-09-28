# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()
account_sid = os.getenv("Account_SID")
auth_token = os.getenv("Auth_Token")
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

client = Client(account_sid, auth_token)

call = client.calls.create(
    url="https://adjectively-unattentive-tripp.ngrok-free.dev/voice",
    to="+91",
    from_="+1",
)

print(call.sid)
