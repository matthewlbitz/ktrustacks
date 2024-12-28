from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///albums.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

