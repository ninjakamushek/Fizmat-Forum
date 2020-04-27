from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class ThreadForm(FlaskForm):
    title = StringField("Вопрос", validators=[DataRequired()])
    submit = SubmitField('Создать')
