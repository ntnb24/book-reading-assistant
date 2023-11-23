import sqlite3

DATABASE = 'app.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def insert_question_answer(question, answer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO questions (question, answer) VALUES (?, ?)', (question, answer))
    conn.commit()
    conn.close()

def get_all_questions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions')
    questions = cursor.fetchall()
    conn.close()
    return questions