from flask import render_template, flash, redirect, url_for, g
from flask_login import current_user, login_user
from app import app, db
from app.forms import SearchForm, SendResultsForm
from app.models import User, SearchQuery

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    #flash(current_user)
    #logic for search form submit
    form = SearchForm()
    if form.validate_on_submit():
        #flash(f'Searching for plot{form.search_query}')
        #add unknown user with new search query to db
        #get data from external api
        return redirect(url_for('results'))
    #render index page
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


@app.route('/results', methods=['GET', 'POST'])
def results():
    form = SendResultsForm()
    if form.validate_on_submit():
        flash(f'Sending results to {form.user_email}')
        #send email
        return redirect(url_for('index'))
    return render_template('results.html', title = 'RESULTS', form = form)
