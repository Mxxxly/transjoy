import json
import os 
from pkg.agent import agentobj
from flask_httpauth import HTTPBasicAuth
from pkg.models import Agent, db

auth = HTTPBasicAuth()


