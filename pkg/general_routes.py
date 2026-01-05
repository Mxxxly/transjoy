from flask import render_template
from pkg import app

@app.get('/')
def home_page():
    return render_template('index.html')

@app.get('/oldindex/')
def landing_page():
    return render_template('indext.html')

@app.get('/about/')
def about_page():
    return render_template('about.html')