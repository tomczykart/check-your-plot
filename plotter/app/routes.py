from flask import render_template
from app import app
from app.forms import SearchForm

@app.route('/')
@app.route('/index')
def index():
    form = SearchForm()
    return render_template('index.html', title = 'HOME', form = form)

@app.route('/about')
def about():
    return render_template('about.html', title = 'ABOUT')

@app.route('/how')
def how():
    return render_template('how.html', title = 'HOW THIS WORKS')
