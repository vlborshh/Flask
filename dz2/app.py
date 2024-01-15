from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from werkzeug.utils import secure_filename
from pathlib import Path, PurePath
from re import split

app = Flask(__name__)
app.secret_key = b'asdgasgdw6362718y7dtdasbdgt213776das7dtgw182ge6'

@app.context_processor
def menu_site():
    menu_i = [
        {'name': 'На главную', 'url': url_for('index')},
        {'name': 'Задание №1', 'url': url_for('task_1')},
        {'name': 'Задание №2', 'url': url_for('task_2')},
        {'name': 'Задание №3', 'url': url_for('task_3')},
        {'name': 'Задание №4', 'url': url_for('task_4')},
        {'name': 'Задание №5', 'url': url_for('task_5')},
        {'name': 'Задание №6', 'url': url_for('task_6')},
        {'name': 'Задание №7', 'url': url_for('task_7')},
        {'name': 'Задание №8', 'url': url_for('task_8')},
        {'name': 'Задание №9(домашняя работа)', 'url': url_for('login_form')},
    ]
    return dict(menu_items=menu_i)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/task_1', methods=['GET', 'POST'])
def task_1():
    if request.method == 'POST':
        return redirect(url_for('hello', name='User'))
    return render_template('task_1.html')


@app.route('/hello/<name>', methods=['GET', 'POST'])
def hello(name):
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('hello.html', name=name)

@app.route('/task_2')
def task_2():
    return render_template('task_2.html')

@app.route('/task_2_upload', methods=['GET', 'POST'])
def task_2_upload():
    if request.method == 'POST':
        image = request.files.get('image')
        file_name = secure_filename(image.filename)
        Path(Path.cwd(), 'static', 'uploads').mkdir(exist_ok=True)
        image.save(PurePath.joinpath(Path.cwd(), 'static', 'uploads', file_name))
        return (f"""Файл {file_name} загружен на сервер<br><a href='{url_for('task_2_upload')}'>Назад</a>""")
    return render_template('form_task_2.html')

@app.route('/task_3', methods=['GET', 'POST'])
def task_3():
    login = 'login'
    password = '0000'
    if request.method == 'POST':
        login_new = request.form.get('login')
        password_new = request.form.get('password')
        if login == login_new and password == password_new:
            return redirect(url_for('hello', name=login))
        else:
            flash('Пара логин/пароль не верна', 'danger')
            return redirect(url_for('task_3'))
    return render_template('task_3.html')

@app.route('/task_4', methods=['GET', 'POST'])
def task_4():
    if request.method == 'POST':
        text_new = request.form.get('text').strip()
        words = split(r'[,.\s]+', text_new)
        return f'Введено: {len(words)} слов'
    return render_template('task_4.html')

@app.route('/task_5', methods=['GET', 'POST'])
def task_5():
    if request.method == 'POST':
        res = 0
        numbers_1 = int(request.form.get('num1'))
        numbers_2 = int(request.form.get('num2'))
        operation = request.form.get('operation')
        if operation == 'plus':
            res = numbers_1 + numbers_2
        elif operation == 'minus':
            res = numbers_1 - numbers_2
        elif operation == 'mult':
            res = numbers_1 * numbers_2
        elif operation == 'div':
            res = numbers_1 / numbers_2
        return str(res)
    return render_template('task_5.html')

@app.route('/task_6', methods=['GET', 'POST'])
def task_6():
    if request.method == 'POST':
        name = request.form.get('name')
        age = int(request.form.get('age'))
        if age >= 18:
            #return f'{name} ваш возраст в пределах допустимого. Доступ разрешен'
            return render_template('index.html')
        else:
            #return f'{name} ваш возраст менее 18 лет. Доступ запрещен'
            return render_template('404.html')
    return render_template('task_6.html')

@app.route('/task_7', methods=['GET', 'POST'])
def task_7():
    if request.method == 'POST':
        numbers = int(request.form.get('num'))
        numbers_pow_2 = pow(numbers,2)
        return f'Введено число: {numbers}. Его квадрат: {numbers_pow_2}.'
    return render_template('task_7.html')

@app.route('/task_8', methods=['GET', 'POST'])
def task_8():
    if request.method == 'POST':
        if not request.form.get('name'):
            flash('Вы не ввели имя', 'danger')
            return redirect(url_for('task_8'))
        name = request.form.get('name')
        flash('Имя введено', 'success')
        return f'Привет {name}'
    return render_template('task_8.html')

#домашнее задание
@app.route('/login_form', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        session['login'] = request.form.get('login')
        session['email'] = request.form.get('email')

        response = make_response(redirect(url_for('login_success')))
        response.set_cookie('login', session['login'])
        response.set_cookie('email', session['email'])
        return response

    context = {
        'login': 'Авторизация'
    }
    return render_template('login_form.html', **context)


@app.route('/login_success', methods=['GET', 'POST'])
def login_success():
    if 'login' in session:
        context = {
            'login': session['login'],
            'email': session['email'],
            'title': 'Добро пожаловать'
        }
        if request.method == 'POST':
            session.pop('login', None)
            session.pop('email', None)

            response = make_response(redirect(url_for('login_form')))
            response.set_cookie('login', '', 0)
            response.set_cookie('email', '', 0)
            return response
        return render_template('login_success.html', **context)
    else:
        return redirect(url_for('login_form'))



if __name__ == '__main__':
    app.run(debug=True)