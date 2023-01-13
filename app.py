from flask import Flask, redirect, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница')


@app.route('/about')
def about():
    return render_template('about.html', title='Наш храм')


@app.route('/news')
def news():
    return render_template('news.html', title='Новости храма')


@app.route('/history')
def history():
    return render_template('history.html', title='История храма')


@app.route('/icon')
def icon():
    return render_template('icon.html', title='Храмовая икона')


@app.route('/priest')
def priest():
    return render_template('priest.html', title='Настоятель храма')


@app.route('/timetable')
def timetable():
    return render_template('timetable.html', title='Расписание богослужений')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Наши контакты')


if __name__ == '__main__':
    app.run()
