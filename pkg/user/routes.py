from flask import Blueprint, render_template, redirect, url_for, flash,jsonify
from pkg.models import User
from pkg.user import userobj
from .form import SignupForm,LoginForm # import the form here
from werkzeug.security import generate_password_hash,check_password_hash
from pkg.models import db,State,City  # SQLAlchemy instance

@userobj.get('/')
def home():
    user = User.query.all()

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
            flash(f"Welcome back, {user.full_name}!", "success")
            return redirect(url_for('bpuser.dashboard'))  # Your dashboard route
        else:
            flash("Invalid email or password", "danger")
    return render_template('user/login.html', form=form)



@userobj.route('/dashboard/')
def dashboard():
    user = User.query.all()
    return render_template('user/dashboard.html',user=user)  # create this template