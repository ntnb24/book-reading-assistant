from flask import request, jsonify, render_template
from app import app
from .models import insert_question_answer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-question', methods=['POST'])
def submit_question():
    data = request.json
    question = data['question']
    answer = "Sample answer"  # Placeholder for your answer generation logic
    insert_question_answer(question, answer)
    return jsonify({"question": question, "answer": answer})



