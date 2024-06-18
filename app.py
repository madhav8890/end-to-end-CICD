from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, task FROM todos;')
    todos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def create_todo():
    new_task = request.json['task']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO todos (task) VALUES (%s) RETURNING id;', (new_task,))
    todo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': todo_id, 'task': new_task})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
