
def check_null_values(data):
    keys = ['title', 'description', 'due_date', 'status']
    for key in keys:
        if data.get(key) is None:
            return False
    return True
