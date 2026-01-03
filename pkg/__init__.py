from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

csrf = CSRFProtect()

def create_app():
    from pkg import config
    from pkg.models import db #we want app to be aware of db 
    #bring in the instances of the Blueprint 
    from pkg.admin import adminobj
    from pkg.user import userobj
    from pkg.api import apiobj
    from pkg.agent import agentobj

    app = Flask(__name__,instance_relative_config=True)

    #register the Blueprint so that app can become aware of them and this comes after app, if app is not created we should not use it 
    app.register_blueprint(userobj)
    app.register_blueprint(adminobj)
    app.register_blueprint(apiobj)
    app.register_blueprint(agentobj)

    
    app.config.from_pyfile('config.py',silent=True)
    app.config.from_object(config.TestConfig)
    csrf.init_app(app) #lazy-loading
    csrf.exempt(apiobj) #API allow visitation to the routes from any source
    db.init_app(app) #lazy-loading i.e suppling app to SQLALchemy class at a later time
    Migrate(app,db)
    return app

app = create_app()


from pkg import models,general_routes
#, models  # Import routes and models to ensure they are loaded and the app recognizes them