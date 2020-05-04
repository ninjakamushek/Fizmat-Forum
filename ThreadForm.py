from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectMultipleField
from wtforms.validators import DataRequired


class ThreadForm(FlaskForm):
    title = StringField("Вопрос", validators=[DataRequired()])
    tags = SelectMultipleField("Тэги", choices=[
    	("akr", "АКР"),
    	("education", "Обучение"),
    	("olympiads", "Олимпиады"),
    	("else", "Другое")], validators=[DataRequired()])
    submit = SubmitField('Создать')
