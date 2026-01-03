from flask import Blueprint
agentobj = Blueprint('bpagent',__name__,template_folder='templates',static_folder='static',url_prefix='/agent')

from pkg.agent import routes