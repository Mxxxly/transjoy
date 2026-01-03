from flask import render_template
from pkg import app

@app.get('/')
def landing_page():
    return render_template('index.html')

