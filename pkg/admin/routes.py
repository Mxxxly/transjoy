from flask import render_template
from pkg.admin import adminobj

@adminobj.route('/')
def home():
    return render_template('admin/index.html')


@adminobj.route('/dashboard/')
def dashboard():
    return render_template('admin/dashboard.html')