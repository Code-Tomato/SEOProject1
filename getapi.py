import os 
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from google import genai
from google.genai import types
import requests
import json
import pandas as pd
from student_info_db import engine, metadata, students
import sqlalchemy as db
from algo import similarity_report

conn = engine.connect()

# Set environment variables
my_api_key = os.getenv('GENAI_API_KEY')
genai.api_key = my_api_key

print("Welcome to RoomieMatch! Please enter your details.\n")

current_user = {
    "name": input("What's your name? "),
    "age": int(input("How old are you? ")),
    "pronouns": input("What are your pronouns? (e.g., he/him, she/her) "),
    "hobbies": input("List your hobbies (comma-separated): "),
    "fav_movies": input("List your favorite movies (comma-separated): "),
    "music_genres": input("Favorite music genres (comma-separated): "),
    "music_artists": input("Favorite music artists (comma-separated): "),
    "instagram": input("Instagram handle (optional): "),
    "email": input("Your email: "),
    "cleanliness": input("How would you describe your cleanliness? (e.g., clean, messy, average): "),
    "sleep_schedule": input("Are you an early bird or a night owl? (early/night): "),
    "wakeup_time": input("When do you usually wake up? (early/late): "),
    "contacted": False  
}

id_results=similarity_report(current_user)
select_query=db.select(students).where(students.c.id.in_(id_results))
results= conn.execute(select_query).fetchall()

SENDER="roomie.match01@gmail.com" # GET EMAIL, CAN ALSO 
#RECIEVER=emails # RECIEVE EMAIL LISTS FROM DATABASE


def gemini_api(current_user_prompt, matched_prompt):
    client = genai.Client(
        api_key=my_api_key,
    )
    
    full_prompt = f"""
You are generating a short summary (around 100 words each) describing the compatibility between the following user and 5 potential roommates.

User Profile:
{current_user_prompt}

Potential Matches:
{matched_prompt}

Provide your output in the following format:

1. [summary of match 1]
2. [summary of match 2]
...
5. [summary of match 5]
"""

    # Specify the model to use and the messages to send
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
        system_instruction="You are giving a summary of the connections between the current_user and the people they match with" \
                            "keep each summary around 100 words and same format for each, label each one 1-5."
        ),
        contents=[full_prompt]
    )
    
    return response.text
    
    
current_user_prompt = ""
current_user_prompt += f"Name: {current_user['name']}\n"
current_user_prompt += f"Pronoun: {current_user['pronouns']}\n"
current_user_prompt += f"Hobbies: {current_user['hobbies']}\n"
current_user_prompt += f"Favorite Movies: {current_user['fav_movies']}\n"
current_user_prompt += f"Music Genres: {current_user['music_genres']}\n"
current_user_prompt += f"Favorite Artists: {current_user['music_artists']}\n"
current_user_prompt += f"Cleanliness: {current_user['cleanliness']}\n"
current_user_prompt += f"Sleep Schedule: {current_user['sleep_schedule']}\n"
current_user_prompt += f"Wakeup Time: {current_user['wakeup_time']}\n"

prompts = []
for row in results:
    student = row._mapping  # or dict(row) if using older SQLAlchemy
    prompt_text = ""
    prompt_text += f"Name: {row['name']}\n"
    prompt_text += f"Pronouns: {row['pronouns']}\n"
    prompt_text += f"Hobbies: {row['hobbies']}\n"
    prompt_text += f"Favorite Movies: {row['fav_movies']}\n"
    prompt_text += f"Music Genres: {row['music_genres']}\n"
    prompt_text += f"Favorite Artists: {row['music_artists']}\n"
    prompt_text += f"Cleanliness: {row['cleanliness']}\n"
    prompt_text += f"Sleep Schedule: {row['sleep_schedule']}\n"
    prompt_text += f"Wakeup Time: {row['wakeup_time']}\n\n"
    
    prompts.append(prompt_text)
    
matched_prompt = ""
for i, match_text in enumerate(prompts, start=1):
    matched_prompt += f"{i}.\n{match_text}"

print(gemini_api(current_user_prompt, matched_prompt))
    
# API Sends email to receiver from Roomie Email
def send_mail(RECIEVER):
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



