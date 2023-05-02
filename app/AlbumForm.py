from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class AlbumForm(FlaskForm):
    album_title = StringField('Album Title', validators=[DataRequired()])
    album_release_date = DateField('Release Date', format='%Y-%m-%d')
    submit = SubmitField('Add Album')
