from flask import Blueprint
trackingobj = Blueprint('bptracking',__name__,url_prefix='/tracking/v1')

# to make the local routes available

from pkg.tracking import routes #from. import routes 