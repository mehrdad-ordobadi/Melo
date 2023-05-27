from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class AlbumForm(FlaskForm):
    """Form for uploading album by artist

    Args:
        FlaskForm: Base class for creating forms in Flask.
    """
    album_title = StringField('Album Title', validators=[DataRequired()])
    album_release_date = DateField('Release Date', format='%Y-%m-%d')
    submit = SubmitField('Add Album')
