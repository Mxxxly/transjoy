from flask import Blueprint, render_template, redirect, url_for, flash,jsonify,session, request
from pkg.models import User
from pkg.user import userobj
from .form import SignupForm,LoginForm # import the form here
from werkzeug.security import generate_password_hash,check_password_hash
from pkg.models import db,State,City, Shipment, ShipmentStatusHistory # SQLAlchemy instance

@userobj.get('/')
def home():
    user = User.query.all()
    user_id= session.get('useronline')
    u= User.query.get(user_id)
    

    return render_template('user/index.html',user=user)


@userobj.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    # Populate states dynamically
    form.state.choices = [(s.id, s.name) for s in State.query.order_by(State.name).all()]
    form.city.choices = [(c.id, c.name) for c in City.query.filter_by(state_id=form.state.data).all()] if form.state.data else []

    if form.validate_on_submit():

        # Check if user exists
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for('bpuser.login'))

        # Create user
        new_user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            state_id=form.state.data,
            city_id=form.city.data,
            password_hash=generate_password_hash(form.password.data)
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for('bpuser.login'))

    return render_template('user/signup.html', form=form)


@userobj.route('/cities/<int:state_id>')
def cities(state_id):
    cities = City.query.filter_by(state_id=state_id).order_by(City.name).all()
    city_list = [{"id": c.id, "name": c.name} for c in cities]
    return jsonify(city_list)




@userobj.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session["useronline"] = user.id
            flash(f"Welcome back, {user.full_name}!", "success")
            return redirect(url_for('bpuser.dashboard'))  # Your dashboard route
        else:
            flash("Invalid email or password", "danger")
    return render_template('user/login.html', form=form)



@userobj.route('/dashboard/')
def dashboard():
    user_id= session.get('useronline')
    u= User.query.get(user_id)
    user = User.query.all()
    if not u:
        flash("You must be logged in as an User to access this page.", "warning")
        return redirect(url_for('bpuser.login'))

    return render_template('user/dashboard.html',user=user,user_id=user_id,u=u)  # create this template


@userobj.route('/logout/')
def logout():
    """Logs the user out by clearing the session."""
    
    # 1. Clear the relevant session data
    # Check if the keys exist before trying to pop them
    if 'useronline' in session:
        session.pop('useronline')
        
    if 'user_full_name' in session:
        session.pop('user_full_name')

    # Optional: Clear the entire session if you have no other data you need to preserve
    # session.clear() 

    # 2. Flash a success message
    flash("You have been successfully logged out.", "info")

    # 3. Redirect to the login page (or homepage)
    # Using 'bpuser.login' ensures the link works correctly across blueprints
    return redirect(url_for('bpuser.login'))



@userobj.route('/track', methods=['GET'])
def track_shipment():
    """Handles the tracking ID submission and redirects to the results page."""
    
    # 1. Get the tracking ID from the URL parameters (since method is GET)
    tracking_id = request.args.get('tracking_id')

    if not tracking_id:
        flash("Please enter a valid Tracking ID.", "danger")
        return redirect(url_for('bpuser.dashboard')) # Send them back if the field was empty

    # 2. In a real application, you would query the database here:
    # shipment = Shipment.query.filter_by(tracking_number=tracking_id).first()
    
    # For now, we will assume you have a 'bpuser.tracking_results' page
    
    # 3. Redirect to a results page, passing the ID in the URL for the next view to process
    return redirect(url_for('bpuser.tracking_results', id=tracking_id))


@userobj.route('/tracking-results/<string:id>')
def tracking_results(id):
    """
    Fetches shipment details and history based on the tracking ID.
    The 'id' comes from the track_shipment redirect.
    """
    # 1. Fetch the shipment or return 404 if not found
    shipment = Shipment.query.filter_by(tracking_number=id).first()

    if not shipment:
        flash(f"Shipment with Tracking ID **{id}** not found.", "danger")
        # Redirect back to the dashboard or a dedicated tracking page
        return redirect(url_for('bpuser.dashboard')) 

    # 2. Fetch the detailed history records
    history = ShipmentStatusHistory.query.filter_by(shipment_id=shipment.id).order_by(
        ShipmentStatusHistory.created_at.desc() # Display newest status first
    ).all()

    # 3. Check if the shipment belongs to the current user (if logged in)
    # Assuming 'u' (current user object) is passed to the template for navbar/header
    # We fetch it again here to ensure it's available.
    user_id = session.get('useronline')
    u = User.query.get(user_id) if user_id else None

    # Check ownership for security, although public tracking is common
    if u and shipment.user_id != u.id:
        flash("Access Denied: This shipment does not belong to your account.", "danger")
        return redirect(url_for('bpuser.dashboard'))

    return render_template(
        'user/tracking_results.html', 
        shipment=shipment, 
        history=history,
        u=u # Pass the user object for the template's navbar/header
    )

# Note: Remember to update the 'track_shipment' route to redirect to this
# return redirect(url_for('bpuser.tracking_results', id=tracking_id))