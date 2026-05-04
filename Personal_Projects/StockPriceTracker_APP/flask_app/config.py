# Flask App Configuration

import os

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    TEMPLATE_AUTO_RELOAD = True
    JSON_SORT_KEYS = False
    
    # Data paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    DATA_FILE = os.path.join(DATA_DIR, 'stock_data.json')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


# Configuration by environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
