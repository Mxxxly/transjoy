# pkg/shipment/form.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from pkg.models import State, City # Ensure this import path is correct

class NewShipmentForm(FlaskForm):
    # Receiver Details
    receiver_name = StringField("Receiver Full Name", validators=[DataRequired(), Length(max=120)])
    receiver_phone = StringField("Receiver Phone", validators=[DataRequired(), Length(max=20)])

    # Pickup Details
    pickup_address = TextAreaField("Pickup Address", validators=[DataRequired(), Length(max=255)])
    pickup_state = SelectField("Pickup State", coerce=int, validators=[DataRequired()])
    pickup_city = SelectField("Pickup City", coerce=int, validators=[DataRequired()])
    
    # Delivery Details
    delivery_address = TextAreaField("Delivery Address", validators=[DataRequired(), Length(max=255)])
    delivery_state = SelectField("Delivery State", coerce=int, validators=[DataRequired()])
    delivery_city = SelectField("Delivery City", coerce=int, validators=[DataRequired()])

    # Package Details
    package_weight = FloatField("Package Weight (kg)", validators=[DataRequired(), NumberRange(min=0.1, message="Weight must be positive.")])
    delivery_type = SelectField("Delivery Type", choices=[
        ('bike', 'Motorcycle/Bike (Quick & Small)'),
        ('van', 'Van/Bus (Standard & Medium)'),
        ('truck', 'Truck (Large/Heavy)')
    ], validators=[DataRequired()])
    
    # Hidden fields for calculated data (distance and amount) - populated by JS/backend
    distance_km = FloatField("Distance (km)", validators=[Optional()])
    calculated_amount = FloatField("Calculated Amount", validators=[Optional()])

    submit = SubmitField("Confirm Shipment & Proceed to Payment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate state choices globally
        state_choices = [(s.id, s.name) for s in State.query.order_by(State.name).all()]
        self.pickup_state.choices = [(0, 'Select State')] + state_choices
        self.delivery_state.choices = [(0, 'Select State')] + state_choices

        # City choices will be populated dynamically via JavaScript or on first load
        self.pickup_city.choices = [(0, 'Select City')]
        self.delivery_city.choices = [(0, 'Select City')]