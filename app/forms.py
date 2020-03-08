from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class PredictionForm(FlaskForm):
    precip = StringField('Precipitation' , validators=[DataRequired()])
    snow = StringField('Snow', validators=[DataRequired()])
    tavg = StringField('Average Temperature', validators=[DataRequired()])
    tmax = StringField('Max Temperature', validators=[DataRequired()])
    tmin = StringField('Min Temperature', validators=[DataRequired()])
    submit = SubmitField('Predict')