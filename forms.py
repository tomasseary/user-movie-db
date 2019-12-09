from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class addMovieForm(FlaskForm):
	movieId = StringField('movieId', validators=[DataRequired()])
	movieTitle = StringField('movieTitle', validators=[DataRequired()])
	movieGenre = StringField('movieGenre', validators=[DataRequired()])
	movieRating = StringField('movieRating', validators=[DataRequired()])
	movieReleased = IntegerField('movieReleased', validators=[DataRequired()])