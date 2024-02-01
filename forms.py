from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField
from wtforms.validators import DataRequired

class SpendingsForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    amount = FloatField('amount', validators=[DataRequired()])
    # id = IntegerField('id', validators=[DataRequired()])