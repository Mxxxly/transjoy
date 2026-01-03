from flask import Blueprint
apiobj = Blueprint('bpapi',__name__,url_prefix='/api/v1')

# to make the local routes available

from pkg.api import routes #from. import routes 