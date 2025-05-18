from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, EmailField
from wtforms.validators import DataRequired


class AddDepForm(FlaskForm):
    title = StringField('Название Департамента', validators=[DataRequired()])
    chief = StringField('Id главного', validators=[DataRequired()])
    members = StringField("Участники", validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Добавить департамент')
