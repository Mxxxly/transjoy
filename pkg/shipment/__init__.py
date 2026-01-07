from flask import Blueprint
shipmentobj = Blueprint('bpshipment',__name__,template_folder='templates',static_folder='static',url_prefix='/shipment')

# to make the local routes available

from pkg.shipment import routes #from. import routes 