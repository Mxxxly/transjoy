from flask import render_template
from pkg.user import userobj

@userobj.get('/')
def home():
    return render_template('user/index.html')


@userobj.get('/signup/')
def signup():
    
    return render_template('user/signup.html')