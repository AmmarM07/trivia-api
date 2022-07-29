import os
from unicodedata import category
from urllib import response
from flask import Flask, current_app, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.---[done]
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories_q = Category.query.order_by(Category.id).all()
        categories = {}
        for category in categories_q:
            categories[category.id] = category.type

        if len(categories) == 0:
            abort(404)    

        return jsonify({
            "success": True,
            "categories": categories,
            "total_categories": len(categories)
        })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination
    at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.--[done**]
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, selection)

        categories_q = Category.query.all()
        categories = {}
        for category in categories_q:
            categories[category.id] = category.type

        if len(questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": questions,
            "categories": categories,
            "current_categrey": None,
            "total_questions": len(Question.query.all())
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a
    question, the question will be removed.
    This removal will persist in the database
    and when you refresh the page.--[done]
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            q = Question.query.filter(Question.id == question_id)
            deleted_question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if q is None:
                abort(404)

            deleted_question.delete()
            return jsonify({
                'success': True,
                'deleted_question': question_id,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(404)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question
    will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        if not 'question' in body:
            abort(422)

        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')

        try:
            question = Question(question=question, answer=answer,
                                category=category, difficulty=difficulty)
            question.insert()
            return jsonify({
                'success': True,
                'created': question.id,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def get_question_by_search_term():
        body = request.get_json()
        search_term = body.get('searchTerm')

        if search_term:
            result = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            current_questions = paginate_questions(request, result)

            if len(result) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(result)
            })
        else:
            abort(404)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_question_by_category(category_id):
        try:
            questions_q = Question.query.filter(
                Question.category == str(category_id)).all()

            if len(questions_q) == 0:
                abort(404)

            questions = paginate_questions(request, questions_q)
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(questions),
                'current_category': category_id
            })
        except:
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quiz_game():
        try:
            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
            category_id = quiz_category['id']
            next_question = None

            if category_id != 0:
                questions = Question.query.filter_by(
                    category=category_id).filter(
                        Question.id.notin_((previous_questions))).all()
            else:
                questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()

            if len(questions) > 0:
                next_question = random.choice(questions).format()
            return jsonify({
                'success': True,
                'question': next_question
            })
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422...[done*].
    """
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_error(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(405)
    def not_allowed_method_error(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 422

    return app
