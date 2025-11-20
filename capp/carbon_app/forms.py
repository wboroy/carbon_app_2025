from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import InputRequired

class TransportForm(FlaskForm):
    transport = SelectField(
        'Transport Type',
        [InputRequired()],
        choices=[
            ('Bus', 'Bus'), ('Car', 'Car'),('Motorbike','Motorbike'),('Train','Train'),('Ferry','Ferry'),
            ('Plane Economy','Plane Economy'), ('Plane Business','Plane Business'),('Bybane','Bybane'),('Walking/Cycling','Walking/Cycling')])
    
    kms = FloatField(
        'Kilometers', 
        [InputRequired()])
    
    fuel_type = SelectField(
        'Type of fuel', 
        [InputRequired()],
        choices=[
            ('Diesel', 'Diesel'),('Petrol','Petrol'),('Electric','Electric'),('Human powered','Human powered'),('Jetfuel','Jetfuel'),('Fossil fuel','Fossil fuel')])
    
    passenger = FloatField(
        "Passengers",
        [InputRequired()],
        default=1,
    )

    submit=SubmitField('Submit')    

