from flask import Blueprint
authobj = Blueprint('bpauth',__name__,template_folder='templates',static_folder='static',url_prefix='/auth')

# to make the local routes available

from pkg.auth import routes #from. import routes 