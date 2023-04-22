import flask, sqlite3, flask_login, os
from werkzeug.security import generate_password_hash, check_password_hash
from fdatabase import Database
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from UserLogin import UserLogin
from forms import LoginForm

from flask import Flask

# конфиг
SECRET_KEY = "dfksdnflksnfks*&*(^787d7sfhids_(980"
app = flask.Flask(__name__, template_folder="./templates")
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fsite.db')))
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

login_manager = flask_login.LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Сначала Авторизуйтесь!'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    '''Вспомогательная функция для создания таблиц БД'''
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    '''Соединение с БД, если оно не установлено'''
    if not hasattr(flask.g, 'link_db'):
        flask.g.link_db = connect_db()
    return flask.g.link_db


dbase = None


@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = Database(db)


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(flask.g, 'link_db'):
        flask.g.link_db.close()


@app.route("/")
def index():
    return flask.render_template('index.html')


@app.route("/profile")
def profile():
    if not flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('login'))
    return flask.render_template('profile.html')


# @app.route("/profile/author/<username>")
# def profile():
# return flask.render_template('author.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if flask.request.method == 'POST':
        email = flask.request.form.get('email')
        print(email)
        return flask.redirect(flask.url_for('login'))
    else:
        return flask.render_template('signup.html')


@app.route("/bd", methods=['GET', 'POST'])
def db():
    weq = dbase.getUser(1)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('profile'))
    if form.validate_on_submit():
        if flask.request.method == 'POST':
            user = dbase.getUserByEmail(flask.request.form['username'])
            if user and check_password_hash(user['password'], flask.request.form['password']):
                userlogin = UserLogin().create(user)
                rm = True if flask.request.form.get('remainme') else False
                flask_login.login_user(userlogin, remember=rm)
                return flask.redirect(flask.request.args.get("next") or flask.url_for("profile"))
            flask.flash("Неверная пара логин/пароль", "error")
        flask.flash("Введите данные", "error")

    return flask.render_template('login.html', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))


if (__name__ == "__main__"):
    app.run(debug=True)
