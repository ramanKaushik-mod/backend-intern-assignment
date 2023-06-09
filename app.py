from flask import Flask, request
from database import close_connection
from handlers import create_task, get_task, get_tasks, update_task, delete_task

app = Flask(__name__)
app.teardown_appcontext(close_connection)

@app.route('/', methods=['POST'])
def create():
    return create_task(request)


@app.route('/', methods=['GET'])
def get():
    task_id = request.args.get('task_id')
    if task_id:
        return get_task(task_id)
    else:
        return get_tasks(request)


@app.route('/<int:task_id>', methods=['PUT', 'DELETE'])
def update_or_delete(task_id):
    if request.method == 'PUT':
        return update_task(task_id, request)
    elif request.method == 'DELETE':
        return delete_task(task_id)



if __name__ == '__main__':
    app.run(debug=True)