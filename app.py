from flask import Flask, request, render_template, jsonify, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from lists import genres, styles, stacks, artists, decades
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "poop"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../albums.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, index = True, nullable = False)
    password_hash = db.Column(db.String(80), unique = True, index = True, nullable = False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.route('/')
def main():
    if "username" in session:
        return redirect(url_for('homelog'))
    return render_template('home.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('homelog'))
    else:
        return render_template('home.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)