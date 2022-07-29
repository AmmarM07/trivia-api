# Backend - Trivia API

## Full Stack Trivia API Project

This application is built to allow users to browse the questions that already on the website. Also it allows add and delete questions. It also gives a chance to users to play quiz game so that they can test their knowledge. The main goal of the application is to build API with endpoints that do the following:

1. Show the 10 questions in one page eihter all the questions together or depening on their category.
2. Delete questions 
3. Search for questions by using keyword
4. Add new questions with their answers and categories
5. play a quiz game 

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** 
- Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Run the Frontend in development mode Mode 
The frontend app was using react. To run the app in development use `npm install` to install the npm then `npm start` to run the app.
If the terminal doesn't open the app automatically, open in any browser [http://localhost:3000](http://localhost:3000)

## TASKS

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## API Reference

### Getting Started

Base URL: Currently this application is only hosted locally. The backend is hosted at http://127.0.0.1:5000/
Authentication: This version does not require authentication or API keys.

### Error Handling

There are four types of errors the API will return:
- 400 - Bad request
- 404 - Not found
- 422 - Unprocessable
- 405 - Method not allowed

## API Endpoints

### GET '/Categories'

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Returns: An object with a single key, `categories`, that contains an object of `id: trype` key: value pairs.
- Sample: `curl -X GET http://localhost:5000/categories`

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### GET '/questions'

- Get all the questions from the database 
- Returns: it returns a JSON object contains the following:
  1. Dictionary of categories
  2. Paginated questions, 10 qustions per page.
  3. Total questions available
- Sample: `curl -X GET http://localhost:5000/categories`

```json
{
"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_categrey": null,
  "questions": [
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 1,
      "id": 2,
      "question": "Which country does have the most WC titles ?"
    },
    {
      "answer": "Meryl Streep",
      "category": "2",
      "difficulty": 4,
      "id": 4,
      "question": "Who has the most oscar nominations?"
    },
    {
      "answer": "Isaac Newton",
      "category": "1",
      "difficulty": 1,
      "id": 6,
      "question": "Who did discover the gravity?"
    },
    {
      "answer": "Edison",
      "category": "1",
      "difficulty": 1,
      "id": 7,
      "question": "Who did invent the electric lamp"
    },
    {
      "answer": "Hedy Lemarr",
      "category": "1",
      "difficulty": 4,
      "id": 10,
      "question": "Who did invent the WiFi?"
    },
    {
      "answer": "1642",
      "category": "4",
      "difficulty": 4,
      "id": 11,
      "question": "When did the first calculator come to life?"
    },
    {
      "answer": "7",
      "category": "6",
      "difficulty": 2,
      "id": 12,
      "question": "How many Ueafa Champions League titla does milan have?"
    },
    {
      "answer": "Van Gogh",
      "category": "2",
      "difficulty": 3,
      "id": 13,
      "question": "Who did paint The Starry Night?"
    },
    {
      "answer": "China",
      "category": "3",
      "difficulty": 2,
      "id": 15,
      "question": "Which country has the most population of the world?"
    },
    {
      "answer": "Khalifa Tower",
      "category": "5",
      "difficulty": 2,
      "id": 16,
      "question": "what is tallest tower in the world?"
    }
  ],
  "success": true,
  "total_questions": 14
}
```

## GET '/categories/int:category_id/questions'

- Get all the questions from the database that belong to the specific catogery id `category_id`
- Returns: it returns a JSON object contains the following:
  1. Paginated questions list from specified category
  2. Total questions available that belong to that specific category
  3. The id of the category 
- Sample: `curl -X GET http://localhost:5000/categories/2/questions`

```json
{
  "current_category": 2,
  "questions": [
    {
      "answer": "Meryl Streep",
      "category": "2",
      "difficulty": 4,
      "id": 4,
      "question": "Who has the most oscar nominations?"
    },
    {
      "answer": "Van Gogh",
      "category": "2",
      "difficulty": 3,
      "id": 13,
      "question": "Who did paint The Starry Night?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

## DELETE '/questions/id'

- Deletes a question with specific id from the database 
- Returns id of the deleted question and the total number of the remaining questions 
- Sample: `curl -X Delete http://localhost:5000/questions/4`

```json 
{
  "deleted_question": 4,
  "success": true,
  "total_questions": 13
}

```
## POST '/questions'

- Creates a new question and adds it to data base using JSON request parameters
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"question": "Who has the second most golden ball titles?", "answer": "C.Ronaldo", "difficulty": 1, "category": "6" }' http://localhost:5000/questions`
- Returns the follwoing JSON object

```json
{
  "created": 21,
  "success": true,
  "total_questions": 14
}
```

## POST 'questions/search'

- Searchs for questions those match the search term
- Retruns a JSON object contains the follwing items:
  1. Paginated questions list that match the search term 
  2. Total of found questions 
- Sample:  `curl -X POST -H "Content-Type: application/json" -d '{ "searchTerm": "Who"}' http://localhost:5000/questions/search`

```json
{
  "questions": [
    {
      "answer": "Van Gogh",
      "category": "2",
      "difficulty": 3,
      "id": 13,
      "question": "Who did paint The Starry Night?"
    },
    {
      "answer": "Hedy Lemarr",
      "category": "1",
      "difficulty": 4,
      "id": 10,
      "question": "Who did invent the WiFi?"
    },
    {
      "answer": "Isaac Newton",
      "category": "1",
      "difficulty": 1,
      "id": 6,
      "question": "Who did discover the gravity?"
    },
    {
      "answer": "Edison",
      "category": "1",
      "difficulty": 1,
      "id": 7,
      "question": "Who did invent the electric lamp"
    },
    {
      "answer": "Thomas Jefferson",
      "category": "4",
      "difficulty": 4,
      "id": 18,
      "question": "who is the third president of US? "
    }
  ],
  "success": true,
  "total_questions": 5
}
```

## POST '/quizzes'

- Allows users to play a quiz game
- Uses JSON request parameters of category and prevoius question 
- Retruns json object contains the next question which is not in previous questions list
-Sample:  `curl -X POST -H "Content-Type: application/json" -d '{'previous_questions': [17, 18], 'quiz_category': {'id': '6', 'type': 'Sports'}}' http://localhost:5000/quizzes`

```json
{
  "question": {
    "id": 12,
    "question": "How many Ueafa Champions League titla does milan have?",
    "answer": "7",
    "category": "6",
    "difficulty": "2",
  },
  "success": true
}
```
## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
