from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, BooleanField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    jn = StringField('Название работы', validators=[DataRequired()])
    tl = StringField('Id тимлмдера', validators=[DataRequired()])
    ws = StringField("Размер работы (в часах)", validators=[DataRequired()])
    col = StringField("Помощники", validators=[DataRequired()])

    n = DateTimeField("начало работы 2025-05-12 21:57:54", validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    c = DateTimeField("конец работы 2025-05-12 21:57:54", validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    f = BooleanField("Завершена ли?")
    submit = SubmitField('Добавить работу')
