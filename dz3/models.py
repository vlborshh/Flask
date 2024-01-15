from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    usersurname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100))
    password = db.Column(db.String(380), nullable=False)

    def __repr__(self):
        return f'Студент({self.username}: день рождения {self.birthday}, почта {self.email})'


