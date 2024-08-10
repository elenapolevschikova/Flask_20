from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # мы созд. объект на основе класса Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'   # здесь по ключу делаем подсоединение к ДБ 'sqlite'
db = SQLAlchemy(app)   # здесь мы передаём сам объект(db) к нашему проекту


class Article(db.Model):  # создаём класс для хранения записей с полями в определённой таблице
    id = db.Column(db.Integer, primary_key=True)   # Integer - только числа, primary_key - уникальное id
    title = db.Column(db.String(100), nullable=False)  # title - название, нельзя устанавливат пустым
    intro = db.Column(db.String(300), nullable=False)
    # intro - вступление, String(300) - текст, длинна, nullable=False - не вступать без вступления
    text = db.Column(db.Text, nullable=False)   # text - для установки полного текста
    date = db.Column(db.DateTime, default=datetime.utcnow)  # date - дата публикаций, utcnow - время публикации


    def __repr__(self):  # при поиске инфо, метод выдачи объекта с id
        return '<Article %r' % self.id



@app.route("/")  # если мы хотим отслеживать главн. стр. вывод.текст - указываем /(слеш)
@app.route("/home")  # на главн. стр.можем вывод.текст - указываем /(слеш и несколько адресов)
# @app.route("/home/new")  # на главн. стр.можем вывод.текст - указываем /(слеш и несколько адресов)
def index():  # выводим функцию
    return render_template("index.html")  # возврат


@app.route("/about")  #
def about():  # выводим функцию
    return render_template("about.html")  # возврат


@app.route("/user/<string:name>/<int:id>")  # если надо получить некий параметр из url адр.(/user,/name имя,/id инд)
def user(name, id):  # выводим функцию
    return "User page:" + name + " - " + str(id)     # возврат


if __name__ == "__main__":   # если мы будем выводить в этом файле main
    app.run(debug=True)      # обращ. к объекту app далее к команде run(запуск этого проекта)
