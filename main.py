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

conn = engine.connect() # Connection to Database
metadata = db.MetaData()
conn = engine.connect()

# Set environment variables
my_api_key = os.getenv('GENAI_API_KEY')
genai.api_key = my_api_key

client = genai.Client(
        api_key=my_api_key,
    )

def collect_user_info():
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

    return current_user

def gemini_api(current_user_prompt, matched_prompt):
    full_prompt = f"""
    You are generating a short summary (around 100 words each) describing the 
    compatibility between the following user and 5 potential roommates.

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
    
# SENDGRID API
def send_mail(RECIEVER, Intro):
    message = Mail(
        from_email=SENDER,
        to_emails=RECIEVER,
        subject='Roommate Inquiry',
        html_content=Intro)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(e.message)

# Test User
# current_user = {
#     "name": "Sophia Lee",
#     "age": 20,
#     "pronouns": "She/Her",
#     "hobbies": "Painting, yoga, reading",
#     "fav_movies": "Little Women, Spirited Away",
#     "music_genres": "Indie, Acoustic",
#     "music_artists": "Phoebe Bridgers, Novo Amor",
#     "instagram": "@sophia.arts",
#     "email": "sophia.lee@example.com",
#     "cleanliness": "average",
#     "sleep_schedule": "early",
#     "wakeup_time": "early",
#     "contacted": False
# }

current_user = collect_user_info()

insert_query= students.insert().values(current_user)

# Execute the query
# conn.execute(insert_query)
# print("Current user added to the roommate_db.")

id_results=similarity_report(current_user) # Gets roommate ID's that are most similar
select_query=db.select(students).where(students.c.id.in_(id_results)) # Selects the roommates form Database
results= conn.execute(select_query).fetchall()

# Turns Dict into String for Gemini
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

# Turns all the possible roommates into a string
emails=[]
prompts = []
for row in results:
    student = row._mapping  
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
    
    emails.append(row['email'])
    prompts.append(prompt_text)

matched_prompt = ""
for i, match_text in enumerate(prompts, start=1):
    matched_prompt += f"{i}.\n{match_text}"

print(gemini_api(current_user_prompt, matched_prompt) + "\n") # Prints summary of possible rommates


# ------ EMAILS -------
reach_out = input("Which possible rommates would you like to reach out to? We will send them an email that introduces you to them" \
                  "(Insert their bullet point number, Comma Seperated): ")

reach_out_list = reach_out.split(",")

valid_emails = []
for i in reach_out_list:
    valid_emails.append(emails[((int)(i)) - 1 ])
    
# Test Emails for the moment
valid_emails= ["marcogb1234@gmail.com", "marcoaguzmanbalcazar@gmail.com"]    
SENDER="roomie.match01@gmail.com" # RoomieMatch Email
RECIEVER=valid_emails 

# Call on Gemini API to create an intro for the User
intro = response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
        system_instruction="You are going to give a quick introduction about myself, its for a potential roommate"
        ),
        contents=current_user_prompt
    )


print("\n" + intro.text)
print("Sending emails...")
for email in RECIEVER:
    send_mail(email, intro.text)
    
# select_query = db.select(students)
# results = conn.execute(select_query).fetchall()

# # Print the results
# for row in results:
#     print(dict(row._mapping))