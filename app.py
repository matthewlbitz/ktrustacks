from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('base.html')

@app.route('/<section>')
def genres(section):
    return render_template('search_section.html', section=section)