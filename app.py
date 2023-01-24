from flask import Flask, redirect, render_template, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import psycopg2
import locale
import requests
from bs4 import BeautifulSoup as bs
# from flask_paginate import Pagination, get_page_args
import lxml

# ---------------Парсер-----------
url_1 = 'https://eparhia992.by/component/search/?searchword=%D0%BA%D1%83%D1%88%D0%BD%D0%B5%D1%80%D0%B5%D0%B2%D0%B8%D1%87&searchphrase=all&limit=0'

response = requests.get(url_1)
soup = bs(response.text, "html.parser")
names = soup.find_all('a')
pub_date = soup.find_all(class_='result-created')
name_result = [x for x in names if 'item' in x.get('href')]
string_result = min(len(pub_date), len(name_result))
# ----------------------------------------------------------


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anatolihalasny1969'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pastor.db"
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap5(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(250))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    news_date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.current_timestamp())
    news_headline = db.Column(db.String, unique=False)
    news_content = db.Column(db.Text, unique=False)
    news_photo = db.Column(db.String, unique=False)

    def __init__(self, news_headline, news_content, news_photo):
        self.news_headline = news_headline
        self.news_content = news_content
        self.news_photo = news_photo

    def __repr__(self):
        return '<News %r>' % self.news_headline


class TimeTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timetable_date_create = db.Column(db.DateTime(timezone=True), nullable=False, default=func.current_timestamp())
    timetable_date = db.Column(db.String, unique=False)
    timetable_content = db.Column(db.Text, unique=False)
    time_service_1 = db.Column(db.String, unique=False)
    time_service_2 = db.Column(db.String, unique=False)
    time_service_3 = db.Column(db.String, unique=False)

    def __init__(self, timetable_date, timetable_content, time_service_1, time_service_2, time_service_3,
                 content_time_service_1, content_time_service_2, content_time_service_3):
        self.timetable_date = timetable_date
        self.timetable_content = timetable_content
        self.time_service_1 = time_service_1
        self.time_service_2 = time_service_2
        self.time_service_2 = time_service_3
        self.content_time_service_1 = content_time_service_1
        self.content_time_service_2 = content_time_service_2
        self.content_time_service_2 = content_time_service_3

    def __repr__(self):
        return '<TimeTable %r>' % self.timetable_content


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.errorhandler(401)
def page_not_found(error):
    return redirect(url_for('error_401'))


# -------------------Главная-------------------
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница')


# -------------------О храме -------------------
@app.route('/about')
def about():
    return render_template('about.html', title='Наш храм')


# ------------------Страница со списком новостей-------------------
@app.route('/news')
def news():
    news_total = News.query.all()
    return render_template('news.html', title='Новости храма', news_total=news_total, names=names,
                           pub_date=pub_date, name_result=name_result, string_result=string_result)


# ----------------Создание новости-----------------------------
@app.route('/create_news', methods=['GET', 'POST'])
@login_required
def create_news():
    if request.method == "POST":
        # news_date = request.form["news_date"]
        news_headline = request.form["news_headline"]
        news_content = request.form["news_content"]
        news_photo = request.form["news_photo"]
        nws = News(news_headline=news_headline, news_content=news_content, news_photo=news_photo)
        db.session.add(nws)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('news'))
    return render_template('create_news.html', title='Добавляем новость')


# --------------------Отдельная страница новости------------------------------------------------------------------------
@app.route('/<int:nws_id>')
def news_page(nws_id):
    nws = News.query.filter_by(id=nws_id).one()
    return render_template('news_page.html', nws=nws)


# --------------------Страница редактирования новости-------------------------------------------------------------------
@app.route('/news_edit')
@login_required
def news_edit():
    edit_news = News.query.all()
    return render_template('news_edit.html', title='Редактируем', edit_news=edit_news)


#  --------------------Редактирем новость-------------------------------------------------------------------------------
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    edit_news = News.query.get_or_404(id)
    if request.method == 'POST':
        edit_news.news_headline = request.form['news_headline']
        edit_news.news_content = request.form['news_content']
        edit_news.news_photo = request.form['news_photo']
        db.session.flush()
        db.session.commit()
        return redirect('/news')
    else:
        return render_template('edit.html', edit_news=edit_news)


#  --------------------Удаляем новость------------------------------------------------------------------------------------
@app.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    nws = News.query.get_or_404(id)
    db.session.delete(nws)
    db.session.flush()
    db.session.commit()
    return redirect(url_for('news'))


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
    services_total = News.query.all()
    return render_template('timetable.html', title='Расписание богослужений', services_total=services_total)


# -------------------Создать расписание богослужений----------------
@app.route('/create_service', methods=['GET', 'POST'])
@login_required
def create_service():
    if request.method == "POST":
        timetable_date = request.form["timetable_date"]
        timetable_content = request.form["timetable_content"]
        time_service_1 = request.form["time_service_1"]
        time_service_2 = request.form["time_service_2"]
        time_service_3 = request.form["time_service_3"]
        content_time_service_1 = request.form["content_time_service_1"]
        content_time_service_2 = request.form["content_time_service_2"]
        content_time_service_3 = request.form["content_time_service_3"]

        serv = TimeTable(timetable_date=timetable_date, timetable_content=timetable_content,
                         time_service_1=time_service_1, time_service_2=time_service_2, time_service_3=time_service_3,
                         content_time_service_1=content_time_service_1, content_time_service_2=content_time_service_2,
                         content_time_service_3=content_time_service_3)
        db.session.add(serv)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('timetable'))
    return render_template('create_service.html', title='Добавляем службу')


# -------------------Контакты----------------
@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Наши контакты')


# -------------------Админка----------------
@app.route('/admin')
def admin():
    return render_template('admin.html', title='Admin page')


#  --------------------Регистрация-------------------------------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password_hash = generate_password_hash(request.form["password"])
        register = User(username=username, password=password_hash)
        db.session.add(register)
        db.session.flush()
        db.session.commit()
        flash('Вы успешно зарегистрированы, теперь можете войти в систему!')
        return redirect(url_for("login"))
    return render_template("register.html", title='Регистрация')


#  --------------------Login-------------------------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username=username).first()
        login_user(user)
        if user is None:
            flash('Неверная пара логин - пароль')
            return render_template("login.html")
        if not check_password_hash(user.password, request.form['password']):
            flash('Неверная пара логин - пароль')
            return render_template("login.html")
        flash(f'Вы успешно авторизованы под именем {username}!')
        return redirect(url_for("admin"))

    return render_template("login.html", title='Вход')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/error_401')
def error_401():
    return render_template('401.html', title='ОШИБКА 401')


if __name__ == '__main__':
    app.run(debug=True)
