from flask import Flask, request, render_template, jsonify, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from lists import genres, styles, stacks, artists, decades
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "poop"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../albums.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

user_favorites = db.Table('user_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key = True),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key = True)                          
)

playlist_songs = db.Table('playlist_songs',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True)
)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(500), unique = False)
    duration = db.Column(db.String(10), unique = False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    album = db.relationship('Album', back_populates='songs')
    playlists = db.relationship('Playlist', secondary=playlist_songs, back_populates='songs')

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), index = True, unique = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='playlists')
    songs = db.relationship('Song', secondary=playlist_songs, back_populates='playlists')

class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    discogs_id = db.Column(db.String(50), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100))
    year = db.Column(db.Integer)
    tracklist = db.Column(db.Text)
    cover_image = db.Column(db.String(500))
    discogs_link = db.Column(db.String(500), nullable=False, unique=True)
    style = db.Column(db.String(200))
    label = db.Column(db.String(200))
    catalog_number = db.Column(db.String(100))
    shelf_label = db.Column(db.String(10))
    favorited_by = db.relationship('User', secondary=user_favorites, back_populates='favorites')
    songs = db.relationship('Song', back_populates='album', cascade='all, delete-orphan')

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, index = True, nullable = False)
    password_hash = db.Column(db.String(255), unique = True, index = True, nullable = False)
    favorites = db.relationship('Album', secondary=user_favorites, back_populates='favorited_by')
    playlists = db.relationship('Playlist', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.route('/')
def main():
    if "username" in session:
        return redirect(url_for('homelog'))
    return render_template('home.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks)

@app.route('/create-playlist', methods=['POST'])
def create_playlist():
    user = User.query.filter_by(username=session['username']).first()
    user_id = user.id
    print('user_ud', user_id)
    data = request.get_json()
    print('heres the data:', data)
    playlist_name = data['playlist_name']
    print('playlist name:', playlist_name)
    
    if not playlist_name:
        # Return a JSON response with an error message
        return jsonify({'message': 'Playlist name is required'}), 400
    
    new_playlist = Playlist(name=playlist_name, user_id=user_id)

    db.session.add(new_playlist)
    db.session.commit()

    # Simulate saving to the database (or any other action)
    print(f"Creating playlist: {playlist_name}")

    # Return a success response as JSON
    return jsonify({'message': f"Playlist '{playlist_name}' created successfully"}), 200

@app.route('/get-playlists', methods=['GET'])
def get_playlists():
    if 'username' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    playlists = Playlist.query.filter_by(user_id=user.id).all()
    return jsonify({
        'playlists': [{'id': playlist.id, 'name': playlist.name} for playlist in playlists]
    })

@app.route('/remove-playlist', methods=['DELETE'])
def remove_playlist():
    print('entered the remove playlist endpoint')
    if 'username' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    # Get the user from the session
    user = User.query.filter_by(username=session['username']).first()
    print('user idL', user.id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    playlist_id = data.get('playlist_id')
    
    print('playlist id:', playlist_id)
    # Get the playlist by its ID
    playlist = Playlist.query.get(playlist_id)
    print('playlist object:', playlist)
    print('playlist user_id from object', playlist.user_id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404

    # Check if the playlist belongs to the logged-in user
    if playlist.user_id != user.id:
        return jsonify({'error': 'You can only remove your own playlists'}), 403

    print('log for testing 1')
    # Remove the playlist from the user's list
    user.playlists.remove(playlist)
    print('log for testing 2')
    print(f"User's playlists after removal: {[p.name for p in user.playlists]}")
    db.session.delete(playlist)
    db.session.commit()
    print('playlist name', playlist.name)
    
    return jsonify({'success': f'Removed {playlist.name} from playlists'}), 200

@app.route('/add-song', methods=['POST'])
def add_song():
    # Parse JSON request data
    data = request.get_json()
    print('heres the data for addsong', data)
    if not data or 'trackId' not in data:
        return jsonify({'error': 'Track ID is required'}), 400

    trackTitle = data['trackId']
    trackDuration = data['trackDuration']
    albumId = data['albumId']

    new_song = Song(name=trackTitle, duration=trackDuration, album_id=albumId)

    db.session.add(new_song)
    db.session.commit()
    return jsonify({'message': 'Track added successfully', 'trackTitle': trackTitle}), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('homelog'))
    else:
        error = "Invalid username and/or password. Please try again."
        return render_template('home.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks, error=error)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('home.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks)
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('homelog'))

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('main'))

@app.route('/add-to-favorites', methods=['POST'])
def add_to_favorites():
    if 'username' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    album_id = request.json.get('album_id')
    album = Album.query.get(album_id)
    if not album:
        return jsonify({'error': 'Album not found'}), 404
    
    if album not in user.favorites:
        user.favorites.append(album)
        db.session.commit()
        return jsonify({'success': f'Added {album.title} to favorites'}), 200
    else:
        return jsonify({'error': 'Album already in favorites'}), 400

@app.route('/remove-from-favorites', methods=['DELETE'])
def remove_from_favorites():
    if 'username' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    album_id = request.json.get('album_id')
    print(album_id)
    album = Album.query.get(album_id)
    if not album:
        return jsonify({'error': 'Album not found'}), 404
    
    if album in user.favorites:
        user.favorites.remove(album)
        db.session.commit()
        return jsonify({'success': f'Added {album.title} to favorites'}), 200
    else:
        return jsonify({'error': 'Album already in favorites'}), 400

@app.route('/get-favorite-songs')
def get_favorite_songs():
    if 'username' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    results = user.favorites
    print('results', results)
    songs = [{'title': album.title, 'artist': album.artist, 'id': album.id, 'genre': album.genre, 'image': album.cover_image, 'shelf': album.shelf_label, 'tracklist': album.tracklist, 'style': album.style} for album in results]
    return jsonify({'songs': songs})

@app.route('/home-log')
def homelog():
    if "username" in session:
        return render_template('home-log.html', username=session["username"])
    return redirect(url_for('main'))

@app.route('/genres')
def genre_section():
    return render_template('genres.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks)

@app.route('/styles')
def style_section():
    return render_template('styles.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks)

@app.route('/artists')
def artist_section():
    return render_template('artists.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks)

@app.route('/the-stacks')
def stacks_section():
    return render_template('the-stacks.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks)

@app.route('/decades')
def decades_section():
    return render_template('decades.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks)

@app.route('/genres-log')
def genre_section_log():
    return render_template('genres-log.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks, username=session["username"])

@app.route('/styles-log')
def style_section_log():
    return render_template('styles-log.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks, username=session["username"])

@app.route('/artists-log')
def artist_section_log():
    return render_template('artists-log.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks, username=session["username"])

@app.route('/the-stacks-log')
def stacks_section_log():
    return render_template('the-stacks-log.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks, username=session["username"])

@app.route('/decades-log')
def decades_section_log():
    return render_template('decades-log.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks, username=session["username"])

@app.route('/genres/<genre>')
def genre_search(genre):
    results = Album.query.filter(Album.genre.like(f"%{genre}%")).all()
    songs = [{'title': album.title, 'artist': album.artist, 'id': album.id, 'genre': album.genre, 'image': album.cover_image, 'shelf': album.shelf_label, 'tracklist': album.tracklist, 'style': album.style} for album in results]
    return jsonify({'songs': songs})

@app.route('/styles/<style>')
def style_search(style):
    results = Album.query.filter(Album.style.like(f"%{style}%")).all()
    print(results)
    songs = [{'title': album.title, 'artist': album.artist, 'id': album.id, 'genre': album.genre, 'image': album.cover_image, 'shelf': album.shelf_label, 'tracklist': album.tracklist, 'style': album.style} for album in results]
    print(songs)
    return jsonify({'songs': songs})

@app.route('/artists/<artist>')
def artist_search(artist):
    results = Album.query.filter(Album.artist.like(f"%{artist}%")).all()
    print(results)
    songs = [{'title': album.title, 'artist': album.artist, 'id': album.id, 'genre': album.genre, 'image': album.cover_image, 'shelf': album.shelf_label, 'tracklist': album.tracklist, 'style': album.style} for album in results]
    print(songs)
    return jsonify({'songs': songs})

@app.route('/the-stacks/<stack>')
def stacks_search(stack):
    results = Album.query.filter(Album.shelf_label.like(f"%{stack}%")).all()
    print(results)
    songs = [{'title': album.title, 'artist': album.artist, 'id': album.id, 'genre': album.genre, 'image': album.cover_image, 'shelf': album.shelf_label, 'tracklist': album.tracklist, 'style': album.style} for album in results]
    print(songs)
    return jsonify({'songs': songs})

@app.route('/decades/<decade>')
def decades_search(decade):
    start_year = int(decade[0:4])
    end_year = start_year + 9

    results = Album.query.filter(Album.year >= start_year, Album.year <= end_year).all()
    print(start_year)
    songs = [{'title': album.title, 'artist': album.artist, 'id': album.id, 'genre': album.genre, 'image': album.cover_image, 'shelf': album.shelf_label, 'tracklist': album.tracklist, 'style': album.style} for album in results]
    print(end_year)
    return jsonify({'songs': songs})

@app.route('/album-locator', methods=['POST'])
def locate_album():
    album_id = request.form.get('id')
    print('album_id', album_id)
    result = Album.query.filter(Album.id == album_id).first()
    print('result:', result)
    if result:
        song = [{'shelf_label': result.shelf_label}]
        return jsonify({'shelf_label': song})
    else:
        return jsonify({'error': 'Album not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)