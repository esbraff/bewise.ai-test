from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import requests
import config

QUESTIONS_URL = 'https://jservice.io/api/random'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@db/{config.POSTGRES_DB}'
db = SQLAlchemy(app)


@dataclass
class Question(db.Model):
    id: int
    question_text: str
    answer_text: str
    created_at: str

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String)
    answer_text = db.Column(db.String)
    created_at = db.Column(db.DateTime)


db.create_all()


@app.route('/create-questions', methods=['POST'])
def create_questions():
    try:
        questions_num = int(request.json['questions_num'])
        r = requests.get(QUESTIONS_URL, params=dict(count=questions_num))
        r.raise_for_status()

        for question in r.json():
            new_question = Question(
                id=question['id'],
                question_text=question['question'],
                answer_text=question['answer'],
                created_at=question['created_at']
            )
            db.session.add(new_question)

        db.session.commit()

        return "OK!"
    except (ValueError, KeyError):
        return 'Invalid questions_num value'


@app.route('/get-questions', methods=["GET"])
def get_questions():
    result = Question.query.all()
    return jsonify(result)
