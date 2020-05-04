from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class UpdateForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    grade = IntegerField('Класс', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
