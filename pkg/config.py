import os 

class GeneralConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(GeneralConfig):
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+mysqlconnector://root@localhost/transjoy' )

