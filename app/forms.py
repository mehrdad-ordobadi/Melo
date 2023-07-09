from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.validators import Optional


class RegistrationForm(FlaskForm):
    """Form for user registration

    Args:
        FlaskForm: Base class for creating forms in Flask.
    """
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(
    ), EqualTo('password', message='Confirm Password must match Password.')])
    user_type = SelectField('User Type', choices=[('listener', 'Listener'), (
        'artist', 'Artist')], validators=[DataRequired(message='User Type is required.')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    artist_stagename = StringField('Artist Stage Name', validators=[])
    artist_city = StringField('Artist City', validators=[])
    artist_tags = StringField('Artist Tag', validators=[])

    submit = SubmitField('Sign Up')


class EventForm(FlaskForm):
    """form for creating an event by artist

    Args:
        FlaskForm: Base class for creating forms in Flask.
    """
    event_title = StringField('Event Title', validators=[DataRequired()])
    event_date = DateTimeLocalField(
        'Event Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    event_venue = StringField('Venue', validators=[DataRequired()])
    description = StringField('Description', validators=[])

    submit = SubmitField('Add Event')

class NotificationForm(FlaskForm):
    notification_title = StringField('Notification Title', validators=[DataRequired()])
    notification_content = StringField('Content',  validators=[])
    submit = SubmitField('Send')