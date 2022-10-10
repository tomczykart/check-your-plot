from flask_wtf  import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User, SearchQuery

class SearchForm(FlaskForm):
    search_query = StringField('Plot id number:', validators=[DataRequired()])
    submit = SubmitField('Search')

    def validate_search_query(self, search_query):#verify plot number

        #WWPPGG_R.XXXX.NR
        ww = search_query.data[0:2]
        pp = search_query.data[2:4]
        gg = search_query.data[4:6]
        r = search_query.data[7:8]
        xxxx = search_query.data.split('.')[1]
        nr = search_query.data.split('.')[2]


        if not (ww + pp+ gg + r + xxxx + nr.replace('/', '')).isdigit():
            raise ValidationError('Identyfikator niepoprawny')

        elif len(search_query.data.split('_')[0]) != 6:
            raise ValidationError('Niepoprawny kod województwa/powiatu/gminy')

        elif len(xxxx) != 4:
            raise ValidationError('Niepoprawny numer obrębu')

        elif not int(ww) % 2 == 0 & 1 < int(ww) < 33:
            raise ValidationError('Kod województwa niepoprawny')

        elif not 0 < int(pp) < 100:
            raise ValidationError('Kod powiatu niepoprawny')
