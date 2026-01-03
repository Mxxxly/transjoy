from flask import Blueprint
shipmentobj = Blueprint('bpshipment',__name__,url_prefix='/shipment/v1')

# to make the local routes available

from pkg.shipment import routes #from. import routes 