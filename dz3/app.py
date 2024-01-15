# база в var/app-instance

from flask import Flask, render_template, url_for, request
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from dz3.forms import RegistrationForm
from dz3.models import db, Student
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seminar3.db'
db.init_app(app)
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = b'b0ee5a2c6515091072087d57c6693be951cd9fc4629e5e66324c8c33331b5768'
csrf = CSRFProtect(app)


@app.context_processor
def menu_items():
    menu_items = [
        {'name': 'Главная', 'url': url_for("index")},
        {'name': 'Регистрация', 'url': url_for("registration")},
    ]
    return dict(menu_items=menu_items)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    context = {'alert_message': "Добро пожаловать!"}
    form = RegistrationForm()
    username = form.username.data
    usersurname = form.usersurname.data
    email = form.email.data
    password = form.password.data
    if request.method == 'POST' and form.validate():
        if Student.query.filter(Student.email == email).all():
            context = {'alert_message': "Пользователь уже существует!"}
            return render_template('registration.html', form=form, **context)
        else:
            password_hash = generate_password_hash(password)
            new_user = Student(username=username, usersurname=usersurname, email=email, password=password_hash)
            db.session.add(new_user)
            db.session.commit()
            return render_template('registration.html', form=form, **context)
    return render_template('registration.html', form=form)
