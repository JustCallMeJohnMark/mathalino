from flask_login import UserMixin

class Teacher(UserMixin):
    def __init__(self, id, username, password, name):
        self.id = id
        self.username = username
        self.password = password
        self.name = name

    def __repr__(self):
        return f'Teacher({self.username}, {self.name})'

class Student(UserMixin):
    def __init__(self, id, username, password, name):
        self.id = id
        self.username = username
        self.password = password
        self.name = name

    def __repr__(self):
        return f'Student({self.username}, {self.name})'
    