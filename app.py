from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Dial
import os

app = Flask(__name__)

# Your Twilio credentials from environment variables
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

@app.route("/handle-call", methods=["POST"])
def handle_call():
    forward_number = os.environ.get("FORWARD_TO_NUMBER")  # e.g., +15551234567
    response = VoiceResponse()
    dial = Dial(action="/handle-call-result", timeout=20)
    dial.number(forward_number)
    response.append(dial)
    return Response(str(response), mimetype="text/xml")

@app.route("/handle-call-result", methods=["POST"])
def handle_call_result():
    call_status = request.form.get("DialCallStatus")
    from_number = request.form.get("From")

    if call_status in ["no-answer", "busy", "failed"]:
        client.messages.create(
            body="Hey! Sorry we missed your call. What can we help you with?",
            from_=twilio_number,
            to=from_number
        )
    return Response("", status=200)

@app.route("/", methods=["GET"])
def home():
    return "Server is live!"
