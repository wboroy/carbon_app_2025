from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import InputRequired

class TransportForm(FlaskForm):
    transport = SelectField(
        'Transport Type',
        [InputRequired()],
        choices=[
            ('Bus', 'Bus'), ('Car', 'Car')])
    kms=FloatField('Kilometers', [InputRequired()])
    fuel_type= SelectField('Type of fuel', [InputRequired()],
        choices=[('Diesel', 'Diesel'),('Petrol', 'Petrol')])
    submit=SubmitField('Submit')    

