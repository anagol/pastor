from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)
bootstrap = Bootstrap5(app)



url = 'https://eparhia992.by/component/search/?searchword=%D0%BA%D1%83%D1%88%D0%BD%D0%B5%D1%80%D0%B5%D0%B2%D0%B8%' \
      'D1%87&searchphrase=all&limit=0'

response = requests.get(url)
soup = bs(response.text, "html.parser")
names = soup.find_all('a')
pub_date = soup.find_all(class_='result-created')
name_result = [x for x in names if 'item' in x.get('href')]
string_result = min(len(pub_date), len(name_result))


# -------------------Главная-------------------
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница')


# -------------------О храме -------------------
@app.route('/about')
def about():
    return render_template('about.html', title='Наш храм')


# ------------------Страница новостей-------------------
@app.route('/news')
def news():
    return render_template('news.html', title='Новости храма', names=names,
                           pub_date=pub_date, name_result=name_result, string_result=string_result)


# -------------------Икона храма----------------
@app.route('/icon')
def icon():
    return render_template('icon.html', title='Храмовая икона')


# -------------------Настоятель храма----------------
@app.route('/priest')
def priest():
    return render_template('priest.html', title='Настоятель храма')


# -------------------Расписание богослужений----------------
@app.route('/timetable')
def timetable():
    return render_template('timetable.html', title='Расписание богослужений')


# -------------------Контакты----------------
@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Наши контакты')


@app.route('/error_401')
def error_401():
    return render_template('401.html', title='ОШИБКА 401')


if __name__ == '__main__':
    app.run(debug=True)
