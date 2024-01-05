# Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна (шапка, меню, подвал)
# и дочерние шаблоны для страниц категорий товаров и отдельных товаров. Например, создать страницы:
# "Одежда", "Обувь" и "Куртка", используя базовый шаблон.

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login_success.html')

@app.route('/jeans/')
def jeans():
    price = 1300
    context = {'price': price}
    return render_template('jeans.html', **context)

@app.route('/jacket/')
def jacket():
    price = 3000
    context = {'price': price}
    return render_template('jacket.html', **context)

@app.route('/shoes/')
def shoes():
    price = 4100
    context = {'price': price}
    return render_template('shoes.html', **context)


if __name__ == '__main__':
    app.run()