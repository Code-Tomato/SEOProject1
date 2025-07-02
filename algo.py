import pandas as pd
import dummy_students_data
from dummy_students_data import results
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dummy_students_data import engine, students


def similarity_report(user_dict):
    # Step 1: Load all students into a DataFrame
    df = pd.DataFrame([dict(row._mapping) for row in results])

    # Add the ego user to the DataFrame
    ego_df = pd.DataFrame([user_dict])
    df = pd.concat([df, ego_df], ignore_index=True)
    ego = ego_df.iloc[0]

    # --- PRIMARY FIELDS (weighted more) ---
    primary_fields = ['sleep_schedule', 'cleanliness', 'wakeup_time']

    # --- SECONDARY FIELDS (weighted less) ---
    secondary_fields = ['hobbies', 'fav_movies', 'music_genres', 'music_artists']

    def combine(row, fields):
        return " ".join(str(row[f]) for f in fields)

    # Combine text for each group
    ego_primary = combine(ego, primary_fields)
    ego_secondary = combine(ego, secondary_fields)
    others = df[df['name'] != user_dict['name']].copy()
    others['primary'] = others.apply(lambda row: combine(row, primary_fields), axis=1)
    others['secondary'] = others.apply(lambda row: combine(row, secondary_fields), axis=1)

    # TF-IDF + cosine similarity for each group
    vec_primary = TfidfVectorizer()
    vec_secondary = TfidfVectorizer()

    primary_matrix = vec_primary.fit_transform([ego_primary] + others['primary'].tolist())
    secondary_matrix = vec_secondary.fit_transform([ego_secondary] + others['secondary'].tolist())

    primary_scores = cosine_similarity(primary_matrix[0:1], primary_matrix[1:]).flatten()
    secondary_scores = cosine_similarity(secondary_matrix[0:1], secondary_matrix[1:]).flatten()

    # Combine with weights
    others['similarity'] = 0.7 * primary_scores + 0.3 * secondary_scores

    # Get top 5
    top_5 = others.sort_values(by='similarity', ascending=False).head(5)

    # Return list of top 5 matching user IDs
    return top_5['id'].tolist()

# person1 = {
#     "name": "Nathan Lemma",
#     "age": 19,
#     "pronouns": "he/him",
#     "hobbies": "Reading, gaming, and hiking.",
#     "fav_movies": "Inception, The Matrix",
#     "music_genres": "Lo-fi, Chill",
#     "music_artists": "Tame Impala, Joji",
#     "instagram": "@nathanl",
#     "email": "nathan.lemma@example.com",
#     "cleanliness": "clean",
#     "sleep_schedule": "early",
#     "wakeup_time": "early",
#     "contacted": False
# }

# print(similarity_report(person1))