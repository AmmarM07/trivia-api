import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'abc')
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.DB_USER,  self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'who was the best football player for 2021',
            'answer': 'messi',
            'category': '1',
            'difficulty': 1
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """
    # tester for get_categories endpoint
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    def test_get_categories_404(self):
        res = self.client().get('/categories/2000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # testers for get_questions endpoint and its' error handelers
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_get_questions_404(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # testers for delete_question endpoint and its' error handelers--
    def test_delete_question(self):
        res = self.client().delete('/questions/16')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertEqual(data['deleted_question'], 16)
        self.assertTrue(len(data['total_questions']))

    def test_delete_question_404(self):
        res = self.client().delete('/questions/5600')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # testers for create_question endpoint and its' error handelers
    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['total_questions'])

    def test_create_question_422(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # testers for search_term endpoint and its' error handelers
    def test_get_question_by_search_term(self):
        search = {
            "searchTerm": "who"
            }
        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_question_by_search_term_404(self):
        search = {
            "searchTerm": "dadada"
            }
        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # testers for get_question_by_category endpoint and its' error handelers-
    def test_get_question_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 1)

        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_get_question_by_category_404(self):
        res = self.client().get('/categories/8000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # testers for quiz_game endpoint and its' error handelers--[1*]
    def test_quiz_game(self):
        quiz_sample = {
            'previous_questions': [17, 18, 19],
            'quiz_category': {'id': '1', 'type': 'sport'}
            }
        res = self.client().post('/quizzes', json=quiz_sample)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def quiz_game_422(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
