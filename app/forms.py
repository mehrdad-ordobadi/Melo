from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.validators import Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', choices=[('listener', 'Listener'), ('artist', 'Artist')], validators=[DataRequired()])
    artist_stagename = StringField('artist_tage Name', validators=[DataRequired(), Length(min=2, max=80)])
    artist_city = StringField('artist_city', validators=[DataRequired(), Length(min=2, max=80)])
    artist_tags = StringField('artist_tag', validators=[DataRequired(), Length(min=2, max=80)])
    
    submit = SubmitField('Sign Up')

def validate(self):
        if not FlaskForm.validate(self):
            return False

        
        if self.user_type.data == 'artist':
            if not self.artist_stagename.data or not self.artist_city.data or not self.artist_tags.data:
                self.artist_stagename.errors.append('artist_stagename name is required.')
                self.artist_city.errors.append('artist_city is required.')
                self.artist_tags.errors.append('artist_tag is required.')
                return False

        return True
