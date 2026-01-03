from flask import Blueprint
trackingobj = Blueprint('bptracking',__name__,template_folder='templates',static_folder='static',url_prefix='/tracking')

# to make the local routes available

from pkg.tracking import routes #from. import routes 