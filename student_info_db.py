import sqlalchemy as db
#Create the database for the roommate matching process
engine = db.create_engine('sqlite:///roommate_match.db')

#MetaData: To create our table
metadata = db.MetaData()

#Data Table for students so Gemini can analyze to see what student would be a good roommate
students = db.Table('students', metadata,
  db.Column('id', db.Integer, primary_key=True),
  db.Column('name', db.String, nullable=False),
  db.Column('age', db.Integer),
  db.Column('pronouns', db.String, nullable=False),
  db.Column('hobbies', db.String, nullable=False),
  db.Column('fav_movies', db.String, nullable=False),
  db.Column('music_genres', db.String, nullable=False),
  db.Column('music_artists', db.String, nullable=False),
  db.Column('instagram', db.String),
  db.Column('email', db.String, unique=True, nullable=False), # This is casuing problem since some students may have unqinue
  db.Column('cleanliness', db.String, nullable=False),
  db.Column('sleep_schedule', db.String, nullable=False),
  db.Column('wakeup_time', db.String, nullable=False),
  db.Column('contacted', db.Boolean, default=False),
)

#data table for students who have been paired
matches = db.Table('matches', metadata,
  db.Column('pair_id', db.Integer, primary_key=True),
  db.Column('student_1_id', db.Integer, nullable=False),
  db.Column('student_2_id', db.Integer, nullable=False),
)

metadata.create_all(engine)
conn = engine.connect()