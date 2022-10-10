from flask import render_template, flash, redirect, url_for, session, request
from app import app, db
from app.forms import SearchForm
from app.models import User, SearchQuery
from app.get_data import get_coordinates, generate_map, plot_area, parse_xml

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    #flash(current_user)
    #logic for search form submit
    form = SearchForm()
    if form.validate_on_submit():
        session['query'] = request.form.get('search_query')

        #get data from external api
        return redirect(url_for('results'))
    #render index page
    return render_template('index.html', title = 'HOME', form = form)



@app.route('/results', methods=['GET', 'POST'])
def results():

    try:
        plot_wkt = get_coordinates(session['query'],'4326')
        #generate plot border coordinates
        map_png = generate_map(session['query'],'2180')

        #ask api for plot map
        plot_parameters = parse_xml(session['query'],'2180')
        #ask api for plot parameters
        area = plot_area(session['query'],'2180')
        #calculate plot area

        return render_template('results.html',
                                title ='RESULTS',
                                plot_wkt=plot_wkt,
                                map_png=map_png,
                                plot_parameters=plot_parameters,
                                area=area
                                )
    except ValueError:
        flash('Wyszukiwanie zakończone niepowodzeniem')
        return redirect(url_for('index'))
        




@app.route('/about')
def about():
    return render_template('about.html', title = 'ABOUT')


@app.route('/how')
def how():
    return render_template('how.html', title = 'HOW THIS WORKS')


@app.route('/faqs')
def faqs():
    return render_template('faqs.html', title = 'FAQs')
