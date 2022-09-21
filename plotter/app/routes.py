from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SearchForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        flash(f'Searching for plot{form.search_query}')
        return redirect(url_for('index'))
    return render_template('index.html', title = 'HOME', form = form)

@app.route('/about')
def about():
    return render_template('about.html', title = 'ABOUT')

@app.route('/how')
def how():
    return render_template('how.html', title = 'HOW THIS WORKS')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html', title = 'FAQs')
