from flask_wtf  import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search_query = StringField('Plot id number', validators=[DataRequired()])
    submit = SubmitField('Search')
