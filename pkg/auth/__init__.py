from flask import Blueprint
authobj = Blueprint('bpauth',__name__,url_prefix='/auth/v1')

# to make the local routes available

from pkg.auth import routes #from. import routes 