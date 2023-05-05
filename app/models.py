# from app import db
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from database import db
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    date_join = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_email = db.Column(db.String(120), nullable=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)

    # artist = db.relationship('Artist', uselist=False, back_populates='user')
    # listener = db.relationship('Listener', uselist=False, back_populates='user')
    type = db.Column(db.String(50)) 
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type,
    }

    def __repr__(self):
        return f'<User {self.username}>'

class Artist(User):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    artist_stagename = db.Column(db.String(80), nullable=False)
    artist_city = db.Column(db.String(80), nullable=False)
    artist_tags = db.Column(db.String(80), nullable=False)
    artist_biography = db.Column(db.Text, nullable=True)
    albums = db.relationship('Album', backref='artist', lazy=True)


    __mapper_args__ = {
        'polymorphic_identity': 'artist',
    }

    def __repr__(self):
        return f'<Artist {self.artist_stagename}>'
    

class Listener(User):
    # user_name = db.Column(db.String(80), db.ForeignKey('user.username'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # first_name = db.Column(db.String(80), nullable=False)
    # last_name = db.Column(db.String(80), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'listener',
    }

    def __repr__(self):
        return f'<Listener {self.first_name} {self.last_name}>'
    
class Album(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    album_title = db.Column(db.String(80), nullable=False)
    album_release_date = db.Column(db.DateTime, nullable=False)
    # user_name = db.Column(db.String(80), db.ForeignKey('artist.user_name'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.user_id'), nullable=False)
    # artist_id = db.Column(db.Integer, db.ForeignKey('artist.user_id'))
    songs = db.relationship('Song', backref='album', lazy=True)
    def __repr__(self):
        return f'<Album {self.album_title}>'

class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    event_title = db.Column(db.String(80), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    event_venue = db.Column(db.String(80), nullable=False)
    # user_name = db.Column(db.String(80), db.ForeignKey('artist.user_name'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.user_id'))
    listener_events = db.relationship('ListenerEvent', backref='event', lazy=True)

    def __repr__(self):
        return f'<Event {self.event_title}>'



class Song(db.Model):
    song_id = db.Column(db.Integer, primary_key=True)
    song_title = db.Column(db.String(80), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'))
    listener_songs = db.relationship('ListenerSong', backref='song', lazy=True)
    playlist_songs = db.relationship('PlaylistSong', backref='song', lazy=True)
    file_path = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Song {self.song_title}>'
    
# class Song(db.Model):
#     song_id = db.Column(db.Integer, primary_key=True)
#     song_title = db.Column(db.String(80), nullable=False)
#     length = db.Column(db.Integer, nullable=False)
#     album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'))
#     listener_songs = db.relationship('ListenerSong', backref='song', lazy=True)
#     playlist_songs = db.relationship('PlaylistSong', backref='song', lazy=True)

#     def __repr__(self):
#         return f'<Song {self.song_title}>'

class ListenerEvent(db.Model):
    # user_name = db.Column(db.String(80), db.ForeignKey('listener.user_name'), primary_key=True)
    listener_id = db.Column(db.Integer, db.ForeignKey('listener.user_id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), primary_key=True)

    def __repr__(self):
        return f'<ListenerEvent listener={self.user_name} event={self.event_id}>'

class Playlist(db.Model):
    playlist_id = db.Column(db.Integer, primary_key=True)
    playlist_title = db.Column(db.String(80), nullable=False)
    playlist_creation_date = db.Column(db.DateTime, nullable=False)
    # user_name = db.Column(db.String(80), db.ForeignKey('listener.user_name'))
    listener_id = db.Column(db.Integer, db.ForeignKey('listener.user_id'))
    playlist_songs = db.relationship('PlaylistSong', backref='playlist', lazy=True)

    def __repr__(self):
        return f'<Playlist {self.playlist_title}>'
    
class ListenerSong(db.Model):
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'), primary_key=True)
    # user_name = db.Column(db.String(80), db.ForeignKey('listener.user_name'), primary_key=True)
    listener_id = db.Column(db.Integer, db.ForeignKey('listener.user_id'), primary_key=True)

    def __repr__(self):
        return f'<ListenerSong listener={self.user_name} song={self.song_id}>'

class PlaylistSong(db.Model):
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'), primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.playlist_id'), primary_key=True)

    def __repr__(self):
        return f'<PlaylistSong playlist={self.playlist_id} song={self.song_id}>'
