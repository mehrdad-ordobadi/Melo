from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from models import User, Artist, Album, Listener, Song, Playlist, PlaylistSong
from forms import RegistrationForm
from datetime import datetime
from database import db
from werkzeug.utils import secure_filename
from biography_form import BiographyForm
import os
import mutagen
from AlbumForm import AlbumForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/audio')
ALLOWED_EXTENSIONS = {'mp3'}    # only mp3 files accepted

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app) 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        existing_user = User.query.filter_by(username=form.username.data).first()

        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return render_template('register.html', form=form)

        user_name = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='sha256')
        user_type = form.user_type.data
        date_join = datetime.utcnow()

        if user_type == 'listener':
            listener = Listener(username=user_name, password=hashed_password, user_type=user_type, user_email=email, date_join=date_join, first_name=form.first_name.data, last_name=form.last_name.data)
            db.session.add(listener)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

        else:
            artist_stagename = form.artist_stagename.data
            artist_city = form.artist_city.data
            artist_tags = form.artist_tags.data
            artist = Artist(username=user_name, password=hashed_password, user_type=user_type, user_email=email, date_join=date_join, first_name=form.first_name.data, last_name=form.last_name.data, artist_stagename=artist_stagename, artist_city=artist_city, artist_tags=artist_tags, artist_biography=None)
            db.session.add(artist)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            # flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Unable to log in. Please check your credentials and try again.', 'danger')
    return render_template('login.html'), 200


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = AlbumForm()
    if request.method == 'POST':
        files = request.files.getlist('file')
        if not files:
            flash('No files part')
            return redirect(request.url)

        album_release_date = form.album_release_date.data
        artist_id = current_user.id
        album = form.album_title.data.strip()
        existing_album = Album.query.filter_by(album_title=album, artist_id=artist_id).first()
        if not existing_album:
            if not form.album_release_date.data:
                flash('New albums require a release dates!')
                return redirect(request.url)
            if form.validate_on_submit():
                new_album = Album(
                    album_title=album,
                    album_release_date=album_release_date,
                    artist_id=artist_id
                )
                artist = Artist.query.get(artist_id)
                artist.albums.append(new_album)
                db.session.add(new_album)
            
        album = album.strip().replace(' ', '_').lower()
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(artist_id), album, filename.lower())
                if os.path.exists(file_path):
                    flash('Song already added in the album!')
                    return redirect(request.url)
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], str(artist_id), album), exist_ok=True)
                file.save(file_path)
                audio = mutagen.File(file_path)     # use mutagen to get the length of the audio file
                length = int(audio.info.length)
                new_song = Song(song_title=os.path.splitext(filename)[0], file_path=file_path, length=length)
                new_album.songs.append(new_song)
                db.session.add(new_song)
        db.session.commit()
        flash('Files uploaded successfully')
        return redirect(url_for('upload_file'))

    return render_template('upload.html', form=form)


@app.route('/songs')
def songs():
    all_albums = Album.query.all()
    return render_template('songs.html', albums=all_albums)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']
    artists = Artist.query.filter(Artist.artist_stagename.ilike(f'%{search_query}%')).all()
    return render_template('search_results.html', artists=artists)

@app.route('/artist/<int:artist_id>', methods=['GET'])
def artist_page(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    albums = Album.query.filter_by(artist_id=artist_id).all()
    return render_template('artist_page.html', artist=artist, albums=albums)



@app.route('/artist/<int:artist_id>/biography', methods=['GET', 'POST'])
@login_required
def artist_biography(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = BiographyForm()
    if form.validate_on_submit():
        if 'delete' in request.form:
            
            artist.artist_biography = ''
        else:
            artist.artist_biography = form.biography.data

        db.session.commit()
        return redirect(url_for('artist_page', artist_id=artist_id))
    elif artist.artist_biography:
        form.biography.data = artist.artist_biography

    return render_template('artist_biography.html', artist=artist, form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
