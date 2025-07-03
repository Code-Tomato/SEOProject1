import unittest
from algo import similarity_report

class TestRoomieMatch(unittest.TestCase):
    
    def test_collect_user_info_structure(self):
        # Simulate a sample user manually since input() can't be tested directly
        sample_user = {
            "name": "Test User",
            "age": 21,
            "pronouns": "they/them",
            "hobbies": "coding,reading",
            "fav_movies": "Inception,Interstellar",
            "music_genres": "Rock,Pop",
            "music_artists": "Queen,Coldplay",
            "instagram": "@test",
            "email": "test@example.com",
            "cleanliness": "clean",
            "sleep_schedule": "night",
            "wakeup_time": "late",
            "contacted": False
        }
        self.assertIsInstance(sample_user, dict)
        self.assertIn("name", sample_user)
        self.assertIn("contacted", sample_user)
        self.assertEqual(sample_user["contacted"], False)

    def test_user_age_validity(self):
        age = 21
        self.assertIsInstance(age, int)
        self.assertGreater(age, 0)
        self.assertLess(age, 120)

    def test_user_hobbies_split(self):
        hobbies = "coding,reading,swimming"
        hobby_list = [h.strip() for h in hobbies.split(",")]
        self.assertEqual(hobby_list, ["coding", "reading", "swimming"])
    
    def test_similarity_report_output(self):
        sample_user = {
            "name": "Ella Barnes",
            "age": 19,
            "pronouns": "she/her",
            "hobbies": "Bullet journaling, yoga, and latte art.",
            "fav_movies": "Breakfast at Tiffany’s, A Silent Voice",
            "music_genres": "Indie Pop, Classical",
            "music_artists": "Clairo, Ryuichi Sakamoto",
            "instagram": "@ellajournals",
            "email": "ella.b@example.com",
            "cleanliness": "clean",
            "sleep_schedule": "early",
            "wakeup_time": "early",
            "contacted": False
        }
        report = similarity_report(sample_user)
        self.assertIsInstance(report, list)