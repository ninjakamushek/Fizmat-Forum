from flask import Flask, render_template, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from AnswerForm import AnswerForm
from CommentForm import CommentForm
from LoginForm import LoginForm
from RegisterForm import RegisterForm
from ThreadForm import ThreadForm
from data import db_session
from data.answers import Answer
from data.comments import Comment
from data.statistics import Action
from data.threads import Thread
from data.users import User

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

@app.route('/sorted')
def sorted_index():
    session = db_session.create_session()
    if request.args.get('sort_type') == 'time':
        return render_template('index.html', threads=session.query(Thread).all())
    elif request.args.get('sort_type') == 'like':
        return render_template('index.html', threads=sorted(session.query(Thread).all(), key=lambda x: x.like_count))
    elif request.args.get('sort_type') == 'view':
        return render_template('index.html', threads=sorted(session.query(Thread).all(), key=lambda x: x.view_count))


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


@app.route('/add_thread', methods=['GET', 'POST'])
@login_required
def add_thread():
    form = ThreadForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        thread = Thread()
        thread.title = form.title.data
        thread.user_id = current_user.id
        thread.like_count = 0
        thread.view_count = 0
        thread.comment_count = 0
        session.add(thread)
        session.commit()
        return redirect('/')
    return render_template('adding new thread.html', title='Создание треда',
                           form=form)


@app.route('/thread/<tid>')
def indexed_thread(tid):
    session = db_session.create_session()
    thread = session.query(Thread).filter(Thread.id == tid).first()
    if thread:
        act = session.query(Action).filter(Action.user_id == current_user.id, Action.thread_id == tid).first()
        if act:
            if act.viewed is None:
                act.viewed = True
                thread.view_count = 1 + session.query(Thread).filter(Thread.id == tid).first().view_count
                session.commit()
        else:
            action = Action()
            action.user_id = current_user.id
            action.thread_id = tid
            action.viewed = True
            thread.view_count = 1 + session.query(Thread).filter(Thread.id == tid).first().view_count
            session.add(action)
            session.commit()
    return render_template('indexed_thread.html',
                           thread=session.query(Thread).filter(Thread.id == tid).first(),
                           comments=session.query(Comment).filter(Comment.thread_id == tid).all())


@app.route('/thread_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def thread_delete(id):
    session = db_session.create_session()
    thread = session.query(Thread).filter(Thread.id == id, Thread.user == current_user).first()
    if thread:
        session.delete(thread)
        for act in session.query(Action).filter(Action.thread_id == id):
            session.delete(act)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/like_thread/<int:id>', methods=['GET', 'POST'])
@login_required
def like_thread(id):
    session = db_session.create_session()
    thread = session.query(Thread).filter(Thread.id == id).first()
    if thread:
        act = session.query(Action).filter(Action.user_id == current_user.id, Action.thread_id == id).first()
        if act != None:
            if act.liked is None:
                act.liked = True
                thread.like_count = 1 + session.query(Thread).filter(Thread.id == id).first().like_count
                session.commit()
        else:
            action = Action()
            action.user_id = current_user.id
            action.thread_id = id
            action.liked = True
            thread.like_count = 1 + session.query(Thread).filter(Thread.id == id).first().like_count
            session.add(action)
            session.commit()
    return redirect('/')


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
        thread = session.query(Thread).filter(Thread.id == tid).first()
        thread.comment_count = 1 + session.query(Thread).filter(Thread.id == tid).first().comment_count
        session.add(comment)
        session.commit()
        return redirect(f'/thread/{tid}')
    return render_template('add_comment.html', title='Оставить комментарий', form=form)


@app.route('/comment_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def comment_edit(id):
    form = CommentForm()
    if request.method == "GET":
        session = db_session.create_session()
        comment = session.query(Comment).filter(Comment.id == id,
                                                Comment.user == current_user).first()
        if comment:
            form.text.data = comment.text
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        comment = session.query(Comment).filter(Comment.id == id,
                                                Comment.user == current_user).first()
        if comment:
            comment.text = form.text.data
            session.commit()
            return redirect(f'/thread/{comment.thread_id}')
        else:
            abort(404)
    return render_template('add_comment.html', title='Редактирование комментария', form=form)


@app.route('/comment_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def comment_delete(id):
    session = db_session.create_session()
    comment = session.query(Comment).filter(Comment.id == id,
                                            Comment.user == current_user).first()
    if comment:
        session.delete(comment)
        thread = session.query(Thread).filter(Thread.id == comment.thread_id).first()
        thread.comment_count = session.query(Thread).filter(Thread.id == comment.thread_id).first().comment_count - 1
        session.commit()
    else:
        abort(404)
    return redirect(f'/thread/{comment.thread_id}')


@app.route('/add_answer/<cid>', methods=['GET', 'POST'])
@login_required
def add_answer(cid):
    form = AnswerForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        answer = Answer()
        answer.text = form.text.data
        answer.user_id = current_user.id
        answer.comm_id = cid
        session.add(answer)
        session.commit()
        return redirect(f'/answers/{answer.comm_id}')
    return render_template('add_answer.html', title='Ответить на комментарий', form=form)


@app.route('/answers/<cid>')
def answers(cid):
    session = db_session.create_session()
    return render_template('answers.html',
                           comment=session.query(Comment).filter(Comment.id == cid).first(),
                           answers=session.query(Answer).filter(Answer.comm_id == cid).all())


def main():
    db_session.global_init("db/FF.sqlite")
    app.run()


if __name__ == '__main__':
    main()
