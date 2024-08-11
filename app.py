from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sl
from datetime import datetime



app = Flask(__name__)  # мы созд. объект на основе класса Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # здесь по ключу делаем подсоединение к ДБ 'sqlite'
db = SQLAlchemy(app)   # здесь мы передаём сам объект(db) к нашему проекту


class Article(db.Model):  # создаём класс для хранения записей с полями в определённой таблице
    id = sl.Column(sl.Integer, primary_key=True)   # Integer - только числа, primary_key - уникальное id
    type = sl.Column(sl.String)
    title = sl.Column(sl.String(100), nullable=False)  # title - название, нельзя устанавливат пустым
    intro = sl.Column(sl.String(300), nullable=False)
    # intro - вступление, String(300) - текст, длинна, nullable=False - не вступать без вступления
    text = sl.Column(sl.Text, nullable=False)   # text - для установки полного текста
    date = sl.Column(sl.DateTime, default=datetime.timestamp)  # date - дата публикаций, utcnow - время публикации
    with app.app_context():
        db.create_all()


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


@app.route("/posts")  # добавляем метод вывода информации из стороннего сайта
def posts():  # выводим функцию
    # Article.query.outerjoin(Comment).group_by(Article.id).order_by(func.count(Comment.id).asc()).all()
    articles = Article.query.order_by(Article.date).all()
    # first()выводит первую запись взятую из БД, order_by(Article.date).all() - сортирует всё по полю date
    return render_template("posts.html", articles=articles)  # возв.шаблон в нём мы можем раб.с article


@app.route("/create_article", methods=["POST", "GET"])  # добавляем метод приёма запросов
def create_article():              # выводим функцию
    if request.method == 'POST':   # проверяется форма приёма и доб.в БД
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)  # создали объект для передачи в БД

        try:
            db.session.add(article)   # add - добавляем объект
            db.session.commit()       # commit - сохраняем объект
            return redirect('/')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create_article.html")  # возврат


# @app.route("/user/<string:name>/<int:id>")  # если надо получить некий параметр из url адр.(/user,/name имя,/id инд)
# def user(name, id):  # выводим функцию
#     return "User page:" + name + " - " + str(id)     # возврат


if __name__ == "__main__":   # если мы будем выводить в этом файле main
    app.run(debug=True)   # обращ. к объекту app далее к команде run(запуск этого проекта)

