from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

genres = ['blues', 'chickenskin', "children's", 'genetic memory', 'jazz', 'reggae', 'scordatura', 'spoken word', 'world', 'electronic', 'funk & soul', 'hip-hop', 'pop', 'rock', 'stage']
decades = ['1900s', '1910s', '1920s', '1930s', '1940s', '1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s']
styles = ['bop', 'post bop', 'interview', 'free jazz', 'experimental', 'afro-cuban jazz', 'cape jazz', 'contemporary jazz', 'latin jazz', 'salsa', 'guajira', 'guaracha', 'guaguancó', 'smooth jazz', 'cool jazz', 'nueva trova', 'cha-cha', 'instrumental', 'bolero', 'avant-garde jazz', 'merengue', 'mambo']
artists = ['charles mingus', 'rova saxophone quartet', 'carl stone','hugh masekela', "marty ehrlich's dark woods ensemble", 'tim hagans', 'conexion latina', 'oscar castro-neves', 'pablo milanés', 'perez prado and his orchestra', 'mario pavone', 'marc ribot']
stacks = ['2A']

@app.route('/')
def main():
    return render_template('home.html', genres=genres, decades=decades, styles=styles, artists=artists, stacks=stacks)

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

@app.route('/genres/<genre>')
def genre_search(genre):
    results = Album.query.filter(Album.genre.like(f"%{genre}%")).all()
    songs = [{'title': album.title, 'artist': album.artist, 'id': album.id, 'genre': album.genre, 'image': album.cover_image, 'shelf': album.shelf_label} for album in results]
    return jsonify({'songs': songs})

@app.route('/styles/<style>')
def style_search(style):
    results = Album.query.filter(Album.style.like(f"%{style}%")).all()
    print(results)
    songs = [{'title': album.title, 'artist': album.artist, 'id': album.id, 'genre': album.genre, 'image': album.cover_image, 'shelf': album.shelf_label} for album in results]
    print(songs)
    return jsonify({'songs': songs})

@app.route('/artists/<artist>')
def artist_search(artist):
    results = Album.query.filter(Album.artist.like(f"%{artist}%")).all()
    print(results)
    songs = [{'title': album.title, 'artist': album.artist, 'id': album.id, 'genre': album.genre, 'image': album.cover_image, 'shelf': album.shelf_label} for album in results]
    print(songs)
    return jsonify({'songs': songs})

@app.route('/the-stacks/<stack>')
def stacks_search(stack):
    results = Album.query.filter(Album.shelf_label.like(f"%{stack}%")).all()
    print(results)
    songs = [{'title': album.title, 'artist': album.artist, 'id': album.id, 'genre': album.genre, 'image': album.cover_image, 'shelf': album.shelf_label} for album in results]
    print(songs)
    return jsonify({'songs': songs})

@app.route('/decades/<decade>')
def decades_search(decade):
    start_year = int(decade[0:4])
    end_year = start_year + 9

    results = Album.query.filter(Album.year >= start_year, Album.year <= end_year).all()
    print(start_year)
    songs = [{'title': album.title, 'artist': album.artist, 'id': album.id, 'genre': album.genre, 'image': album.cover_image, 'shelf': album.shelf_label} for album in results]
    print(end_year)
    return jsonify({'songs': songs})