import os

class Config:
    '''
    General configuration parent class
    '''
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ephantus:switcher12@localhost/piches_app'
    DATABASE_URL='postgres://gabsykbpnmcoqo:2aefad3dea83969f994635b5722dcbed4765f137335adcc536c9d92249c22662@ec2-23-21-195-249.compute-1.amazonaws.com:5432/d3p4mmhs9n404v'
    SECRET_KEY=os.environ.get('SECRET_KEY')
class ProdConfig(Config):
    '''
    Pruduction configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''    
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class TestConfig(Config):
    '''
    Testing configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass

class DevConfig(Config):
    '''
    Development configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    

    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig
}
