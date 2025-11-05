from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import InputRequired

class BusForm(FlaskForm):
    kms=FloatField('Kilometers', [InputRequired()])
    fuel_type= SelectField('Type of fuel', [InputRequired()],
        choices=[('Diesel', 'Diesel'),('Petrol', 'Petrol')])
    submit=SubmitField('Submit') 