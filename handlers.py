from flask import jsonify
from database import get_db
from util import check_null_values

validStatuses = ("Incomplete", "In Progress", "Completed")

def create_task(request):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    status = data.get('status')

    if not check_null_values(data):
        return jsonify({'message':'data is Incomplete, check the fields'}), 400

    if status not in validStatuses:
        return jsonify({'status':status, 'message':'status not valid'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, due_date, status)
        VALUES (?, ?, ?, ?)
    ''', (title, description, due_date, status))
    db.commit()

    task_id = cursor.lastrowid

    response = {
        'id': task_id,
        'title': title,
        'description': description,
        'due_date': due_date,
        'status': status
    }

    return jsonify(response), 201


def get_task(task_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
            SELECT * FROM tasks
            WHERE id = ?
        ''', (task_id,))
    task = cursor.fetchone()

    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    task_data = {
        'id': task[0],
        'title': task[1],
        'description': task[2],
        'due_date': task[3],
        'status': task[4]
    }

    return jsonify(task_data)



def get_tasks(request):
    db = get_db()
    cursor = db.cursor()

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    cursor.execute('''
        SELECT * FROM tasks
        ORDER BY id
        LIMIT ? OFFSET ?
    ''', (per_page, (page - 1) * per_page))

    tasks = cursor.fetchall()

    response = []
    for task in tasks:
        task_data = {
            'id': task[0],
            'title': task[1],
            'description': task[2],
            'due_date': task[3],
            'status': task[4]
        }
        response.append(task_data)

    return jsonify(response)


def update_task(task_id, request):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = list(cursor.fetchone())

    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    update_data = request.get_json()
    if 'due_date' in update_data:
        task[3] = update_data['due_date']
    if 'title' in update_data:
        task[1] = update_data['title']
    if 'description' in update_data:
        task[2] = update_data['description']
    if 'status' in update_data:
        if update_data['status'] not in validStatuses:
            return jsonify({'status':update_data['status'], 'message':'status not valid'}), 400
        else:
            task[4] = update_data['status']

    cursor.execute('UPDATE tasks SET due_date=?, title=?, description=?, status=? WHERE id=?', (task[3], task[1], task[2], task[4], task[0]))
    db.commit()

    updated_task = {
        'id': task[0],
        'title': task[1],
        'description': task[2],
        'due_date': task[3],
        'status': task[4]
    }

    return jsonify(updated_task)



def delete_task(task_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    return f"deleted Task with Task-ID : {task_id}"
