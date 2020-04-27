from flask import Flask, render_template
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.utils import redirect
from LoginForm import LoginForm
from RegisterForm import RegisterForm
from ThreadForm import ThreadForm
from CommentForm import CommentForm
from AnswerForm import AnswerForm
from data import db_session
from data.users import User
from data.threads import Thread
from data.comments import Comment

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'ff_secret_key'


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    session = db_session.create_session()
    return render_template('index.html', threads=session.query(Thread).all())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.email = form.email.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_thread',  methods=['GET', 'POST'])
@login_required
def add_thread():
    form = ThreadForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        thread = Thread()
        thread.title = form.title.data
        thread.user_id = current_user.id
        session.add(thread)
        session.commit()
        return redirect('/')
    return render_template('adding new thread.html', title='Создание треда',
                           form=form)


@app.route('/thread/<tid>')
def indexed_thread(tid):
    session = db_session.create_session()
    return render_template('indexed_thread.html',
                           thread=session.query(Thread).filter(Thread.id == tid).first(),
                           comments=session.query(Comment).filter(Comment.thread_id==tid).all())


@app.route('/add_comment/<tid>', methods=['GET', 'POST'])
@login_required
def add_comment(tid):
    form = CommentForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        comment = Comment()
        comment.text = form.text.data
        comment.user_id = current_user.id
        comment.thread_id = tid
        session.add(comment)
        session.commit()
        return redirect(f'/thread/{tid}')
    return render_template('add_comment.html', title='Оставить комментарий', form=form)


# def


def main():
    db_session.global_init("db/FF.sqlite")
    app.run()


if __name__ == '__main__':
    main()
