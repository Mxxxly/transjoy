from flask import Blueprint
paymentobj = Blueprint('bppayment',__name__,url_prefix='/payment/v1')

# to make the local routes available

from pkg.payments import routes #from. import routes 