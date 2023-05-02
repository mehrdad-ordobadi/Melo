from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.validators import Optional

class ListenerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=80)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=80)])
    submit = SubmitField('Submit')
