import os 
from google import genai
from google.genai import types
import requests
import json

# Set environment variables
my_api_key = os.getenv('GENAI_API_KEY')

genai.api_key = my_api_key

url="https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15"
data = requests.get(url).json()
data_str = ""
for game in data:
    print(game)
    data_str += json.dumps(game, indent=2) + "\n"


# for game in data:
#     print(f"Title: {game['title']}, Sales Price: {game['salePrice']}, Normal Price: {game['normalPrice']}")
    
user_input = input("What type of games and price range are you looking for? ")

#Create an genAI client using the key from our environment variable
client = genai.Client(
    api_key=my_api_key,
)

# Specify the model to use and the messages to send
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
      system_instruction="Parse through the data and let me know "
    ),
    contents=[user_input, data_str]
)

print(response.text)


