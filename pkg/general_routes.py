from flask import render_template,session
from pkg import app
from pkg.models import db, User, State, City

@app.get('/')
def home_page():
    user = User.query.all()
    user_id= session.get('useronline')
    u= User.query.get(user_id)
    return render_template('index.html',user=user,u=u,user_id=user_id)


@app.get('/oldindex/')
def landing_page():
    return render_template('indext.html')


@app.get('/about/')
def about_page():
    return render_template('about.html')


@app.get('/service/')
def service():
    return render_template('service.html')

@app.get('/contact/')
def contact():
    return render_template('contact.html')