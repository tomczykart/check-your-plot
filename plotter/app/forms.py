from flask_wtf  import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from app.models import User, SearchQuery

class SearchForm(FlaskForm):
    search_query = StringField('Plot id number', validators=[DataRequired()])
    submit = SubmitField('Search')

class SendResultsForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send results')
