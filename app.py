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

@app.route('/')
def main():
    return render_template('home.html', genres=genres, decades=decades)

@app.route('/<section>')
def section(section):
    return render_template(f'{section}.html', section=section, genres=genres, decades=decades)

@app.route('/<section>/<subsection>')
def subsection(section, subsection):
    return render_template(f'{section}.html', section=section, subsection=subsection, genres=genres, decades=decades)

@app.route('/genres/<genre>')
def genre_search(genre):
    results = Album.query.filter(Album.genre.like(f"%{genre}%")).all()
    songs = [{'title': album.title, 'artist': album.artist, 'id': album.id, 'genre': album.genre, 'image': album.cover_image, 'shelf': album.shelf_label} for album in results]
    return jsonify({'songs': songs})