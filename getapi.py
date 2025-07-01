import os 
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from google import genai
from google.genai import types
import requests
import json
import pandas as pd
import sqlalchemy as db

# Database
# Set environment variables
my_api_key = os.getenv('GENAI_API_KEY')
genai.api_key = my_api_key

SENDER="roomie.match01@gmail.com" # GET EMAIL, CAN ALSO 
RECIEVER="marcogb1234@gmail.com" # RECIEVE EMAIL, GET FROM DATABASE


about_me=input("Tell me about yourself: ")
#Create an genAI client using the key from our environment variable
client = genai.Client(
    api_key=my_api_key,
)

# Specify the model to use and the messages to send
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
      system_instruction="You are generating the body of an email, you are writing a summary of this person based on the contents"
    ),
    contents=about_me
)

message = Mail(
    from_email=SENDER,
    to_emails=RECIEVER,
    subject='Roommate Inquiry',
    html_content=response.text)
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)



