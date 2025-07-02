from student_info_db import engine, metadata, students
import sqlalchemy as db

conn = engine.connect()

engine = db.create_engine('sqlite:///roommate_match.db')
metadata = db.MetaData()
conn = engine.connect()

students = db.Table('students', metadata, autoload_with=engine)


# Create dummy data (you can insert multiple students if you like
dummy_students = [
    {
        "name": "Josh Anderson",
        "age": 18,
        "pronouns": "he/him",
        "hobbies": "watching film, hiking",
        "fav_movies": "Avengers End Game, X-Men Days of Future Past",
        "music_genres": "R&B, Pop",
        "music_artists": "Steve Lacy",
        "instagram": "@nyc.josh",
        "email": "joshanderson@example.com",
        "cleanliness": "clean",
        "sleep_schedule": "late",
        "wakeup_time": "late",
        "contacted": False
    },
    {
        "name": "Ben Brown",
        "age": 19,
        "pronouns": "he/him",
        "hobbies": "Gaming, especially FPS games, and cooking new recipes.",
        "fav_movies": "John Wick, Spider-Man",
        "music_genres": "Hip-Hop, Rap",
        "music_artists": "Drake, Kendrick",
        "instagram": "@benb",
        "email": "benjib@example.com",
        "cleanliness": "messy",
        "sleep_schedule": "late",
        "wakeup_time": "late",
        "contacted": False
    },
    {
        "name": "Salma Lopez",
        "age": 18,
        "pronouns": "she/her",
        "hobbies": "I love reading, especially latin american literature",
        "fav_movies": "Mcfarland USA, Juno",
        "music_genres": "Pop, R&B",
        "music_artists": "The Marias, Malcolm Todd",
        "instagram": "@salma_l",
        "email": "salmalopez@example.com",
        "cleanliness": "clean",
        "sleep_schedule": "late",
        "wakeup_time": "early",
        "contacted": False
    },
    {
        "name": "Eve Flores",
        "age": 18,
        "pronouns": "she/her",
        "hobbies": "I enjoy cooking, baking, and playing video games",
        "fav_movies": "La La Land, Star Wars Revenge of the Sith",
        "music_genres": "Chill, R&B, Rap",
        "music_artists": "Megan Thee Stallion, Cuco",
        "instagram": "@eve_flores",
        "email": "eveflores@example.com",
        "cleanliness": "clean",
        "sleep_schedule": "late",
        "wakeup_time": "late",
        "contacted": False
    },
    {
        "name": "Denise Lillies",
        "age": 19,
        "pronouns": "she/her",
        "hobbies": "I enjoy gyming, playing my guitar, and reading books",
        "fav_movies": "The Notebook, 500 Days of Summer",
        "music_genres": "Chill, R&B, Rap",
        "music_artists": "Tyler The Creator, Mac DeMarco",
        "instagram": "@denise_l",
        "email": "deniselillies@example.com",
        "cleanliness": "neutral",
        "sleep_schedule": "late",
        "wakeup_time": "early",
        "contacted": False
    },
    {
        "name": "David Diaz",
        "age": 18,
        "pronouns": "he/him",
        "hobbies": "Basketball, working out, and watching documentaries.",
        "fav_movies": "The Batman, Parasite",
        "music_genres": "Rap, R&B, Rock",
        "music_artists": "Frank Ocean, Ian",
        "instagram": "@daviddiaz",
        "email": "daviddiaz@example.com",
        "cleanliness": "neutral",
        "sleep_schedule": "late",
        "wakeup_time": "early",
        "contacted": False
    },
    {
        "name": "Isabella Johnson",
        "age": 18,
        "pronouns": "she/her",
        "hobbies": "Reading non-fiction, debates, and crafting.",
        "fav_movies": "Legally Blonde, Scott Pilgrim vs. The World",
        "music_genres": "Lo-fi, Chill",
        "music_artists": "Tame Impala, Joji",
        "instagram": "@isabell_j",
        "email": "isabellajohnson@example.com",
        "cleanliness": "neutral",
        "sleep_schedule": "late",
        "wakeup_time": "early",
        "contacted": False
    },
    {
        "name": "Jalen Cortes",
        "age": 18,
        "pronouns": "he/him",
        "hobbies": "Working out, streaming games, and playing soccer.",
        "fav_movies": "Avengers: Endgame, Fast & Furious",
        "music_genres": "R&B, Rap",
        "music_artists": "21 Savage, Travis Scott",
        "instagram": "jasonj",
        "email": "jason@example.com",
        "cleanliness": "neutral",
        "sleep_schedule": "late",
        "wakeup_time": "early",
        "contacted": False
    },
    {
        "name": "Cristian Castellanos",
        "age": 18,
        "pronouns": "he/him",
        "hobbies": "I enjoy swimming, hiking, and playing video games.",
        "fav_movies": "The Batman, Ponyo, ",
        "music_genres": "R&B, Chill, Rap, Soul",
        "music_artists": "Malcolm Todd, The Marias, Tyler the Creator",
        "instagram": "cristiann",
        "email": "ccastellanos@vassar.edu",
        "cleanliness": "neutral",
        "sleep_schedule": "late",
        "wakeup_time": "late",
        "contacted": False
    },  
    {
        "name": "Lucas Kim",
        "age": 18,
        "pronouns": "he/him",
        "hobbies": "Skateboarding, anime, and coding.",
        "fav_movies": "Spirited Away, The Matrix",
        "music_genres": "Lo-fi, Rock",
        "music_artists": "Radiohead, Joji",
        "instagram": "lucask",
        "email": "lucas.kim@example.com",
        "cleanliness": "neutral",
        "sleep_schedule": "late",
        "wakeup_time": "late",
        "contacted": False
    },
    {
        "name": "Aaliyah Jackson",
        "age": 19,
        "pronouns": "she/her",
        "hobbies": "Dancing, podcasting, yoga",
        "fav_movies": "Step Up, Hidden Figures",
        "music_genres": "R&B, Pop",
        "music_artists": "SZA, Beyoncé",
        "instagram": "aaliyahmoves",
        "email": "a.jackson@example.com",
        "cleanliness": "clean",
        "sleep_schedule": "early",
        "wakeup_time": "early",
        "contacted": False
    },
    {
        "name": "Liam White",
        "age": 19,
        "pronouns": "he/him",
        "hobbies": "Gaming, music production, hiking",
        "fav_movies": "Inception, Tenet",
        "music_genres": "EDM, Rap",
        "music_artists": "Kanye West, Flume",
        "instagram": "@liamw",
        "email": "liam.white@example.com",
        "cleanliness": "messy",
        "sleep_schedule": "late",
        "wakeup_time": "late",
        "contacted": False
    }
]


conn.execute(students.delete()) #For testing: prints on terminal each time file runs
insert_query = students.insert().values(dummy_students)
conn.execute(insert_query)

# Print all rows in the students table
select_query = db.select(students)
results = conn.execute(select_query).fetchall()

print("Students Table:\n")
for row in results:
  print(row._mapping) #dict(row) crashed, ._mapping gives data as a key-value pair