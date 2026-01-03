from flask import Blueprint
adminobj = Blueprint('bpadmin',__name__,template_folder='templates',static_folder='static',url_prefix='/admin')

# to make the routes available

from pkg.admin import routes #from. import routes 