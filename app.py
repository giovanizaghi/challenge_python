from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# PostgreSQL connection config
db_config = {
    'host': 'localhost',
    'database': 'taxinsight',
    'user': 'postgres',
    'password': 'postgres'
}

def get_db_connection():
    conn = psycopg2.connect(**db_config)
    return conn

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING id', (title, description))
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': task_id, 'title': title, 'description': description}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tasks SET title = %s, description = %s WHERE id = %s',
                (title, description, task_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': task_id, 'title': title, 'description': description})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': f'Task {task_id} deleted'})

if __name__ == '__main__':
    app.run(debug=True)
