# pkg/shipment/routes.py

from flask import render_template, redirect, url_for, flash, session, jsonify, request
from . import shipmentobj 
from .form import NewShipmentForm
from pkg.models import State, City, User, db # Ensure User and db are imported
# Removed: from pkg.auth.decorators import login_required 

# NOTE: The 'u' (current user object) is best retrieved within the function
# for security and context, especially without a decorator.

@shipmentobj.route('/new/', methods=['GET', 'POST'])
def new_shipment():
    """Handles the creation of a new shipment order."""
    
    # 1. Security Check: Ensure user is logged in (Manual check)
    user_id = session.get('useronline')
    if not user_id:
        flash('You must be logged in to create a new shipment.', 'warning')
        return redirect(url_for('bpuser.login'))
        
    # Retrieve the current user object
    u = User.query.get(user_id) 

    form = NewShipmentForm()
    
    if form.validate_on_submit():
        # *** SHIPMENT LOGIC STARTS HERE ***
        
        distance = form.distance_km.data
        amount = form.calculated_amount.data
        
        if not distance or not amount:
            # Note: This is a client-side error, but we validate it server-side too.
            flash('Please click the "Calculate Rate" button and ensure a valid rate is displayed before confirming.', 'danger')
            return render_template('shipment/new_shipment.html', form=form, u=u, title='Create New Shipment')
        
        # ... (Shipment creation logic) ...
        
        flash(f'Shipment order received. Redirecting to payment...', 'success')
        # Redirecting to the dashboard for now
        return redirect(url_for('bpuser.dashboard')) 

    return render_template(
        'shipment/new_shipment.html', 
        form=form, 
        u=u, # Pass the user object
        title='Create New Shipment'
    )

@shipmentobj.route('/api/cities/<int:state_id>')
def get_cities(state_id):
    """
    API endpoint to fetch cities belonging to a specific state.
    """
    if state_id == 0:
        return jsonify([])

    cities = City.query.filter_by(state_id=state_id).order_by(City.name).all()
    city_list = [{'id': city.id, 'name': city.name} for city in cities]
    return jsonify(city_list)